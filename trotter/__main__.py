from sys import argv
from .amalgam import Amalgams
from .combination import Combinations
from .combinatoric import Combinatoric
from .composition import Compositions
from .compound import Compounds
from .permutation import Permutations
from .subset import Subsets


if __name__ == "__main__":
    elements = "abcde"
    k = 3
    if len(argv) == 3:
        try:
            k = int(argv[1])
        except ValueError:
            print("Expecting integer k as first argument...")
            exit(1)
        elements = argv[2]
        if k < 0 or k > len(elements):
            print(
                f"Expecting 0 ≤ k ≤ {len(elements)} "
                f"for elements {",".join(elements)}..."
            )
            exit(1)

    C: Combinatoric

    for C in Permutations, Combinations, Amalgams, Compositions:
        print()
        print(C)
        cs = C(3, elements)
        print(cs)
        for i, c in enumerate(cs):
            print(f"[{i}]".rjust(5) + f" {c} -> {cs.index(c)}")

    for C in Subsets, Compounds:
        print()
        print(C)
        cs = C(elements)
        print(cs)
        for i, c in enumerate(cs):
            print(f"[{i}]".rjust(5) + f" {c}".rjust(6) + f" -> {cs.index(c)}")
