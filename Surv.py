"""Совместимый вход в игру: `python Surv.py`.

Сама игра теперь живёт в пакете `surv` (см. `surv/README.md` и
`surv/runtime.py`).  Этот файл оставлен для старых команд и скриптов:
`import Surv` по-прежнему видит все имена игры, а запись в них попадает
в общий мир, а не в копию.
"""

import sys
import types

from surv import runtime as _runtime


class _GameFacade(types.ModuleType):
    """Модуль-окно: чтение и запись идут в `surv.runtime`."""

    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)
        return getattr(_runtime, name)

    def __setattr__(self, name, value):
        if name.startswith("__"):
            super().__setattr__(name, value)
        else:
            setattr(_runtime, name, value)

    def __dir__(self):
        return sorted(set(super().__dir__()) | set(vars(_runtime)))


sys.modules[__name__].__class__ = _GameFacade


if __name__ == "__main__":
    _runtime.main()
