# -*- coding: utf-8 -*-
"""
Author: Richard Ambler <rambler@wya.top>
Date: January 2015
"""

from typing import List

# Cache to store calculated factorials.
_fact_cache = {2: 2}


def _fact(n: int) -> int:
    """
    `n`! (`n`-factorial)
    """
    if n <= 1:
        return 1
    else:
        if not (n in _fact_cache.keys()):
            _fact_cache[n] = n * _fact(n - 1)
        return _fact_cache[n]


def _n_p_r(n: int, r: int) -> int:
    """
    The number of permutations of `r` items taken from `n`.
    """
    return _fact(n) // _fact(n - r)


def _n_c_r(n: int, r: int) -> int:
    """
    The number of combinations of `r` items taken from `n`.
    """
    return _n_p_r(n, r) // _fact(r)


def _sorted_arrangement(arrangement: List, items: List) -> List:
    """
    The items in `arrangement` in the same order as they appear in `items`.
    """
    return sorted(arrangement, key=lambda item: items.index(item))


def _items_are_unique(items: List) -> bool:
    """
    Whether the items in `items` are unique.
    """
    return len(set(items)) == len(items)


def _items_exist_in_universal(items, universal):
    """
    Whether all items in `items` are in `universal`.
    """
    return all(item in universal for item in items)


def _permutation_worker(k: int, items: List) -> List:
    """
    The `k`th Johnson-Trotter permutation of all items.
    """
    n = len(items)
    if n <= 1:
        return items
    else:
        group = k // n
        item = k % n
        position = n - item - 1 if group % 2 == 0 else item
        dummy = _permutation_worker(group, items[0:(n - 1)])
        dummy.insert(position, items[n - 1])
        return dummy


def _inverse_permutation_worker(permutation: List, items: List) -> int:
    """
    The index of `permutation` in the list of permutations of items in `items`.
    """
    if len(permutation) == 1:
        return 0
    else:
        n = len(items)
        index = permutation.index(items[-1])
        group = _inverse_permutation_worker(
            [x for x in permutation if x != items[-1]],
            items[0:(-1)]
        )
        return n * group + (n - index - 1 if group % 2 == 0 else index)


def _combination(k: int, r: int, items: List) -> List:
    """
    The `k`th combination of `r` items taken from items.
    """
    n = len(items)
    position = 0
    d = _n_c_r(n - position - 1, r - 1)

    while k >= d:
        k -= d
        position += 1
        d = _n_c_r(n - position - 1, r - 1)

    if r == 0:
        return []
    else:
        tail = items[(position + 1):]
        dummy = [items[position]]
        dummy.extend(_combination(k, r - 1, tail))
        return dummy


def _inverse_combination(combination: List, items: List) -> int:
    """
    The index of `combination` in the ordered combinations of items in `items`.
    """
    def helper(combination, items):
        if len(combination) == 0:
            return 0
        else:
            k = 0
            r = len(combination)
            n = len(items)
            item_index = 0
            while combination[0] != items[item_index]:
                k += _n_c_r(n - item_index - 1, r - 1)
                item_index += 1
            return k + helper(combination[1:], items[(item_index + 1):])
    return helper(_sorted_arrangement(combination, items), items)


def _composition(k: int, r: int, items: List):
    """
    The `k`th selection of `r` items taken from `items`.
    """
    n = len(items)
    position = 0
    d = _n_c_r(n + r - position - 2, r - 1)

    while k >= d:
        k -= d
        position += 1
        d = _n_c_r(n + r - position - 2, r - 1)

    if r == 0:
        return []
    else:
        tail = items[position:]
        dummy = [items[position]]
        dummy.extend(_composition(k, r - 1, tail))
        return dummy


def _inverse_composition(composition: List, items: List) -> int:
    """
    The index of `composition` in the ordered compositions of items in `items`.
    """
    def helper(composition, items):
        if len(composition) == 0:
            return 0
        else:
            k = 0
            n = len(items)
            r = len(composition)
            item_index = 0
            while (composition[0] != items[item_index]):
                k += _n_c_r(n + r - item_index - 2, r - 1)
                item_index += 1
            return k + helper(composition[1:], items[item_index:])
    return helper(_sorted_arrangement(composition, items), items)


def _permutation(k: int, r: int, items: List) -> List:
    """
    The `k`th permutation of `r` items taken from `items`.
    """
    f = _fact(r)
    group = k // f
    item = k % f
    comb = _combination(group, r, items)
    return _permutation_worker(item, comb)


