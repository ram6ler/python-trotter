from .helpers import (
    Arrangement,
    adjusted_index,
    fix_type,
    ncr,
    elements_are_unique,
    elements_exist_in_universal,
    combination,
    inverse_combination,
    raise_if_not_unique,
)
from .combinatoric import Combinatoric


class Combinations(Combinatoric):
    """
    A pseudo-list containing combinations of elements.

    A combination is an arrangement in which order is not important and
    repetition is not allowed.
    """

    def __init__(self, r: int, elements: Arrangement):
        self._r = r
        self._elements = elements
        self._length = ncr(len(elements), r)
        raise_if_not_unique(elements)

    def __getitem__(self, k: int | slice) -> Arrangement:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = combination(
                adjusted_index(k, self._length),
                self._r,
                self._elements,
            )
            return fix_type(self._elements, dummy)

    def __repr__(self):
        return super()._repr("Combinations")

    def __str__(self):
        return super()._str("combinations")

    def __contains__(self, combination: list) -> bool:
        return elements_exist_in_universal(
            combination, self._elements
        ) and elements_are_unique(combination)

    def index(self, combination: list) -> int:
        return (
            inverse_combination(
                combination,
                self._elements,
            )
            if combination in self
            else -1
        )
