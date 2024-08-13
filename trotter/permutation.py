from .helpers import (
    Arrangement,
    adjusted_index,
    fix_type,
    npr,
    elements_are_unique,
    elements_exist_in_universal,
    permutation,
    inverse_permutation,
)
from .combinatoric import Combinatoric


class Permutations(Combinatoric):
    """
    A pseudo-list containing permutations of elements.

    A permutation is an arrangement in which order is important and
    repetition is not allowed.
    """

    def __init__(self, r: int, elements: Arrangement):
        self._r = r
        self._elements = elements
        self._length = npr(len(elements), r)

    def __getitem__(self, k: int | slice) -> Arrangement:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = permutation(
                adjusted_index(k, self._length),
                self._r,
                self._elements,
            )
            return fix_type(self._elements, dummy)

    def __repr__(self):
        return super()._repr("Permutations")

    def __str__(self):
        return super()._str("permutations")

    def __contains__(self, permutation: list) -> bool:
        return elements_exist_in_universal(
            permutation, self._elements
        ) and elements_are_unique(permutation)

    def index(self, permutation):
        return (
            inverse_permutation(
                permutation,
                self._elements,
            )
            if permutation in self
            else -1
        )
