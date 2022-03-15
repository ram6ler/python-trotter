from .helpers import (
    _adjusted_index,
    _arrangement,
    _n_c_r,
    _items_are_unique,
    _items_exist_in_universal,
    _combination,
    _inverse_combination,
)
from .combinatoric import Combinatoric


class Combinations(Combinatoric):
    """A pseudo-list containing combinations of items.

    A combination is an arrangement in which order is not important and
    repetition is not allowed.
    """

    def __init__(self, r: int, items: list | str):
        self._r = r
        self._items = items
        self._length = _n_c_r(len(items), r)

    def __getitem__(self, k: int | slice) -> list | str:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _combination(
                _adjusted_index(k, self._length),
                self._r,
                self._items,
            )
            return _arrangement(self._items, dummy)

    def __repr__(self):
        return super()._repr("Combinations")

    def __str__(self):
        return super()._str("combinations")

    def __contains__(self, combination: list) -> bool:
        return _items_exist_in_universal(
            combination, self._items
        ) and _items_are_unique(combination)

    def index(self, combination: list) -> int:
        return (
            _inverse_combination(combination, self._items)
            if combination in self
            else -1
        )
