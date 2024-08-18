from .helpers import (
    Arrangement,
    adjusted_index,
    fix_type,
    elements_exist_in_universal,
    elements_are_unique,
    npr,
    compound,
    inverse_compound,
    raise_if_not_unique,
)

from .combinatoric import Combinatoric


class Compounds(Combinatoric):
    """
    A pseudo-list containing compounds of elements.

    A compound is an arrangement in which order is important,
    repetition is not allowed, and length is not specified.
    """

    def __init__(self, elements: Arrangement):
        n = len(elements)
        self._elements = elements
        self._length = sum([npr(n, r) for r in range(n + 1)])
        raise_if_not_unique(elements)

    def __getitem__(self, k: int | slice) -> Arrangement:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = compound(adjusted_index(k, self._length), self._elements)
            return fix_type(self._elements, dummy)

    def __repr__(self):
        arrangement = fix_type(self._elements, self._elements)
        return "Compounds({})".format(
            f'"{arrangement}"' if isinstance(arrangement, str) else arrangement
        )

    def __str__(self):
        arrangement = fix_type(self._elements, self._elements)
        return "A pseudo-list containing {} compounds of {}.".format(
            self._length,
            '"{}"'.format(arrangement) if isinstance(arrangement, str) else arrangement,
        )

    def __contains__(self, compound: list) -> bool:
        return elements_exist_in_universal(
            compound, self._elements
        ) and elements_are_unique(compound)

    def index(self, compound: list) -> int:
        return (
            inverse_compound(
                compound,
                self._elements,
            )
            if compound in self
            else -1
        )
