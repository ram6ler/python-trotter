from .helpers import (
    _adjusted_index,
    _arrangement,
    _items_exist_in_universal,
    _items_are_unique,
    _subset,
    _inverse_subset,
)
from .combinatoric import Combinatoric


class Subsets(Combinatoric):
    """A pseudo-list containing subsets of items.

    A subset is an arrangement in which order is not important,
    repetition is not allowed and length is not specified.
    """

    def __init__(self, items: list | str):
        self._items = items
        self._length = 1 << len(items)

    def __getitem__(self, k: int | slice) -> list | str:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _subset(_adjusted_index(k, self._length), self._items)
            return _arrangement(self._items, dummy)

    def __repr__(self):
        arrangement = _arrangement(self._items, self._items)
        return "Subsets({})".format(
            f'"{arrangement}' if isinstance(arrangement, str) else arrangement,
        )

    def __str__(self):
        arrangement = _arrangement(self._items, self._items)
        return "List pseudo-list of {} subsets of {}".format(
            self._length,
            f'"{arrangement}"' if isinstance(arrangement, str) else arrangement,
        )

    def __contains__(self, subset: list) -> bool:
        return _items_exist_in_universal(subset, self._items) and _items_are_unique(
            subset
        )

    def index(self, subset: list) -> int:
        return _inverse_subset(subset, self._items) if subset in self else -1