def _inverse_permutation(permutation: List, items: List) -> int:
    """
    The index of `permutation` in the ordered permutations of items in `items`.
    """
    r = len(permutation)
    if r == 0:
        return 0
    else:
        sorted_permutation = _sorted_arrangement(permutation, items)
        group = _inverse_combination(sorted_permutation, items)
        return group * _fact(r) + _inverse_permutation_worker(permutation, sorted_permutation)


def _amalgam(k: int, r: int, items: List) -> List:
    """
    The `k`th permutation of `r` items taken from `items`.
    """
    def element(i):
        nonlocal k
        p = len(items) ** (r - i - 1)
        index = k // p
        k %= p
        return items[index]
    return [element(i) for i in range(r)]


def _inverse_amalgam(amalgam: List, items: List) -> int:
    """
    The index of `amalgam` in the ordered amalgams of items in `items`.
    """
    r = len(amalgam)
    n = len(items)
    powers = [n ** i for i in range(r)]
    return sum([items.index(amalgam[position]) * powers[r - position - 1] for position in range(r)])


def _subset(k: int, items: List) -> List:
    """
    The `k`th subset of items taken from `items`.
    """
    return [items[i] for i in [j for j in range(len(items)) if k & (1 << j) != 0]]


def _inverse_subset(subset: List, items: List) -> int:
    """
    The index of `subset` in the ordered subsets of items in `items`.
    """
    def helper(subset, items):
        k = 0
        n = len(items)
        power = 1
        for index in range(n):
            if items[index] in subset:
                k += power
            power *= 2
        return k
    return helper(_sorted_arrangement(list(set(subset)), items), items)


def _compound(k: int, items: List) -> List:
    """
    The `k`th compound of items taken from `items`.
    """
    n = len(items)
    for r in range(n):
        groupSize = _n_p_r(n, r)
        if k >= groupSize:
            k -= groupSize
        else:
            break
    else:
        r += 1
    return _permutation(k, r, items)


def _inverse_compound(compound, items):
    """
    The index of `compound` in the ordered compounds of items in `items`.
    """
    n = len(items)
    k = sum([_n_p_r(n, r) for r in range(len(compound))])
    return (k + _inverse_permutation(compound, items))


def _adjustedIndex(k: int, n: int) -> int:
    """
    The index `k` mod `n` (to allow for wraparound).
    """
    return k % n


def _arrangement(items: List, arrangement: List) -> List:
    """
    A representation of an `arrangement` based on the type of the `items`.
    """
    return "".join(arrangement) if isinstance(items, str) else arrangement


def _string(combinatoric, name: str) -> str:
    """
    A string summary of a `combinatoric`.
    """
    return "A pseudo-list containing {} {}-{} of {}.".format(
           combinatoric._length,
           combinatoric._r,
           name,
           _arrangement(combinatoric._items, combinatoric._items)
    )


def _representation(combinatoric, name: str) -> str:
    """
    A string representation of a `combinatoric`.
    """
    return "{}({}, {})".format(
        name,
        combinatoric._r,
        _arrangement(combinatoric._items, combinatoric._items)
    )


class _Combinatoric:
    """
    The base class for the combinatorics classes.
    (Not meant for instantiation.)
    """

    def __init__(self):
        self._r: int
        self._items: List
        self._length: int

    def __len__(self):
        return self._length

    def __iter__(self):
        return (self[i] for i in range(self._length))

    def __getitem__(self, k: int):
        pass

    def __contains__(self, amalgam: List) -> bool:
        pass

    def index(self, arrangement: List) -> int:
        pass

    def _str(self, name: str) -> str:
        return _string(self, name)

    def _repr(self, name) -> str:
        return _representation(self, name)

    def _slice(self, s):
        start = 0 if s.start == None else s.start
        stop = self._length if s.stop == None else s.stop
        step = 1 if s.step == None else s.step
        if step > 0:
            while stop < start:
                stop += self._length
        if step < 0:
            while stop > start:
                stop -= self._length
        return [
            self[_adjustedIndex(i, self._length)]
            for i in range(start, stop, step)
        ]


