from .helpers import (
    Arrangement,
    fix_type,
    adjusted_index,
    elements_exist_in_universal,
    amalgam,
    inverse_amalgam,
)
from .combinatoric import Combinatoric


class Amalgams(Combinatoric):
    """
    A pseudo-list containing amalgams of elements.

    An amalgam is an arrangement in which order is important and
    repetition is allowed.
    """

    def __init__(self, r: int, elements: Arrangement):
        self._r = r
        self._elements = elements
        self._length = len(elements) ** r

    def __getitem__(self, k: int | slice) -> Arrangement:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = amalgam(
                adjusted_index(k, self._length),
                self._r,
                self._elements,
            )
            return fix_type(self._elements, dummy)

    def __repr__(self):
        return super()._repr("Amalgams")

    def __str__(self):
        return super()._str("amalgams")

    def __contains__(self, amalgam: list) -> bool:
        return elements_exist_in_universal(amalgam, self._elements)

    def index(self, amalgam: list) -> int:
        return (
            inverse_amalgam(
                amalgam,
                self._elements,
            )
            if amalgam in self
            else -1
        )
