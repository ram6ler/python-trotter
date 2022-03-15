from .helpers import (
    _adjusted_index,
    _arrangement,
    _items_exist_in_universal,
    _items_are_unique,
    _n_p_r,
    _compound,
    _inverse_compound,
)

from .combinatoric import Combinatoric


class Compounds(Combinatoric):
    """A pseudo-list containing compounds of items.

    A compound is an arrangement in which order is important,
    repetition is not allowed, and length is not specified.
    """

    def __init__(self, items: list | str):
        n = len(items)
        self._items = items
        self._length = sum([_n_p_r(n, r) for r in range(n + 1)])

    def __getitem__(self, k: int | slice) -> list | str:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _compound(_adjusted_index(k, self._length), self._items)
            return _arrangement(self._items, dummy)

    def __repr__(self):
        arrangement = _arrangement(self._items, self._items)
        return "Compounds({})".format(
            f'"{arrangement}"' if isinstance(arrangement, str) else arrangement
        )

    def __str__(self):
        arrangement = _arrangement(self._items, self._items)
        return "List pseudo-list of {} compounds of {}".format(
            self._length,
            '"{}"'.format(arrangement) if isinstance(arrangement, str) else arrangement,
        )

    def __contains__(self, compound: list) -> bool:
        return _items_exist_in_universal(compound, self._items) and _items_are_unique(
            compound
        )

    def index(self, compound: list) -> int:
        return _inverse_compound(compound, self._items) if compound in self else -1
