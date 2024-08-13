from .helpers import (
    Arrangement,
    adjusted_index,
    fix_type,
    elements_exist_in_universal,
    ncr,
    composition,
    inverse_composition,
)

from .combinatoric import Combinatoric


class Compositions(Combinatoric):
    """
    A pseudo-list containing compositions of elements.

    A composition is an arrangement in which order is not important and
    repetition is allowed.
    """

    def __init__(self, r: int, elements: Arrangement):
        self._r = r
        self._elements = elements
        self._length = ncr(len(elements) + r - 1, r)

    def __getitem__(self, k: int | slice) -> Arrangement:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = composition(
                adjusted_index(k, self._length),
                self._r,
                self._elements,
            )
            return fix_type(self._elements, dummy)

    def __repr__(self):
        return super()._repr("Compositions")

    def __str__(self):
        return super()._str("compositions")

    def __contains__(self, selection: list) -> bool:
        return elements_exist_in_universal(selection, self._elements)

    def index(self, selection: list) -> int:
        return (
            inverse_composition(
                selection,
                self._elements,
            )
            if selection in self
            else -1
        )
