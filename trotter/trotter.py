from .helpers import Arrangement, fix_type


class Trotter:
    def __init__(self, elements: Arrangement) -> None:
        self._permutation = fix_type(elements, elements)
        self._n = len(elements)
        self._pivot_index = self._n - 1
        self._direction = -1

    @property
    def n(self) -> int:
        return self._n

    @property
    def permutation(self) -> Arrangement:
        return fix_type(self._permutation, self._permutation)

    @property
    def pivot(self):
        return self._permutation[self._pivot_index]

    @property
    def pivot_index(self) -> int:
        return self._pivot_index

    @property
    def direction(self) -> int:
        return self._direction

    def _step(self, direction: int) -> None:
        if self._n >= 2:
            next_pivot_index = self._pivot_index + direction * self._direction
            if next_pivot_index == -1:
                *elements, a, b = self._permutation
                self._permutation = fix_type(
                    self._permutation,
                    [*elements, b, a],
                )
                self._direction *= -1
            elif next_pivot_index == self._n:
                a, b, *elements = self._permutation
                self._permutation = fix_type(
                    self._permutation,
                    [b, a, *elements],
                )
                self._direction *= -1
            else:
                pivot = self._permutation[self._pivot_index]
                background = [
                    element for element in self._permutation if element != pivot
                ]

                background.insert(next_pivot_index, pivot)
                self._permutation = fix_type(
                    self._permutation,
                    background,
                )
                self._pivot_index = next_pivot_index

    def step(self) -> None:
        self._step(1)

    def step_back(self) -> None:
        self._step(-1)

    def __str__(self) -> str:
        pivot = self._permutation[self._pivot_index]
        template = r"<[{}]" if self._direction == -1 else r"[{}]>"
        return " ".join(
            template.format(element) if element == pivot else element
            for element in self._permutation
        )
