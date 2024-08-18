from functools import wraps
from typing import Callable

type Arrangement = list | str


class TrotterException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"* Trotter Exception: {self.message}"


def cached(f: Callable[[int], int]) -> Callable[[int], int]:
    cache = dict[int, int]()

    @wraps(f)
    def wrapper(n: int) -> int:
        if n not in cache:
            cache[n] = f(n)
        return cache[n]

    return wrapper


@cached
def fact(n: int) -> int:
    """
    n!
    """
    if n <= 1:
        return 1
    return n * fact(n - 1)


def npr(n: int, r: int) -> int:
    """
    Permutations count of r elements taken from n.
    """
    return fact(n) // fact(n - r)


def ncr(n: int, r: int) -> int:
    """
    Combinations count of r elements taken from n.
    """
    return npr(n, r) // fact(r)


def sorted_elements(arrangement: list, elements: Arrangement) -> list:
    """
    Elements of `arrangement` ordered as they appear in `elements`.
    """
    return sorted(
        arrangement,
        key=lambda element: elements.index(element),
    )


def elements_are_unique(elements: list) -> bool:
    """
    Whether elements in `elements` are unique.
    """
    return len(set(elements)) == len(elements)


def raise_if_not_unique(elements: Arrangement) -> None:
    if not elements_are_unique(elements):
        raise TrotterException(f"Elements {", ".join(elements)} expected to be unique.")


def elements_exist_in_universal(elements: list, universal: Arrangement) -> bool:
    """
    Whether elements in `elements` are in universal.
    """
    return all(element in universal for element in elements)


def fix_type(elements: Arrangement, arrangement: Arrangement) -> Arrangement:
    """
    A representation of `arrangement` based on the type of the `elements`.
    """
    return (
        "".join(arrangement)
        if isinstance(elements, str)
        else [element for element in arrangement]
    )


def total_permutation(global_index: int, first_permutation: list) -> list:
    """
    The permutation at position `global_index` relative to `first_permutation`.
    """
    n = len(first_permutation)
    if n <= 1:
        return first_permutation
    else:
        partition_index = global_index // n
        local_index = global_index % n
        position = n - local_index - 1 if partition_index % 2 == 0 else local_index
        *background_elements, pivot_element = first_permutation
        background_permutation = total_permutation(
            partition_index,
            background_elements,
        )
        return [
            *background_permutation[:position],
            pivot_element,
            *background_permutation[position:],
        ]


def inverse_total_permutation(permutation: list, elements: list) -> int:
    """
    The index of `permutation` in the Johnson-Trotter list of
    permutations of the elements in `elements`.
    """
    if len(permutation) == 0:
        return 0
    else:
        n = len(elements)
        *background_elements, pivot_element = elements
        position = permutation.index(pivot_element)
        partition_index = inverse_total_permutation(
            [x for x in permutation if x != pivot_element],
            background_elements,
        )
        local_index = n - 1 - position if partition_index % 2 == 0 else position
        return n * partition_index + local_index


def amalgam(k: int, r: int, elements: Arrangement) -> list:
    """
    The `k`th permutation of `r` elements taken from `elements`.
    """

    def element(i: int):
        nonlocal k
        p = len(elements) ** (r - i - 1)
        index = k // p
        k %= p
        return elements[index]

    return [element(i) for i in range(r)]


def inverse_amalgam(amalgam: list, elements: Arrangement) -> int:
    """
    The index of `amalgam` in the ordered amalgams of elements in `elements`.
    """
    r = len(amalgam)
    n = len(elements)
    powers = [n**i for i in range(r)]
    return sum(
        [
            elements.index(amalgam[position]) * powers[r - position - 1]
            for position in range(r)
        ]
    )


def combination(k: int, r: int, elements: Arrangement) -> list:
    """
    The `k`th combination of `r` elements taken from elements.
    """
    n = len(elements)
    position = 0
    d = ncr(n - position - 1, r - 1)

    while k >= d:
        k -= d
        position += 1
        d = ncr(n - position - 1, r - 1)

    if r == 0:
        return []
    else:
        tail = elements[(position + 1) :]
        dummy = [elements[position]]
        dummy.extend(combination(k, r - 1, tail))
        return dummy


