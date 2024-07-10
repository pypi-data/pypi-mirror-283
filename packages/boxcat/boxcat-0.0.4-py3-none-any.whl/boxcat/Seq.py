from functools import reduce
from typing import List, Callable, TypeVar, Generic

T = TypeVar('T')
U = TypeVar('U')


class Seq(Generic[T]):

    def __init__(self, iterable: List[T]):
        self.list = iterable

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



if __name__ == "__main__":
    # Example usage
    numbers = [1, 2, 3, 4, 5]

    # Create a sequence from a list of numbers
    seq = Seq(numbers)

    # Example usage of methods
    print(f"Original List: {seq.to_list()}")

    # Take first 3 elements
    # print(f"Take 3: {seq.take(3).to_list()}")
    print(f"Take 3: {numbers[:3]}")

    # Map each element to its square
    print(reversed(f"Map to squares: {seq.map(lambda x: x * x).to_list()}"))

    # Flatten elements after mapping to lists
    print(f"Flat map: {seq.flat_map(lambda x: [x, x]).to_list()}")

    # Filter even numbers
    print(f"Filter even: {seq.filter(lambda x: x % 2 == 0).to_list()}")

    # Reduce to sum
    print(f"Reduce sum: {seq.reduce(lambda x, y: x + y, 0)}")

    # Fold from left starting with 0
    print(f"Fold left: {seq.fold_left(0)(lambda x, y: x + y)}")

    # Fold from right with a function returning a function to multiply
    print(f"Fold right: {seq.fold_right(lambda x: lambda y: x * y, 1)}")
