import itertools
import unittest
import typipe as ty
from typing import Iterable, Callable
import math


def times_two(x: int) -> int:
    return x * 2


class TestTypipe(unittest.TestCase):
    def typipe_aliases_identity_as_get(self) -> None:
        self.assertEqual(ty.get, ty.identity)
        self.assertEqual(ty.get(5), 5)
        self.assertEqual(ty.get("x"), "x")
        self.assertEqual(ty.get(ty), ty)
        self.assertEqual(ty.get(self), self)

    def test_pipe_get(self):
        result: ty.Piped[int] = ty.pipe(5) | times_two
        self.assertEqual(result.get(), 10)

    def test_pipe_get_and_then_identity(self):
        result: int = ty.pipe(-3) | times_two > ty.get
        self.assertEqual(result, -6)

    def test_pipe_with_multiple_operations(self):
        result: ty.Piped[str] = (
            ty.pipe(253)
            | times_two
            | times_two
            | times_two
            | ty.castfunc(int, str, lambda s: f"hello {s}!!")
            | ty.castfunc(str, str, lambda s: s.upper())
        )
        self.assertEqual(result.get(), "HELLO 2024!!")

    def test_piped_len(self):
        p = ty.pipe(3.1415926535)
        self.assertEqual(len(p), 1)
        p = p | ty.identity | ty.identity
        self.assertEqual(len(p), 3)
        p = p | ty.identity | ty.identity | ty.identity | round
        self.assertEqual(len(p), 7)
        p = p | times_two
        self.assertEqual(len(p), 8)

    def test_map(self):
        result: list[int] = ty.pipe([1, 2, 3]) | ty.map(times_two) > list[int]
        self.assertEqual(result, [2, 4, 6])

    def test_curry(self):
        def add(x: int, y: int) -> int:
            return x + y

        curried_add: Callable[[int], Callable[[int], int]] = ty.curry(add)
        add_five: Callable[[int], int] = curried_add(5)
        self.assertEqual(add_five(3), 8)

    # def test_cast(self):
    #     result = ty.pipe([(0, 1)]) | ty.cast(list[tuple[int, int]])
    #     # todo: how to test?
    #     assert result == result

    def test_filter(self):
        def is_even(x: int) -> bool:
            return x % 2 == 0

        result: list[int] = ty.pipe([1, 2, 3, 4, 5, 6]) | ty.filter(is_even) > list[int]
        self.assertEqual(result, [2, 4, 6])

    def test_filterfalse(self):
        def is_even(x: int) -> bool:
            return x % 2 == 0

        result: list[int] = (
            ty.pipe([1, 2, 3, 4, 5, 6]) | ty.filterfalse(is_even) > list[int]
        )
        self.assertEqual(result, [1, 3, 5])

    def test_reduce(self):
        def sum_func(x: int, y: int) -> int:
            return x + y

        result = ty.pipe([1, 2, 3, 4, 5]) | ty.reduce(sum_func, 0) > ty.get
        self.assertEqual(result, 15)

    def test_starmap(self):
        # TODO: currently starmap is defined as a composition of map and star. Somehow this doesn't infer types well.
        def add(x: int, y: int) -> int:
            return x + y

        xs: list[tuple[int, int]] = [(0, 1), (2, 3), (4, 5)]
        result = ty.pipe(xs) | ty.starmap(add) > list[int]
        self.assertEqual(result, [1, 5, 9])

    def test_star(self):
        def add(x: int, y: int) -> int:
            return x + y

        xs: list[tuple[int, int]] = [(0, 1), (2, 3), (4, 5)]
        # NOTE: NB passing xs directly would not be typechecked,
        # since [(0, 1), (2, 3), (4, 5)] is inferred as list[Any]
        result = ty.pipe(xs) | ty.map(ty.star(add)) > list[int]
        self.assertEqual(result, [1, 5, 9])

    def test_flatmap(self):
        def add(x: int) -> list[int]:
            return [x] * x

        result = ty.pipe([0, 1, 2, 3, 4]) | ty.flatmap(add) > list[int]
        self.assertEqual(result, [1, 2, 2, 3, 3, 3, 4, 4, 4, 4])

    def test_accumulate(self):
        result = (
            ty.pipe([1, 2, 3, 4, 5]) | ty.accumulate(lambda x, y: x + y) | list[int]
        )
        self.assertEqual(result.get(), [1, 3, 6, 10, 15])

    def test_tapwith(self):
        log: list = []
        x: ty.Piped[Iterable[int]] = (
            ty.pipe([1, 2, 3])
            | ty.map(times_two)
            | ty.map(ty.tapwith(lambda xs: (log.append(xs), log.append("hi"))))
            | ty.map(times_two)
        )
        self.assertEqual(log, [])
        y: list[int] = x > list[int]
        self.assertEqual(log, [2, "hi", 4, "hi", 6, "hi"])
        self.assertEqual(y, [4, 8, 12])

    def test_tapcopywith(self):
        log: list = []
        x: ty.Piped[Iterable[int]] = (
            ty.pipe([1, 2, 3])
            | ty.map(times_two)
            | ty.tapcopywith(lambda xs: (log.append(list(xs)), log.append("hi")))
            | ty.map(times_two)
        )
        self.assertEqual(log, [])
        y: list[int] = x > list[int]
        self.assertEqual(log, [[2, 4, 6], "hi"])
        self.assertEqual(y, [4, 8, 12])

    def test_tapwith_antiusecase(self):
        # todo: obviously would be better without this behavior. Consider changing
        log: list = []

        def append(x):
            log.append(list(x))

        x: ty.Piped[Iterable[int]] = (
            ty.pipe([1, 2, 3])
            | ty.map(times_two)
            | ty.tapwith(append)
            | ty.map(times_two)
        )
        self.assertEqual(log, [])
        y: list[int] = x > list[int]
        self.assertEqual(log, [[2, 4, 6]])
        self.assertEqual(y, [])

    def test_dropwhile(self):
        xs = itertools.count()
        ys = (
            ty.pipe(xs)
            | ty.dropwhile(ty.castfunc(int, bool, lambda x: x < 3))
            | ty.take(3)
            > list[int]
        )
        self.assertEqual(ys, [3, 4, 5])

    def test_drop(self):
        xs = itertools.count()
        ys = ty.pipe(xs) | ty.drop(10) | ty.take(3) > list[int]
        self.assertEqual(ys, [10, 11, 12])

    def test_takewhile(self):
        xs = itertools.count()
        taken = (
            ty.pipe(xs) | ty.takewhile(ty.castfunc(int, bool, lambda x: x < 3))
            > list[int]
        )
        self.assertEqual(taken, [0, 1, 2])

    def test_take(self):
        xs = itertools.count()
        taken = ty.pipe(xs) | ty.take(5) > list[int]
        self.assertEqual(taken, [0, 1, 2, 3, 4])

    def test_last(self):
        xs = [1, 1, 1, 1, 1, 1, 9999]
        x = ty.pipe(xs) | ty.last > int
        self.assertEqual(x, 9999)

    def test_tail(self):
        xs = [1, 1, 1, 1, 1, 1, 9999]
        x = ty.pipe(xs) | ty.tail(3) > list[int]
        self.assertEqual(x, [1, 1, 9999])

    def test_tee(self):
        xs = [1, 2]
        x, y = ty.pipe(xs) | ty.tee(2) > ty.get
        self.assertEqual(list(x), [1, 2])
        self.assertEqual(list(y), [1, 2])

    def test_permutations(self):
        xs = [0, 1]
        ys = ty.pipe(xs) | ty.permutations(2) > set[tuple[int, ...]]
        self.assertEqual(ys, {(0, 1), (1, 0)})
        xs = [0, 1, 2]
        ys = ty.pipe(xs) | ty.permutations(2) > set[tuple[int, ...]]
        self.assertEqual(ys, {(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)})
        ys = ty.pipe(xs) | ty.permutations(3) > set[tuple[int, ...]]
        self.assertEqual(
            ys,
            {(0, 1, 2), (1, 2, 0), (2, 0, 1), (0, 2, 1), (2, 1, 0), (1, 0, 2)},
        )

        for n in range(9):
            xs = list(range(n))
            for k in range(n):
                ys = ty.pipe(xs) | ty.permutations(k) > set[tuple[int, ...]]
                self.assertEqual(len(ys), math.perm(n, k))

    def test_combinations(self):
        xs = [0, 1]
        ys = ty.pipe(xs) | ty.combinations(2) > set[tuple[int, ...]]
        self.assertEqual(ys, {(0, 1)})
        xs = [0, 1, 2]
        ys = ty.pipe(xs) | ty.combinations(2) > set[tuple[int, ...]]
        self.assertEqual(ys, {(0, 1), (0, 2), (1, 2)})
        ys = ty.pipe(xs) | ty.combinations(3) > set[tuple[int, ...]]
        self.assertEqual(
            ys,
            {(0, 1, 2)},
        )
        for n in range(10):
            xs = list(range(n))
            for k in range(n):
                ys = ty.pipe(xs) | ty.combinations(k) > set[tuple[int, ...]]
                self.assertEqual(len(ys), math.comb(n, k))

    def test_combinations_with_replacement(self):
        xs = [0, 0, 0, 1, 1]
        ys = ty.pipe(xs) | ty.combinations_with_replacement(4) > set[tuple[int, ...]]
        self.assertEqual(
            ys,
            {(0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1)},
        )

    def test_batched(self):
        xs = ty.pipe(10) > range
        yss = ty.pipe(xs) | ty.batched(3) > list
        self.assertEqual(yss, [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)])


if __name__ == "__main__":
    unittest.main()
