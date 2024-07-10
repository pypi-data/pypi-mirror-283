from functools import reduce
from typing import List, Callable, TypeVar, Generic

T = TypeVar('T')
U = TypeVar('U')


class Seq(Generic[T]):

    def __init__(self, iterable: List[T]):
        self.list = iterable

    def is_not_empty(self) -> bool:
        if len(self.list) > 0:
            return True
        else:
            return False

    def take(self, n: int) -> 'Seq[T]':
        return Seq(self.list[:n])

    def fill(self, number_of_times: int) -> Callable[[T], 'Seq[U]']:
        def append_item(*item: T) -> Seq[U]:
            result = self.list

            for i in range(number_of_times):
                for elem in item:
                    result.append(elem)
            return Seq(result)

        return append_item

    def map(self, func: Callable[[T], U]) -> 'Seq[U]':
        return Seq([func(item) for item in self.list])

    def mapN(self, func: Callable[..., U], *seqs: List[T]) -> List[U]:
        return [func(*args) for args in zip(self.list, *seqs)]

    def flat_map(self, func: Callable[[T], List[U]]) -> 'Seq[U]':
        flattened = [item for sublist in map(func, self.list) for item in sublist]
        return Seq(flattened)

    def filter(self, func: Callable[[T], bool]) -> 'Seq[T]':
        return Seq([item for item in self.list if func(item)])

    def reduce(self, func: Callable[[T, T], T], initial: T) -> T:
        return reduce(func, self.list, initial)

    def fold_left(self, initial: U) -> Callable[[Callable[[U, T], U]], U]:
        def inner_fold(func: Callable[[U, T], U]) -> U:
            res = initial
            for item in self.list:
                res = func(res, item)
            return res

        return inner_fold

    def fold_right(self, func: Callable[[T], Callable[[U], U]], initial: U) -> U:
        def inner_func(item: T, acc: U) -> U:
            return func(item)(acc)

        return reduce(lambda acc, item: inner_func(item, acc), reversed(self.list), initial)

    def reverse(self) -> 'Seq[T]':
        return Seq(reversed(self.list))

    def to_list(self) -> List[T]:
        return self.list
