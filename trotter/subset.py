from .helpers import (
    Arrangement,
    adjusted_index,
    fix_type,
    elements_exist_in_universal,
    elements_are_unique,
    subset,
    inverse_subset,
)
from .combinatoric import Combinatoric


class Subsets(Combinatoric):
    """
    A pseudo-list containing subsets of elements.

    A subset is an arrangement in which order is not important,
    repetition is not allowed and length is not specified.
    """

    def __init__(self, elements: Arrangement):
        self._elements = elements
        self._length = 1 << len(elements)

    def __getitem__(self, k: int | slice) -> Arrangement:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = subset(adjusted_index(k, self._length), self._elements)
            return fix_type(self._elements, dummy)

    def __repr__(self):
        arrangement = fix_type(self._elements, self._elements)
        return "Subsets({})".format(
            f'"{arrangement}' if isinstance(arrangement, str) else arrangement,
        )

    def __str__(self):
        arrangement = fix_type(self._elements, self._elements)
        return "A pseudo-list containing {} subsets of {}.".format(
            self._length,
            f'"{arrangement}"' if isinstance(arrangement, str) else arrangement,
        )

    def __contains__(self, subset: list) -> bool:
        return elements_exist_in_universal(
            subset, self._elements
        ) and elements_are_unique(subset)

    def index(self, subset: list) -> int:
        return (
            inverse_subset(
                subset,
                self._elements,
            )
            if subset in self
            else -1
        )
