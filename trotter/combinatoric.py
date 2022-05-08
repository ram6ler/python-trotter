from random import randint
from .helpers import _adjusted_index, _arrangement


def _fast_dice_roller(n: int) -> int:
    # Uses Fast Dice Roller algorithm.
    # See Lumbroso, J. (2012)
    #   Optimal Discrete Uniform Generation from Coin Flips, and Applications.
    v, c = 1, 0
    while True:
        v, c = 2 * v, 2 * c + randint(0, 1)
        if v >= n:
            if c < n:
                return c
            else:
                v -= n
                c -= n


class Combinatoric:
    """
    The base class for the combinatorics classes. (Not meant for instantiation, but can be useful for typing and polymorphism.)
    """

    _r: int
    _items: list | str
    _length: int

    def __init__(self):
        raise NotImplementedError()

    def __len__(self):
        return self._length

    def __iter__(self):
        return (self[i] for i in range(self._length))

    def __getitem__(self, k: int | slice) -> list | str:
        raise NotImplementedError()

    def __contains__(self, arrangement: list) -> bool:
        raise NotImplementedError()

    def random(self) -> list | str:
        """A random combinatoric."""
        return self[_fast_dice_roller(self._length)]

    def index(self, arrangement: list) -> int:
        raise NotImplementedError()

    def _str(self, name: str) -> str:
        return _string(self, name)

    def _repr(self, name) -> str:
        return _representation(self, name)

    def _slice(self, s: slice):
        start = 0 if s.start == None else _adjusted_index(s.start, self._length)
        stop = self._length if s.stop == None else _adjusted_index(s.stop, self._length)
        step = 1 if s.step == None else s.step

        return [
            self[_adjusted_index(i, self._length)] for i in range(start, stop, step)
        ]


def _string(combinatoric: Combinatoric, name: str) -> str:
    """A string summary of the Combinatoric."""
    arrangement = _arrangement(combinatoric._items, combinatoric._items)
    return "A pseudo-list containing {} {}-{} of {}.".format(
        combinatoric._length,
        combinatoric._r,
        name,
        f"'{arrangement}'" if isinstance(arrangement, str) else arrangement,
    )


def _representation(combinatoric: Combinatoric, name: str) -> str:
    """A string representation of the Combinatoric."""
    arrangement = _arrangement(
        combinatoric._items,
        combinatoric._items,
    )
    return "{}({}, {})".format(
        name,
        combinatoric._r,
        f"'{arrangement}'" if isinstance(arrangement, str) else arrangement,
    )
