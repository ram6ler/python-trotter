from functools import wraps
from typing import Callable


def _cached(f: Callable[[int], int]) -> Callable[[int], int]:
    cache = dict[int, int]()

    @wraps(f)
    def wrapper(n: int) -> int:
        if n not in cache:
            cache[n] = f(n)
        return cache[n]

    return wrapper


@_cached
def _fact(n: int) -> int:
    """n!"""
    if n <= 1:
        return 1
    return n * _fact(n - 1)


def _n_p_r(n: int, r: int) -> int:
    """Permutations count of r items taken from n."""
    return _fact(n) // _fact(n - r)


def _n_c_r(n: int, r: int) -> int:
    """Combinations count of r items taken from n."""
    return _n_p_r(n, r) // _fact(r)


def _sorted_arrangement(arrangement: list, items: list | str) -> list:
    """Elements of arrangement ordered as they appear in items."""
    return sorted(
        arrangement,
        key=lambda item: items.index(item),
    )


def _items_are_unique(items: list) -> bool:
    """Whether elements in items are unique."""
    return len(set(items)) == len(items)


def _items_exist_in_universal(items: list, universal: list | str) -> bool:
    """Whether elements in items are in universal."""
    return all(item in universal for item in items)


def _arrangement(items: list | str, arrangement: list | str) -> list | str:
    """A representation of arrangement based on the type of the items."""
    return "".join(arrangement) if isinstance(items, str) else arrangement


def _permutation_worker(k: int, items: list) -> list:
    """The kth Johnson-Trotter permutation of all items."""
    n = len(items)
    if n <= 1:
        return items
    else:
        group = k // n
        item = k % n
        position = n - item - 1 if group % 2 == 0 else item
        dummy = _permutation_worker(group, items[0 : (n - 1)])
        dummy.insert(position, items[n - 1])
        return dummy


def _inverse_permutation_worker(permutation: list, items: list) -> int:
    """
    The index of permutation in the Johnson-Trotter list of
    permutations of elements in items.
    """
    if len(permutation) == 1:
        return 0
    else:
        n = len(items)
        index = permutation.index(items[-1])
        group = _inverse_permutation_worker(
            [x for x in permutation if x != items[-1]],
            items[0:(-1)],
        )
        return n * group + (n - index - 1 if group % 2 == 0 else index)


def _amalgam(k: int, r: int, items: list | str) -> list:
    """The kth permutation of r items taken from items."""

    def element(i):
        nonlocal k
        p = len(items) ** (r - i - 1)
        index = k // p
        k %= p
        return items[index]

    return [element(i) for i in range(r)]


def _inverse_amalgam(amalgam: list, items: list | str) -> int:
    """
    The index of amalgam in the ordered amalgams of
    elements in items.
    """
    r = len(amalgam)
    n = len(items)
    powers = [n ** i for i in range(r)]
    return sum(
        [
            items.index(amalgam[position]) * powers[r - position - 1]
            for position in range(r)
        ]
    )


def _combination(k: int, r: int, items: list | str) -> list:
    """The kth combination of r elements taken from items."""
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
        tail = items[(position + 1) :]
        dummy = [items[position]]
        dummy.extend(_combination(k, r - 1, tail))
        return dummy


def _inverse_combination(combination: list, items: list | str) -> int:
    """
    The index of combination in the ordered combinations of
    elements in items.
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
            return k + helper(combination[1:], items[(item_index + 1) :])

    return helper(
        _sorted_arrangement(combination, items),
        items,
    )


def _permutation(k: int, r: int, items: list | str) -> list:
    """The kth permutation of r elements taken from items."""
    f = _fact(r)
    group = k // f
    item = k % f
    comb = _combination(group, r, items)
    return _permutation_worker(item, comb)


def _inverse_permutation(permutation: list, items: list | str) -> int:
    """
    The index of permutation in the ordered permutations of
    elements in `items`.
    """
    r = len(permutation)
    if r == 0:
        return 0
    else:
        sorted_permutation = _sorted_arrangement(permutation, items)
        group = _inverse_combination(sorted_permutation, items)
        return group * _fact(r) + _inverse_permutation_worker(
            permutation, sorted_permutation
        )


def _composition(k: int, r: int, items: list | str):
    """The kth selection of r elements taken from items."""
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


def _inverse_composition(composition: list, items: list | str) -> int:
    """
    The index of composition in the ordered compositions of
    elements in `items`.
    """

    def helper(composition, items):
        if len(composition) == 0:
            return 0
        else:
            k = 0
            n = len(items)
            r = len(composition)
            item_index = 0
            while composition[0] != items[item_index]:
                k += _n_c_r(n + r - item_index - 2, r - 1)
                item_index += 1
            return k + helper(composition[1:], items[item_index:])

    return helper(_sorted_arrangement(composition, items), items)


def _subset(k: int, items: list | str) -> list:
    """The kth subset of elements taken from items."""
    return [items[i] for i in [j for j in range(len(items)) if k & (1 << j) != 0]]


def _inverse_subset(subset: list, items: list | str) -> int:
    """
    The index of subset in the ordered subsets of
    elements in items.
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

    return helper(
        _sorted_arrangement(list(set(subset)), items),
        items,
    )


def _compound(k: int, items: list | str) -> list:
    """The kth compound of elements taken from items."""
    n = len(items)
    for r in range(n):
        group_size = _n_p_r(n, r)
        if k >= group_size:
            k -= group_size
        else:
            break
    else:
        r += 1
    return _permutation(k, r, items)


def _inverse_compound(compound, items):
    """
    The index of compound in the ordered compounds of
    elements in items.
    """
    n = len(items)
    k = sum([_n_p_r(n, r) for r in range(len(compound))])
    return k + _inverse_permutation(compound, items)


def _adjusted_index(k: int, n: int) -> int:
    """Index `k` mod `n` (for wraparound)."""
    return k % n
