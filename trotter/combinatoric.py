from .helpers import _adjusted_index, _arrangement


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
