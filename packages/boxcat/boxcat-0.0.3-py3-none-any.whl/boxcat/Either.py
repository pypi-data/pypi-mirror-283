from typing import Generic, TypeVar, Callable

L = TypeVar('L')
R = TypeVar('R')
U = TypeVar('U')


class Either(Generic[L, R]):

    def __init__(self):
        self.value = None

    def is_left(self) -> bool:
        return isinstance(self, Left)

    def is_right(self) -> bool:
        return isinstance(self, Right)

    def map(self, func: Callable[[R], U]) -> 'Either[L, U]':
        if self.is_right():
            return Right(func(self.value))
        return self  # type: ignore

    def flat_map(self, func: Callable[[R], 'Either[L, U]']) -> 'Either[L, U]':
        if self.is_right():
            return func(self.value)  # type: ignore
        return self  # type: ignore

    def fold(self, if_left: Callable[[L], U], if_right: Callable[[R], U]) -> U:
        if self.is_right():
            return if_right(self.value)  # type: ignore
        return if_left(self.value)  # type: ignore


# Left subclass
class Left(Either[L, R]):
    def __init__(self, value: L):
        self.value = value


# Right subclass
class Right(Either[L, R]):
    def __init__(self, value: R):
        self.value = value


# Example usage
def example():
    left_value = Left("Error")
    right_value = Right(42)

    # Using map on Right
    mapped_right = right_value.map(lambda x: x * 2)
    print(mapped_right.value if mapped_right.is_right() else "No value")  # Output: 84

    # Using flat_map on Right
    flat_mapped_right = right_value.flat_map(lambda x: Right(x * 2))
    print(flat_mapped_right.value if flat_mapped_right.is_right() else "No value")  # Output: 84

    # Using fold
    result = right_value.fold(
        if_left=lambda x: f"Error: {x}",
        if_right=lambda x: f"Success: {x}"
    )
    print(result)  # Output: Success: 42

    # Using fold on Left
    result = left_value.fold(
        if_left=lambda x: f"Error: {x}",
        if_right=lambda x: f"Success: {x}"
    )
    print(result)  # Output: Error: Error
