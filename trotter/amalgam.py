from .helpers import (
    _arrangement,
    _adjusted_index,
    _items_exist_in_universal,
    _amalgam,
    _inverse_amalgam,
)
from .combinatoric import Combinatoric


class Amalgams(Combinatoric):
    """A pseudo-list containing amalgams of items.

    An amalgam is an arrangement in which order is important and
    repetition is allowed.
    """

    def __init__(self, r: int, items: list | str):
        self._r = r
        self._items = items
        self._length = len(items) ** r

    def __getitem__(self, k: int | slice) -> list | str:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _amalgam(
                _adjusted_index(k, self._length),
                self._r,
                self._items,
            )
            return _arrangement(self._items, dummy)

    def __repr__(self):
        return super()._repr("Amalgams")

    def __str__(self):
        return super()._str("amalgams")

    def __contains__(self, amalgam: list) -> bool:
        return _items_exist_in_universal(amalgam, self._items)

    def index(self, amalgam: list) -> int:
        return _inverse_amalgam(amalgam, self._items) if amalgam in self else -1
