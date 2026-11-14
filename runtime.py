"""Общее пространство имён игры, собранное из частей.

Игра выросла из одного файла и до сих пор держит сотни общих переменных:
мир, игрока, камеру, инвентарь, шрифты, открытые меню.  Чтобы разложить
её по файлам, не переписывая каждое обращение к этим переменным, части
выполняются в пространстве имён этого модуля — для них это по-прежнему
один общий модуль, а для читателя это отдельные файлы по темам.

Порядок частей важен: объявления классов и модульные значения выполняются
сверху вниз, как в исходном файле.
"""

import os as _rt_os

from . import config as _rt_config
from . import visual as _rt_visual
from .netcode import _UdpNet  # noqa: F401  (нужен частям игры)

_RT_PARTS_DIR = _rt_os.path.join(
    _rt_os.path.dirname(_rt_os.path.abspath(__file__)), "parts")

_RT_PARTS = (
    "00_bootstrap.py",
    "10_graphics.py",
    "12_detail_style.py",
    "20_audio.py",
    "30_ui_widgets.py",
    "32_worldgen.py",
    "34_world_objects.py",
    "36_effects.py",
    "40_entities.py",
    "42_nature.py",
    "46_player.py",
    "50_mp_protocol.py",
    "54_multiplayer.py",
    "56_game_state.py",
    "60_inventory_ui.py",
    "62_placement.py",
    "64_build_actions.py",
    "66_debug.py",
    "70_item_icons.py",
    "72_inventory_draw.py",
    "74_panels.py",
    "78_collisions.py",
    "80_world_events.py",
    "82_actions.py",
    "84_flow.py",
    "85_save.py",
    "86_hud.py",
    "90_loop.py",
)

_RT_LOADED = False


def _rt_load():
    """Выполнить все части в пространстве имён этого модуля."""
    global _RT_LOADED
    if _RT_LOADED:
        return
    # Флаг ставим заранее: если часть импортирует `surv.runtime`,
    # рекурсии не будет.
    _RT_LOADED = True
    namespace = globals()
    for key, value in vars(_rt_config).items():
        if not key.startswith("__"):
            namespace[key] = value
    for key in _rt_visual.__all__:
        namespace[key] = getattr(_rt_visual, key)
    for name in _RT_PARTS:
        path = _rt_os.path.join(_RT_PARTS_DIR, name)
        with open(path, encoding="utf-8") as fh:
            source = fh.read()
        exec(compile(source, path, "exec"), namespace)


_rt_load()