def inverse_combination(combination: list, elements: Arrangement) -> int:
    """
    The index of `combination` in the ordered combinations of elements in `elements`.
    """

    def helper(combination: list, elements: Arrangement) -> int:
        if len(combination) == 0:
            return 0
        else:
            k = 0
            r = len(combination)
            n = len(elements)
            element_index = 0
            while combination[0] != elements[element_index]:
                k += ncr(n - element_index - 1, r - 1)
                element_index += 1
            return k + helper(combination[1:], elements[(element_index + 1) :])

    return helper(
        sorted_elements(combination, elements),
        elements,
    )


def permutation(k: int, r: int, elements: Arrangement) -> list:
    """
    The `k`th permutation of `r` elements taken from `elements`.
    """
    f = fact(r)
    partition_index = k // f
    local_index = k % f
    comb = combination(partition_index, r, elements)
    return total_permutation(local_index, comb)


def inverse_permutation(permutation: list, elements: Arrangement) -> int:
    """
    The index of `permutation` in the ordered permutations of elements in `elements`.
    """
    r = len(permutation)
    if r == 0:
        return 0
    else:
        sorted_permutation = sorted_elements(permutation, elements)
        group = inverse_combination(sorted_permutation, elements)
        return group * fact(r) + inverse_total_permutation(
            permutation, sorted_permutation
        )


def composition(k: int, r: int, elements: Arrangement) -> list:
    """
    The `k`th composition of `r` elements taken from `elements`.
    """
    n = len(elements)
    position = 0
    d = ncr(n + r - position - 2, r - 1)

    while k >= d:
        k -= d
        position += 1
        d = ncr(n + r - position - 2, r - 1)

    if r == 0:
        return []
    else:
        tail = elements[position:]
        dummy = [elements[position]]
        dummy.extend(composition(k, r - 1, tail))
        return dummy


def inverse_composition(composition: list, elements: Arrangement) -> int:
    """
    The index of `composition` in the ordered compositions of elements in `elements`.
    """

    def helper(composition: list, elements: Arrangement) -> int:
        if len(composition) == 0:
            return 0
        else:
            k = 0
            n = len(elements)
            r = len(composition)
            element_index = 0
            while composition[0] != elements[element_index]:
                k += ncr(n + r - element_index - 2, r - 1)
                element_index += 1
            return k + helper(composition[1:], elements[element_index:])

    return helper(sorted_elements(composition, elements), elements)


def subset(k: int, elements: Arrangement) -> list:
    """
    The `k`th subset of elements taken from `elements`.
    """
    return [elements[i] for i in [j for j in range(len(elements)) if k & (1 << j) != 0]]


def inverse_subset(subset: list, elements: Arrangement) -> int:
    """
    The index of `subset` in the ordered subsets of elements in `elements`.
    """

    def helper(subset: list, elements: Arrangement) -> int:
        k = 0
        n = len(elements)
        power = 1
        for index in range(n):
            if elements[index] in subset:
                k += power
            power *= 2
        return k

    return helper(
        sorted_elements(list(set(subset)), elements),
        elements,
    )


def compound(k: int, elements: Arrangement) -> list:
    """
    The `k`th compound of elements taken from `elements`.
    """
    n = len(elements)
    for r in range(n):
        group_size = npr(n, r)
        if k >= group_size:
            k -= group_size
        else:
            break
    else:
        r += 1
    return permutation(k, r, elements)


def inverse_compound(compound: list, elements: Arrangement):
    """
    The index of `compound` in the ordered compounds of elements in `elements`.
    """
    n = len(elements)
    k = sum([npr(n, r) for r in range(len(compound))])
    return k + inverse_permutation(compound, elements)


def adjusted_index(k: int, n: int) -> int:
    """
    Index `k` mod `n` (for wraparound).
    """
    return k % n