class Amalgams(_Combinatoric):
    """A pseudo-list containing amalgrams of objects.

    The term *amalgam* is used to refer to an arrangement of items such that
    order is important and replacement is allowed.

    An instance of `Amalgams` is a pseudo-list in that it does not actually
    store the arrangements but rather presents a mapping as an indexable list.

    Args:
      r (int): The number of items to take.
      items: An indexable object containing the items to be arranged.
        If `items` is a string, the individual characters will be arranged.

    Example:

      >>> a = Amalgams(3, 'abcde')
      >>> len(a)
      125
      >>> a[0:10]

      ['aaa', 'aab', 'aac', 'aad', 'aae', 'aba', 'abb', 'abc', 'abd', 'abe']

    """

    def __init__(self, r: int, items: List):
        self._r = r
        self._items = items
        self._length = len(items) ** r

    def __getitem__(self, k: int) -> List:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _amalgam(
                _adjustedIndex(k, self._length),
                self._r,
                self._items
            )
            return _arrangement(self._items, dummy)

    def __repr__(self):
        return super()._repr("Amalgams")

    def __str__(self):
        return super()._str("amalgams")

    def __contains__(self, amalgam: List) -> bool:
        return _items_exist_in_universal(amalgam, self._items)

    def index(self, amalgam: List) -> int:
        return _inverse_amalgam(amalgam, self._items) if amalgam in self else -1


class Combinations(_Combinatoric):
    """A pseudo-list containing combinations of objects.

    The term *combination* is used to refer to an arrangement of items such that
    order is not important and replacement is not allowed.

    An instance of `Combinations` is a pseudo-list in that it does not actually
    store the arrangements but rather presents a mapping as an indexable list.

    Args:
      r (int): The number of items to take.
      items: An indexable object containing the items to be arranged.
        If `items` is a string, the individual characters will be arranged.

    Example:

      >>> c = Combinations(3, "abcde")
      >>> len(c)
      10
      >>> c[0:]

      ['abc', 'abd', 'abe', 'acd', 'ace', 'ade', 'bcd', 'bce', 'bde', 'cde']

    """

    def __init__(self, r: int, items: List):
        self._r = r
        self._items = items
        self._length = _n_c_r(len(items), r)

    def __getitem__(self, k: int) -> List:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _combination(
                _adjustedIndex(k, self._length),
                self._r,
                self._items
            )
            return _arrangement(self._items, dummy)

    def __repr__(self):
        return super()._repr("Combinations")

    def __str__(self):
        return super()._str("combinations")

    def __contains__(self, combination: List) -> bool:
        return _items_exist_in_universal(combination, self._items) and _items_are_unique(combination)

    def index(self, combination: List) -> int:
        return _inverse_combination(combination, self._items) if combination in self else -1


class Permutations(_Combinatoric):
    """A pseudo-list containing permutations of objects.

    The term *permutation* is used to refer to an arrangement of items such that
    order is important and replacement is not allowed.

    An instance of `Permutations` is a pseudo-list in that it does not actually
    store the arrangements but rather presents a mapping as an indexable list.

    Args:
      r (int): The number of items to take.
      items: An indexable object containing the items to be arranged.
        If `items` is a string, the individual characters will be arranged.

    Example:

      >>> p = Permutations(3, "abcde")
      >>> len(p)
      60
      >>> p[0:10]

      ['abc', 'acb', 'cab', 'cba', 'bca', 'bac', 'abd', 'adb', 'dab', 'dba']

    """

    def __init__(self, r: int, items: List):
        self._r = r
        self._items = items
        self._length = _n_p_r(len(items), r)

    def __getitem__(self, k: int) -> List:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _permutation(
                _adjustedIndex(k, self._length),
                self._r,
                self._items
            )
            return _arrangement(self._items, dummy)

    def __repr__(self):
        return super()._repr("Permutations")

    def __str__(self):
        return super()._str("permutations")

    def __contains__(self, permutation: List) -> bool:
        return _items_exist_in_universal(permutation, self._items) and _items_are_unique(permutation)

    def index(self, permutation):
        return _inverse_permutation(permutation, self._items) if permutation in self else -1


