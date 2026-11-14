"""Надёжный слой поверх UDP: порядок, подтверждения, фрагментация.

Класс `_UdpNet` ничего не знает об игре: он принимает функцию отправки
датаграммы и разбирает входящие пакеты.  Ввод и позиции идут без гарантий,
а команды, мир и рукопожатие — с подтверждениями и повторами.
"""
import json
import struct
import threading
import time
import zlib

from .config import (
    MP_UDP_ACK_INTERVAL,
    MP_UDP_FLAG_COMPRESSED,
    MP_UDP_FLAG_FRAGMENT,
    MP_UDP_FLAG_RELIABLE,
    MP_UDP_FRAG_BURST,
    MP_UDP_FRAG_SIZE,
    MP_UDP_HEADER,
    MP_UDP_IDLE_TIMEOUT,
    MP_UDP_MAGIC,
    MP_UDP_MAX_MESSAGE,
    MP_UDP_RELIABLE_TYPES,
    MP_UDP_RESEND_INTERVAL,
)


class _UdpNet:
    """Надёжный слой поверх UDP с доставкой по порядку.

    Каждое сообщение — JSON.  Надёжные сообщения (рукопожатие, диффы мира,
    команды) получают номер, подтверждаются получателем и при потере
    пересылаются.  Большие сообщения режутся на фрагменты по ~1200 байт и
    сжимаются zlib, поэтому полный снапшот мира проходит одним «пакетным
    поездом».  Ввод, позиции и эффекты идут как обычные датаграммы без
    повторов: устаревшие данные не должны тормозить свежие.
    """

    def __init__(self, send_func, on_message, on_close, sock=None,
                 start_reader=True, addr=None):
        self.send_func = send_func
        self.on_message = on_message
        self.on_close = on_close
        self.sock = sock
        self.addr = addr
        self.alive = True
        self.last_recv = time.time()
        self.out_seq = 0
        self.in_seq = 0
        self.in_ack_bits = 0
        self._got_packet = False
        self.next_out_msg = 1
        self.next_in_msg = 1
        self.ack_msg = 0
        self.peer_ack_msg = 0
        self.outbox = {}
        self.fragments = {}
        self.ready_msgs = {}
        self.pending_ack = False
        self._last_ack_sent = 0.0
        self.rtt = 0.0
        self.packets_in = 0
        self.packets_out = 0
        self.bytes_in = 0
        self.bytes_out = 0
        self._lock = threading.RLock()
        if start_reader and sock is not None:
            threading.Thread(target=self._reader, args=(sock,),
                             daemon=True).start()
        threading.Thread(target=self._maintenance, daemon=True).start()

    # ---------------------------------------------------------- отправка
    def send(self, msg):
        if not self.alive:
            return False
        try:
            payload = (json.dumps(msg, ensure_ascii=False,
                                  separators=(',', ':')) + "\n").encode('utf-8')
        except Exception:
            return False
        compressed = False
        if len(payload) >= 512:
            try:
                packed = zlib.compress(payload, 3)
                if len(packed) < len(payload) - 32:
                    payload = packed
                    compressed = True
            except Exception:
                pass
        reliable = msg.get('type') in MP_UDP_RELIABLE_TYPES
        if not reliable and len(payload) > MP_UDP_FRAG_SIZE:
            # Слишком большая датаграмма гарантированно развалится на MTU.
            reliable = True
        if not reliable:
            self._send_datagram(
                payload, 0, 0, 1,
                MP_UDP_FLAG_COMPRESSED if compressed else 0)
            return True
        with self._lock:
            mid = self.next_out_msg
            self.next_out_msg += 1
            chunks = [payload[i:i + MP_UDP_FRAG_SIZE]
                      for i in range(0, len(payload), MP_UDP_FRAG_SIZE)]
            if not chunks:
                chunks = [b'']
            self.outbox[mid] = {'chunks': chunks, 'next': 0.0, 'tries': 0,
                                'compressed': compressed,
                                'type': msg.get('type')}
        self._send_reliable(mid)
        return True

    def pending_reliable(self, msg_type=None):
        """Сколько надёжных сообщений ещё не подтверждено.

        С ``msg_type`` считает только сообщения этого типа — игра использует
        это как обратное давление для диффов мира.
        """
        with self._lock:
            if msg_type is None:
                return len(self.outbox)
            return sum(1 for entry in self.outbox.values()
                       if entry.get('type') == msg_type)

    def _send_datagram(self, payload, msg_id, frag_idx, frag_count, flags):
        with self._lock:
            self.out_seq += 1
            seq = self.out_seq
            ack = self.in_seq
            bits = self.in_ack_bits
            ack_msg = self.ack_msg
        header = MP_UDP_HEADER.pack(MP_UDP_MAGIC, flags, seq, ack, bits,
                                    msg_id, ack_msg, frag_idx, frag_count)
        data = header + payload
        try:
            self.send_func(data)
        except Exception:
            return False
        self.packets_out += 1
        self.bytes_out += len(data)
        return True

    def _send_reliable(self, mid):
        with self._lock:
            entry = self.outbox.get(mid)
            if entry is None:
                return
            chunks = entry['chunks']
            count = len(chunks)
            cursor = int(entry.get('cursor', 0))
            if cursor >= count:
                cursor = 0
            end = min(count, cursor + MP_UDP_FRAG_BURST)
            compressed = entry['compressed']
        flags = MP_UDP_FLAG_RELIABLE
        if count > 1:
            flags |= MP_UDP_FLAG_FRAGMENT
        if compressed:
            flags |= MP_UDP_FLAG_COMPRESSED
        for idx in range(cursor, end):
            if not self.alive:
                return
            self._send_datagram(chunks[idx], mid, idx, count, flags)
        with self._lock:
            entry = self.outbox.get(mid)
            if entry is None:
                return
            if end < count:
                # Большой снапшот/дифф не вываливаем в сокет одним залпом:
                # иначе буфер приёма переполняется, половина фрагментов
                # теряется, и сообщение бесконечно переотправляется целиком.
                # Продолжим на следующем витке обслуживания.
                entry['cursor'] = end
                entry['next'] = time.time()
            else:
                entry['cursor'] = 0
                entry['next'] = time.time() + MP_UDP_RESEND_INTERVAL
                entry['tries'] += 1
        # Надёжное сообщение повторяется, пока не придёт подтверждение.
        # Раньше после MP_UDP_MAX_RESENDS попыток соединение закрывалось:
        # один застрявший фрагмент или всплеск диффов мира рвал всю сессию.
        # Теперь живость пира определяет только тайм-аут молчания, а
        # застрявшее сообщение продолжает повторяться до подтверждения.

    # ---------------------------------------------------------- приём
    def _reader(self, sock):
        errors = 0
        while self.alive:
            try:
                data = sock.recv(65535)
                errors = 0
            except OSError:
                # Windows присылает WSAECONNRESET (ICMP port unreachable)
                # на UDP-сокет как обычную ошибку чтения.  Это не значит,
                # что канал мёртв: просто один старый пакет не дошёл.
                # Раньше поток чтения из-за этого завершался и клиент
                # «терял соединение» на ровном месте.
                errors += 1
                if not self.alive or errors > 400:
                    break
                time.sleep(0.01)
                continue
            if not data:
                break
            self.handle_datagram(data)
        self.close()

    def handle_datagram(self, data):
        if not self.alive or len(data) < MP_UDP_HEADER.size:
            return
        try:
            (magic, flags, seq, _ack, _ack_bits, msg_id, ack_msg,
             frag_idx, frag_count) = MP_UDP_HEADER.unpack_from(data)
        except struct.error:
            return
        if magic != MP_UDP_MAGIC:
            return
        payload = data[MP_UDP_HEADER.size:]
        now = time.time()
        self.last_recv = now
        self.packets_in += 1
        self.bytes_in += len(data)
        with self._lock:
            if not self._got_packet:
                self._got_packet = True
                self.in_seq = seq
                self.in_ack_bits = 0
            elif seq > self.in_seq:
                shift = seq - self.in_seq
                if shift < 32:
                    self.in_ack_bits = (
                        (self.in_ack_bits << shift) | (1 << (shift - 1))
                    ) & 0xFFFFFFFF
                else:
                    self.in_ack_bits = 0
                self.in_seq = seq
            elif seq < self.in_seq and self.in_seq - seq <= 32:
                self.in_ack_bits |= 1 << (self.in_seq - seq - 1)
            if ack_msg > self.peer_ack_msg:
                # ack_msg — это подтверждение НАШИХ исходящих сообщений.
                # Раньше он сравнивался с self.ack_msg (подтверждением
                # входящих), и при двустороннем обмене подтверждения
                # игнорировались: очередь исходящих росла вечно.
                self.peer_ack_msg = ack_msg
                stale = [mid for mid in self.outbox if mid <= ack_msg]
                for mid in stale:
                    self.outbox.pop(mid, None)
        if not payload:
            self.pending_ack = True
            return
        self.pending_ack = True
        if flags & MP_UDP_FLAG_RELIABLE:
            self._handle_reliable(msg_id, frag_idx, frag_count, payload, flags)
        elif not (flags & MP_UDP_FLAG_FRAGMENT):
            msg = self._decode(payload, flags)
            if msg is not None:
                self._deliver(msg)

    def _handle_reliable(self, msg_id, frag_idx, frag_count, payload, flags):
        if msg_id <= 0 or frag_count <= 0:
            return
        if msg_id < self.next_in_msg:
            return  # уже доставлено
        now = time.time()
        delivered = []
        with self._lock:
            entry = self.fragments.get(msg_id)
            if entry is None:
                entry = {'count': frag_count, 'parts': {}, 'time': now}
                self.fragments[msg_id] = entry
            entry['parts'][frag_idx] = payload
            if len(entry['parts']) < entry['count']:
                return
            raw = b''.join(entry['parts'].get(i, b'')
                           for i in range(entry['count']))
            self.fragments.pop(msg_id, None)
            if len(raw) > MP_UDP_MAX_MESSAGE:
                return
            if flags & MP_UDP_FLAG_COMPRESSED:
                try:
                    raw = zlib.decompress(raw)
                except Exception:
                    return
            try:
                msg = json.loads(raw.decode('utf-8').rstrip('\n'))
            except Exception:
                return
            self.ready_msgs[msg_id] = (now, msg)
            while self.next_in_msg in self.ready_msgs:
                _ts, item = self.ready_msgs.pop(self.next_in_msg)
                delivered.append(item)
                self.ack_msg = self.next_in_msg
                self.next_in_msg += 1
            self.pending_ack = True
        for item in delivered:
            self._deliver(item)

    @staticmethod
    def _decode(payload, flags):
        if flags & MP_UDP_FLAG_COMPRESSED:
            try:
                payload = zlib.decompress(payload)
            except Exception:
                return None
        try:
            return json.loads(payload.decode('utf-8').rstrip('\n'))
        except Exception:
            return None

    def _deliver(self, msg):
        try:
            self.on_message(msg)
        except Exception:
            pass

    # ---------------------------------------------------------- служебное
    def _maintenance(self):
        while self.alive:
            time.sleep(0.02)
            now = time.time()
            with self._lock:
                due = [mid for mid, entry in self.outbox.items()
                       if entry['next'] <= now]
            for mid in due:
                if not self.alive:
                    return
                self._send_reliable(mid)
            need_ack = False
            with self._lock:
                for mid, entry in list(self.fragments.items()):
                    if now - entry['time'] > 15.0:
                        self.fragments.pop(mid, None)
                for mid, (ts, _msg) in list(self.ready_msgs.items()):
                    if now - ts > 15.0:
                        self.ready_msgs.pop(mid, None)
                if (self.pending_ack and
                        now - self._last_ack_sent >= MP_UDP_ACK_INTERVAL):
                    self.pending_ack = False
                    self._last_ack_sent = now
                    need_ack = True
            if need_ack:
                self._send_datagram(b'', 0, 0, 0, 0)

    def close(self):
        with self._lock:
            if not self.alive:
                return
            self.alive = False
            self.outbox.clear()
            self.fragments.clear()
            self.ready_msgs.clear()
        sock = self.sock
        self.sock = None
        if sock is not None:
            try:
                sock.close()
            except Exception:
                pass
        try:
            self.on_close()
        except Exception:
            pass
