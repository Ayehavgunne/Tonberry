from typing import Any, Hashable

from _contextvars import ContextVar


class ContextVarManager:
    def __init__(self, name: str):
        object.__setattr__(self, "_context_var", ContextVar(name))

    @property
    def _context(self) -> Any:
        return self._context_var.get()

    def get(self, item: Hashable, default: Any) -> Any:
        return self._context.get(item, default)

    def __getitem__(self, item: Hashable) -> Any:
        return self._context[item]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self._context[key] = value

    def __delitem__(self, key: Hashable) -> None:
        del self._context[key]

    def __setattr__(self, key: str, value: Any) -> None:
        setattr(self._context, key, value)

    def __getattr__(self, item: str) -> Any:
        return getattr(self._context, item)


def set_context_var(context_var_manager: Any, var: Any) -> None:
    # noinspection PyProtectedMember
    context_var_manager._context_var.set(var)
