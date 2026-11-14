"""Визуальный слой: общие примитивы оформления.

Модуль не знает о состоянии игры: здесь только палитра, кэшированные
поверхности и маленькие функции рисования.  Части игры получают эти имена
через `surv.runtime` (см. `runtime.py`), поэтому импортировать их в частях
не нужно.

Все тяжёлые вещи (градиенты, панели, тени, свечения, виньетка, зерно)
считаются один раз и кэшируются по размеру и цветам: рисование кадра
не должно каждый раз пересобирать поверхности.
"""

import math

import pygame

try:
    import pygame.surfarray as _surfarray
except Exception:  # surfarray может быть собран без numpy
    _surfarray = None

try:
    import numpy as np
except ImportError:
    np = None


# --------------------------------------------------------------------------
#  Палитра
# --------------------------------------------------------------------------
#  Тёмный сине-графитовый камень для панелей, тёплое золото для акцентов,
#  холодный свет для текста.  Один набор на весь интерфейс.
PAL_INK        = (9, 12, 20)
PAL_PANEL_TOP  = (62, 74, 102)
PAL_PANEL_BOT  = (28, 35, 52)
PAL_BORDER     = (120, 146, 192)
PAL_BORDER_HI  = (186, 212, 248)
PAL_GOLD       = (242, 198, 108)
PAL_GOLD_DEEP  = (150, 108, 44)
PAL_TEXT       = (238, 244, 253)
PAL_MUTED      = (160, 178, 205)
PAL_ROW        = (46, 56, 80)
PAL_ROW_HOVER  = (62, 75, 102)
PAL_ROW_SEL    = (78, 100, 142)
PAL_OK         = (132, 220, 148)
PAL_BAD        = (238, 112, 104)
PAL_GLASS      = (13, 18, 30)
PAL_WARM       = (255, 236, 196)


# --------------------------------------------------------------------------
#  Мелкие помощники цвета
# --------------------------------------------------------------------------

def vis_clamp01(t):
    return 0.0 if t < 0.0 else (1.0 if t > 1.0 else t)


def vis_lerp(a, b, t):
    """Смешать два цвета (или числа) без округления альфы."""
    t = vis_clamp01(t)
    if isinstance(a, (int, float)):
        return a + (b - a) * t
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(min(len(a), len(b))))


def vis_shade(c, factor):
    """Умножить яркость: 1.0 — как есть, 0.5 — вдвое темнее."""
    return tuple(max(0, min(255, int(round(v * factor)))) for v in c[:3])


def vis_alpha(c, a):
    return (c[0], c[1], c[2], max(0, min(255, int(a))))


def vis_mix3(a, b, c, t):
    """Три опорных цвета: 0 -> a, 0.5 -> b, 1 -> c."""
    t = vis_clamp01(t)
    return vis_lerp(a, b, t * 2.0) if t < 0.5 else vis_lerp(b, c, (t - 0.5) * 2.0)


# --------------------------------------------------------------------------
#  Кэши
# --------------------------------------------------------------------------
_GRAD_CACHE = {}
_MASK_CACHE = {}
_PANEL_CACHE = {}
_SHADOW_CACHE = {}
_GLOW_CACHE = {}
_TEXT_CACHE = {}
_VIGNETTE_CACHE = {}
_GRAIN_CACHE = {}
_CACHE_LIMIT = 320


def _cache_put(cache, key, value):
    if len(cache) >= _CACHE_LIMIT:
        cache.clear()
    cache[key] = value
    return value


# --------------------------------------------------------------------------
#  Градиенты и скруглённые маски
# --------------------------------------------------------------------------

def vis_mask(w, h, radius):
    """Белая скруглённая маска: ею обрезаются градиентные поверхности."""
    key = (w, h, radius)
    mask = _MASK_CACHE.get(key)
    if mask is not None:
        return mask
    mask = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, w, h),
                     border_radius=max(0, radius))
    return _cache_put(_MASK_CACHE, key, mask)


