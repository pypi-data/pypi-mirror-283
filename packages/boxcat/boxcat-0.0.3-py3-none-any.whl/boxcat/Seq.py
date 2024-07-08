from functools import reduce
from typing import List, Callable, TypeVar, Generic

T = TypeVar('T')
U = TypeVar('U')


class Seq(Generic[T]):

    def __init__(self, iterable: List[T]):
        self.list = iterable

    def map(self, func: Callable[[T], U]) -> 'Seq[U]':
        return Seq(list(map(func, self.list)))

    def flat_map(self, func: Callable[[T], List[U]]) -> 'Seq[U]':
        flattened = [item for sublist in map(func, self.list) for item in sublist]
        return Seq(flattened)

    def filter(self, func: Callable[[T], bool]) -> 'Seq[T]':
        return Seq(list(filter(func, self.list)))

    def reduce(self, func: Callable[[T, T], T], initial: T) -> T:
        return reduce(func, self.list, initial)

    def fold(self, if_empty: Callable[[], U], if_non_empty: Callable[[List[T]], U]) -> U:
        if not self.list:
            return if_empty()
        else:
            return if_non_empty(self.list)

    def fold_left(self, initial: U) -> Callable[[Callable[[U, T], U]], U]:
        def inner_fold(func: Callable[[U, T], U]) -> U:
            res = initial
            for item in self.list:
                res = func(res, item)
            return res

        return inner_fold

    def back_to_python_list(self) -> List[T]:
        return self.list
