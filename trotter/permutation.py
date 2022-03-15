from .helpers import (
    _adjusted_index,
    _arrangement,
    _n_p_r,
    _items_are_unique,
    _items_exist_in_universal,
    _permutation,
    _inverse_permutation,
)
from .combinatoric import Combinatoric


class Permutations(Combinatoric):
    """A pseudo-list containing permutations of items.

    A permutation is an arrangement in which order is important and
    repetition is not allowed.
    """

    def __init__(self, r: int, items: list | str):
        self._r = r
        self._items = items
        self._length = _n_p_r(len(items), r)

    def __getitem__(self, k: int | slice) -> list | str:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _permutation(
                _adjusted_index(k, self._length),
                self._r,
                self._items,
            )
            return _arrangement(self._items, dummy)

    def __repr__(self):
        return super()._repr("Permutations")

    def __str__(self):
        return super()._str("permutations")

    def __contains__(self, permutation: list) -> bool:
        return _items_exist_in_universal(
            permutation, self._items
        ) and _items_are_unique(permutation)

    def index(self, permutation):
        return (
            _inverse_permutation(permutation, self._items)
            if permutation in self
            else -1
        )