def vis_gradient(w, h, top, bottom, radius=0):
    """Вертикальный градиент, при radius > 0 — со скруглёнными углами."""
    if w <= 0 or h <= 0:
        return pygame.Surface((max(1, w), max(1, h)), pygame.SRCALPHA)
    key = (w, h, tuple(top[:3]), tuple(bottom[:3]), radius)
    surf = _GRAD_CACHE.get(key)
    if surf is not None:
        return surf
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    for y in range(h):
        t = y / max(1, h - 1)
        pygame.draw.line(surf, vis_lerp(top, bottom, t), (0, y), (w, y))
    if radius:
        surf.blit(vis_mask(w, h, radius), (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return _cache_put(_GRAD_CACHE, key, surf)


def vis_gradient_h(w, h, left, right):
    """Горизонтальный градиент — для полос и подчёркиваний."""
    key = ("h", w, h, tuple(left[:3]), tuple(right[:3]))
    surf = _GRAD_CACHE.get(key)
    if surf is not None:
        return surf
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    for x in range(w):
        pygame.draw.line(surf, vis_lerp(left, right, x / max(1, w - 1)),
                         (x, 0), (x, h))
    return _cache_put(_GRAD_CACHE, key, surf)


# --------------------------------------------------------------------------
#  Панели и тени
# --------------------------------------------------------------------------

def vis_panel(w, h, radius=14, top=None, bottom=None, border=None,
              gloss=0.55, inner_shadow=True, border_alpha=255):
    """Каменная плита интерфейса: градиент, верхний блик, фаска и кромка."""
    top = top or PAL_PANEL_TOP
    bottom = bottom or PAL_PANEL_BOT
    border = border or PAL_BORDER
    if w <= 2 or h <= 2:
        return pygame.Surface((max(1, w), max(1, h)), pygame.SRCALPHA)
    key = (w, h, radius, tuple(top[:3]), tuple(bottom[:3]), tuple(border[:3]),
           gloss, inner_shadow, border_alpha)
    cached = _PANEL_CACHE.get(key)
    if cached is not None:
        return cached
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    surf.blit(vis_gradient(w, h, top, bottom, radius), (0, 0))

    # Мягкий блик сверху: свет как будто падает с верхнего левого угла.
    if gloss > 0:
        gh = max(3, int(h * 0.48))
        gl = pygame.Surface((w, gh), pygame.SRCALPHA)
        for i in range(gh):
            t = i / max(1, gh - 1)
            a = int(54 * gloss * (1.0 - t) ** 1.8)
            if a > 0:
                pygame.draw.line(gl, (255, 255, 255, a), (0, i), (w, i))
        gl.blit(vis_mask(w, gh, radius), (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        surf.blit(gl, (0, 0))

    # Внутренняя светлая кромка и тень у нижней границы — объём плиты.
    inset = max(0, radius - 2)
    pygame.draw.line(surf, vis_alpha(vis_lerp(border, (255, 255, 255), 0.35), 120),
                     (radius, 1), (w - radius, 1), 1)
    if inner_shadow:
        sh = max(3, int(h * 0.34))
        shd = pygame.Surface((w, sh), pygame.SRCALPHA)
        for i in range(sh):
            t = i / max(1, sh - 1)
            shd.set_at((0, 0), (0, 0, 0, 0))
            pygame.draw.line(shd, (0, 0, 0, int(58 * t ** 1.4)), (0, i), (w, i))
        surf.blit(shd, (0, h - sh))
    if inset:
        pass

    # Кромка: сначала тёмная снаружи, затем светлая внутри.
    pygame.draw.rect(surf, vis_alpha(vis_shade(border, 0.45), 220),
                     (0, 0, w, h), 2, border_radius=radius)
    pygame.draw.rect(surf, vis_alpha(border, border_alpha),
                     (0, 0, w, h), 1, border_radius=radius)
    return _cache_put(_PANEL_CACHE, key, surf)


def vis_shadow(w, h, radius=14, alpha=110, spread=8, dy=0):
    """Мягкая тень под панелью: несколько скруглённых колец с разной альфой."""
    if w <= 0 or h <= 0:
        return pygame.Surface((1, 1), pygame.SRCALPHA)
    key = (w, h, radius, alpha, spread, dy)
    cached = _SHADOW_CACHE.get(key)
    if cached is not None:
        return cached
    pad = spread
    surf = pygame.Surface((w + pad * 2, h + pad * 2 + dy), pygame.SRCALPHA)
    for i in range(spread, 0, -1):
        a = int(alpha * (1.0 - i / (spread + 1)) ** 1.7)
        if a <= 0:
            continue
        rect = pygame.Rect(pad - i, pad - i + dy, w + i * 2, h + i * 2)
        pygame.draw.rect(surf, (0, 0, 0, a), rect, border_radius=radius + i)
    return _cache_put(_SHADOW_CACHE, key, surf)


def vis_draw_shadow(surface, rect, radius=14, alpha=110, spread=8, dy=8):
    """Нарисовать тень под прямоугольником (координаты — как у самой панели)."""
    sh = vis_shadow(rect.w, rect.h, radius, alpha, spread, dy)
    surface.blit(sh, (rect.x - spread, rect.y - spread))


def vis_draw_panel(surface, rect, radius=14, top=None, bottom=None, border=None,
                   gloss=0.55, shadow=110, spread=8, dy=7):
    """Панель с тенью одним вызовом."""
    if shadow:
        vis_draw_shadow(surface, rect, radius, shadow, spread, dy)
    surface.blit(vis_panel(rect.w, rect.h, radius, top, bottom, border, gloss),
                 rect.topleft)


def vis_glass(w, h, radius=12, tint=None, alpha=214):
    """Полупрозрачное «стекло» для подсказок и плашек поверх мира."""
    tint = tint or PAL_GLASS
    key = ("glass", w, h, radius, tuple(tint[:3]), alpha)
    cached = _PANEL_CACHE.get(key)
    if cached is not None:
        return cached
    surf = vis_panel(w, h, radius, vis_lerp(tint, (70, 86, 118), 0.22),
                     tint, vis_lerp(tint, PAL_BORDER, 0.55), gloss=0.5)
    surf.set_alpha(alpha)
    return _cache_put(_PANEL_CACHE, key, surf)


# --------------------------------------------------------------------------
#  Свечение, кольца, виньетка, зерно
# --------------------------------------------------------------------------

def vis_glow(radius, color, alpha=150, steps=14):
    """Радиальное свечение (круг с мягким краем)."""
    radius = max(2, int(radius))
    key = (radius, tuple(color[:3]), alpha, steps)
    cached = _GLOW_CACHE.get(key)
    if cached is not None:
        return cached
    d = radius * 2
    surf = pygame.Surface((d, d), pygame.SRCALPHA)
    for i in range(steps, 0, -1):
        r = max(1, int(radius * i / steps))
        a = int(alpha * (1.0 - i / (steps + 1)) ** 1.9)
        if a <= 0:
            continue
        pygame.draw.circle(surf, (*color[:3], a), (radius, radius), r)
    return _cache_put(_GLOW_CACHE, key, surf)


def vis_ring(w, h, radius, color, width=2, glow=None, glow_alpha=90, glow_pad=6):
    """Кольцо-рамка вокруг прямоугольника, при желании со свечением."""
    key = ("ring", w, h, radius, tuple(color[:3]), width, glow, glow_alpha, glow_pad)
    cached = _PANEL_CACHE.get(key)
    if cached is not None:
        return cached
    pad = glow_pad if glow else 0
    surf = pygame.Surface((w + pad * 2, h + pad * 2), pygame.SRCALPHA)
    if glow:
        for i in range(glow_pad, 0, -1):
            a = int(glow_alpha * (i / glow_pad) ** 1.6)
            pygame.draw.rect(surf, (*glow, a),
                             (pad - i, pad - i, w + i * 2, h + i * 2),
                             border_radius=radius + i, width=2)
    pygame.draw.rect(surf, color, (pad, pad, w, h), width, border_radius=radius)
    return _cache_put(_PANEL_CACHE, key, surf)


def vis_vignette(w, h, strength=1.0, color=(0, 0, 0), inner=0.42):
    """Затемнение по краям кадра.  Считается один раз на размер/силу."""
    key = (w, h, round(strength, 2), tuple(color[:3]), round(inner, 2))
    cached = _VIGNETTE_CACHE.get(key)
    if cached is not None:
        return cached
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    if np is not None and _surfarray is not None:
        xx, yy = np.mgrid[0:w, 0:h].astype(np.float32)
        nx = (xx - (w - 1) * 0.5) / max(1.0, (w - 1) * 0.5)
        ny = (yy - (h - 1) * 0.5) / max(1.0, (h - 1) * 0.5)
        d = np.sqrt(nx * nx + ny * ny) / math.sqrt(2.0)
        k = np.clip((d - inner) / max(1e-5, 1.0 - inner), 0.0, 1.0) ** 1.7
        alpha = (k * 255.0 * strength).astype(np.uint8)
        surf.fill((*color[:3], 0))
        try:
            px = _surfarray.pixels_alpha(surf)
            px[:] = alpha
            del px
        except Exception:
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            rings = 26
            for i in range(rings):
                t = i / (rings - 1)
                a = int(255 * strength * t ** 2.0)
                inset = int((1.0 - t) * min(w, h) * 0.5)
                pygame.draw.rect(surf, (*color[:3], a),
                                 (inset, inset, w - inset * 2, h - inset * 2),
                                 max(2, int(min(w, h) * 0.06)), border_radius=40)
    else:
        rings = 26
        for i in range(rings):
            t = i / (rings - 1)
            a = int(255 * strength * t ** 2.0)
            inset = int((1.0 - t) * min(w, h) * 0.5)
            pygame.draw.rect(surf, (*color[:3], a),
                             (inset, inset, w - inset * 2, h - inset * 2),
                             max(2, int(min(w, h) * 0.06)), border_radius=40)
    return _cache_put(_VIGNETTE_CACHE, key, surf)


def vis_grain(w, h, alpha=10, seed=7):
    """Едва заметное зерно — убирает «пластиковую» гладкость больших заливок."""
    key = (w, h, alpha, seed)
    cached = _GRAIN_CACHE.get(key)
    if cached is not None:
        return cached
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    if np is not None and _surfarray is not None:
        rng = np.random.default_rng(seed)
        noise = rng.integers(0, 256, size=(w, h), dtype=np.uint16)
        a = (noise % 2) * 0 + (noise > 200) * alpha
        surf.fill((255, 255, 255, 0))
        try:
            px = _surfarray.pixels_alpha(surf)
            px[:] = a.astype(np.uint8)
            del px
        except Exception:
            pass
    return _cache_put(_GRAIN_CACHE, key, surf)


# --------------------------------------------------------------------------
#  Текст
# --------------------------------------------------------------------------

def vis_text(font, text, color, shadow=True, outline=None, shadow_alpha=130,
             shadow_off=(1, 2)):
    """Текст с мягкой тенью/обводкой.  Результат кэшируется."""
    if not text:
        return pygame.Surface((1, 1), pygame.SRCALPHA)
    key = (id(font), text, tuple(color[:3]), bool(shadow),
           None if outline is None else tuple(outline[:3]), shadow_alpha, shadow_off)
    cached = _TEXT_CACHE.get(key)
    if cached is not None:
        return cached

    base = font.render(text, True, color)
    if not shadow and outline is None:
        return _cache_put(_TEXT_CACHE, key, base)

    pad = 2
    w = base.get_width() + pad * 2
    h = base.get_height() + pad * 2
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    if shadow:
        sh = font.render(text, True, (0, 0, 0))
        sh.set_alpha(shadow_alpha)
        surf.blit(sh, (pad + shadow_off[0], pad + shadow_off[1]))
    if outline is not None:
        ol = font.render(text, True, outline)
        for ox, oy in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0),
                       (-1, 1), (0, 1), (1, 1)):
            surf.blit(ol, (pad + ox, pad + oy))
    surf.blit(base, (pad, pad))
    return _cache_put(_TEXT_CACHE, key, surf)


def vis_text_at(surface, font, text, pos, color, anchor="topleft",
                shadow=True, outline=None, shadow_alpha=130):
    """Нарисовать текст с тенью; anchor — как у Rect."""
    surf = vis_text(font, text, color, shadow, outline, shadow_alpha)
    pad = 2 if (shadow or outline is not None) else 0
    rect = surf.get_rect(**{anchor: pos})
    surface.blit(surf, (rect.x - pad, rect.y - pad))
    return rect


def vis_gradient_text(font, text, top, bottom, shadow=True, shadow_alpha=150):
    """Текст с вертикальным градиентом — для крупных заголовков."""
    key = (id(font), text, tuple(top[:3]), tuple(bottom[:3]), shadow, shadow_alpha)
    cached = _TEXT_CACHE.get(key)
    if cached is not None:
        return cached
    base = font.render(text, True, (255, 255, 255))
    w, h = base.get_size()
    grad = vis_gradient(w, h, top, bottom)
    layer = grad.copy()
    layer.blit(base, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    pad = 3 if shadow else 0
    surf = pygame.Surface((w + pad * 2, h + pad * 2), pygame.SRCALPHA)
    if shadow:
        sh = font.render(text, True, (0, 0, 0))
        sh.set_alpha(shadow_alpha)
        surf.blit(sh, (pad + 1, pad + 2))
    surf.blit(layer, (pad, pad))
    return _cache_put(_TEXT_CACHE, key, surf)


def vis_gradient_text_at(surface, font, text, pos, top, bottom, anchor="topleft",
                         shadow=True):
    surf = vis_gradient_text(font, text, top, bottom, shadow)
    pad = 3 if shadow else 0
    rect = surf.get_rect(**{anchor: pos})
    surface.blit(surf, (rect.x - pad, rect.y - pad))
    return rect


def vis_text_glow(font, text, color, spread=6, alpha=90):
    """Мягкое свечение вокруг надписи: уменьшенная копия, растянутая обратно."""
    key = ("tglow", id(font), text, tuple(color[:3]), spread, alpha)
    cached = _TEXT_CACHE.get(key)
    if cached is not None:
        return cached
    base = font.render(text, True, color)
    w, h = base.get_size()
    small = pygame.transform.smoothscale(base, (max(1, w // 4), max(1, h // 4)))
    blur = pygame.transform.smoothscale(small, (w + spread * 2, h + spread * 2))
    blur.set_alpha(alpha)
    return _cache_put(_TEXT_CACHE, key, blur)


# --------------------------------------------------------------------------
#  Полоски и мелочи
# --------------------------------------------------------------------------

def vis_bar_fill(w, h, top, bottom, radius=None, gloss=True):
    """Заливка полоски: градиент, блик сверху и мягкая тень снизу."""
    if w <= 0 or h <= 0:
        return pygame.Surface((1, 1), pygame.SRCALPHA)
    radius = h // 2 if radius is None else radius
    key = ("bar", w, h, tuple(top[:3]), tuple(bottom[:3]), radius, gloss)
    cached = _PANEL_CACHE.get(key)
    if cached is not None:
        return cached
    surf = vis_gradient(w, h, top, bottom, radius)
    if gloss and h >= 6:
        g = pygame.Surface((w, max(2, h // 2)), pygame.SRCALPHA)
        for i in range(g.get_height()):
            t = i / max(1, g.get_height() - 1)
            pygame.draw.line(g, (255, 255, 255, int(70 * (1 - t))), (0, i), (w, i))
        g.blit(vis_mask(w, g.get_height(), max(1, radius // 2)), (0, 0),
               special_flags=pygame.BLEND_RGBA_MULT)
        surf.blit(g, (0, 1))
    return _cache_put(_PANEL_CACHE, key, surf)


def vis_dot(surface, center, radius, color, glow=True):
    """Круглый индикатор с бликом (для статусов и имён в сети)."""
    x, y = int(center[0]), int(center[1])
    if glow:
        g = vis_glow(radius + 5, color, 110)
        surface.blit(g, (x - radius - 5, y - radius - 5))
    pygame.draw.circle(surface, vis_shade(color, 0.65), (x, y + 1), radius)
    pygame.draw.circle(surface, color, (x, y), radius)
    pygame.draw.circle(surface, vis_lerp(color, (255, 255, 255), 0.65),
                       (x - max(1, radius // 3), y - max(1, radius // 3)),
                       max(1, radius // 3))


def vis_sparkle(surface, center, size, color=(255, 250, 220), alpha=200):
    """Четырёхлучевой блик — для монет, искр и подсветки."""
    x, y = int(center[0]), int(center[1])
    s = max(2, int(size))
    layer = pygame.Surface((s * 4, s * 4), pygame.SRCALPHA)
    c = s * 2
    pygame.draw.polygon(layer, (*color[:3], alpha // 3),
                        [(c, c - s * 2), (c + s // 2, c), (c, c + s * 2), (c - s // 2, c)])
    pygame.draw.polygon(layer, (*color[:3], alpha // 3),
                        [(c - s * 2, c), (c, c + s // 2), (c + s * 2, c), (c, c - s // 2)])
    pygame.draw.circle(layer, (*color[:3], alpha), (c, c), max(1, s // 2))
    surface.blit(layer, (x - c, y - c))


__all__ = [
    "PAL_INK", "PAL_PANEL_TOP", "PAL_PANEL_BOT", "PAL_BORDER", "PAL_BORDER_HI",
    "PAL_GOLD", "PAL_GOLD_DEEP", "PAL_TEXT", "PAL_MUTED", "PAL_ROW",
    "PAL_ROW_HOVER", "PAL_ROW_SEL", "PAL_OK", "PAL_BAD", "PAL_GLASS", "PAL_WARM",
    "vis_clamp01", "vis_lerp", "vis_shade", "vis_alpha", "vis_mix3",
    "vis_mask", "vis_gradient", "vis_gradient_h",
    "vis_panel", "vis_shadow", "vis_draw_shadow", "vis_draw_panel", "vis_glass",
    "vis_glow", "vis_ring", "vis_vignette", "vis_grain",
    "vis_text", "vis_text_at", "vis_gradient_text", "vis_gradient_text_at",
    "vis_text_glow",
    "vis_bar_fill", "vis_dot", "vis_sparkle",
]