class Compositions(_Combinatoric):
    """A pseudo-list containing compositions of objects.

    The term *composition* is used to refer to an arrangement of items such that
    order is not important and replacement is allowed.

    An instance of `Compositions` is a pseudo-list in that it does not actually
    store the arrangements but rather presents a mapping as an indexable list.

    Args:
      r (int): The number of items to take.
      items: An indexable object containing the items to be arranged.
        If `items` is a string, the individual characters will be arranged.

    Example:

      >>> s = Compositions(3, "abcde")
      >>> len(s)
      35
      >>> s[0:10]

      ['aaa', 'aab', 'aac', 'aad', 'aae', 'abb', 'abc', 'abd', 'abe', 'acc']

    """

    def __init__(self, r: int, items: List):
        self._r = r
        self._items = items
        self._length = _n_c_r(len(items) + r - 1, r)

    def __getitem__(self, k: int) -> List:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _composition(
                _adjustedIndex(k, self._length),
                self._r,
                self._items
            )
            return _arrangement(self._items, dummy)

    def __repr__(self):
        return super()._repr("Compositions")

    def __str__(self):
        return super()._str("selections")

    def __contains__(self, selection: List) -> bool:
        return _items_exist_in_universal(selection, self._items)

    def index(self, selection: List) -> int:
        return _inverse_composition(selection, self._items) if selection in self else -1


class Subsets(_Combinatoric):
    """A pseudo-list containing subsets of objects.

    An instance of `Subsets` is a pseudo-list in that it does not actually
    store the subsets but rather presents a mapping as an indexable list.

    Args:
      items: An indexable object containing the items to be arranged.
        If `items` is a string, the individual characters will be arranged.

    Example:

      >>> ss = Subsets("abcde")
      >>> len(ss)
      32
      >>> ss[0:10]

      ['', 'a', 'b', 'ab', 'c', 'ac', 'bc', 'abc', 'd', 'ad']

    """

    def __init__(self, items: List):
        self._items = items
        self._length = 1 << len(items)

    def __getitem__(self, k: int) -> List:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _subset(
                _adjustedIndex(k, self._length),
                self._items
            )
            return _arrangement(self._items, dummy)

    def __repr__(self):
        return "Subsets({})".format(
            _arrangement(self._items, self._items))

    def __str__(self):
        return "List pseudo-list of {} subsets of {}".format(
            self._length,
            '"{}"'.format(self._items)
            if isinstance(self._items, str)
            else self._items
        )

    def __contains__(self, subset: List) -> bool:
        return _items_exist_in_universal(subset, self._items) and _items_are_unique(subset)

    def index(self, subset: List) -> int:
        return _inverse_subset(subset, self._items) if subset in self else -1


class Compounds(_Combinatoric):
    """A pseudo-list containing compounds (permutations of unspecified length) of objects.

    An instance of `Compounds` is a pseudo-list in that it does not actually
    store the compounds but rather presents a mapping as an indexable list.

    Args:
      items: An indexable object containing the items to be arranged.
        If `items` is a string, the individual characters will be arranged.

    Example:

      >>> cp = Compounds("abcde")
      >>> len(cp)
      326
      >>> cp[0:10]
      ['', 'a', 'b', 'c', 'd', 'e', 'ab', 'ba', 'ac', 'ca']

    """

    def __init__(self, items: List):
        n = len(items)
        self._items = items
        self._length = sum([_n_p_r(n, r) for r in range(n + 1)])

    def __getitem__(self, k: int) -> List:
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _compound(
                _adjustedIndex(k, self._length),
                self._items
            )
            return _arrangement(self._items, dummy)

    def __repr__(self):
        return "Compounds({})".format(
            _arrangement(self._items, self._items))

    def __str__(self):
        return "List pseudo-list of {} compounds of {}".format(
            self._length,
            '"{}"'.format(self._items)
            if isinstance(self._items, str)
            else self._items
        )

    def __contains__(self, compound: List) -> bool:
        return _items_exist_in_universal(compound, self._items) and _items_are_unique(compound)

    def index(self, compound: List) -> int:
        return _inverse_compound(compound, self._items) if compound in self else -1


def test():
    #items = ["a", "b", "c", "d"]
    items = "abcd"
    n = len(items)

    def inverse_test(combinatoric):
        print("combinatoric:", combinatoric)
        print("type:", type(combinatoric))
        for i in range(len(combinatoric)):
            arrangement = combinatoric[i]
            index = combinatoric.index(arrangement)
            print("{}.\t{}\t... {}".format(i, arrangement, index))

    print("\n\nCheck 1 - inverse permutations")
    inverse_test(Permutations(n, items))

    print("\n\nCheck 2 - inverse combinations")
    inverse_test(Combinations(n, items))

    print("\n\nCheck 3 - inverse compositions")
    inverse_test(Compositions(n, items))

    print("\n\nCheck 4 - inverse amalgams")
    inverse_test(Amalgams(n, items))

    print("\n\nCheck 5 - inverse subsets")
    inverse_test(Subsets(items))

    print("\n\nCheck 6 - inverse compounds")
    inverse_test(Compounds(items))
