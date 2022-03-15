from .helpers import (
    _adjusted_index,
    _arrangement,
    _items_exist_in_universal,
    _n_c_r,
    _composition,
    _inverse_composition,
)

from .combinatoric import Combinatoric


class Compositions(Combinatoric):
    """A pseudo-list containing compositions of items.

    A composition is an arrangement in which order is not important and
    repetition is allowed.
    """

    def __init__(self, r: int, items: list | str):
        self._r = r
        self._items = items
        self._length = _n_c_r(len(items) + r - 1, r)

    def __getitem__(self, k: int | slice) -> list | str:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _composition(
                _adjusted_index(k, self._length),
                self._r,
                self._items,
            )
            return _arrangement(self._items, dummy)

    def __repr__(self):
        return super()._repr("Compositions")

    def __str__(self):
        return super()._str("compositions")

    def __contains__(self, selection: list) -> bool:
        return _items_exist_in_universal(selection, self._items)

    def index(self, selection: list) -> int:
        return _inverse_composition(selection, self._items) if selection in self else -1
