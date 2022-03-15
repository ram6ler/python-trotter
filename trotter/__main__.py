from .amalgam import Amalgams
from .combination import Combinations
from .combinatoric import Combinatoric
from .composition import Compositions
from .compound import Compounds
from .permutation import Permutations
from .subset import Subsets


def test1() -> None:
    items = "-o#*+"
    k = 3

    def tower(cs: Combinatoric) -> None:
        print(repr(cs))
        print(str(cs))
        for i, c in enumerate(cs):
            index = cs.index(c)
            a = str(i).rjust(5)
            b = str(c).center(5)
            c = str(index).ljust(5)
            print(f"{a}{b}{c}")

        print("-" * 60)

    for c_2 in [Amalgams, Combinations, Compositions, Permutations]:
        c2s: Combinatoric = c_2(k, items)
        tower(c2s)

    for c_1 in [Compounds, Subsets]:
        c1s: Combinatoric = c_1(items)
        tower(c1s)


if __name__ == "__main__":
    test1()
