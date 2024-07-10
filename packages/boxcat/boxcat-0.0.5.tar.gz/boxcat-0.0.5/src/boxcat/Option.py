from typing import Optional, Callable, TypeVar

T = TypeVar('T')
U = TypeVar('U')


class Option:
    def __init__(self, value: Optional[T]):
        self.value = value

    def map(self, func: Callable[[T], U]) -> 'Option[U]':
        if self.value is None:
            return Option(None)
        else:
            return Option(func(self.value))

    def mapN(func: Callable[..., U], *options: 'Option[U]') -> 'Option[U]':
        mapped_values = [opt.value for opt in options if opt.value is not None]
        if len(mapped_values) == len(options):
            return Option(func(*mapped_values))
        else:
            return Option()

    def flat_map(self, func: Callable[[T], Optional[U]]) -> 'Option[U]':
        if self.value is None:
            return Option(None)
        else:
            return func(self.value)

    def filter(self, func: Callable[[T], bool]) -> 'Option':
        if self.value is None or not func(self.value):
            return Option(None)
        else:
            return self

    def unsafe_get(self) -> U:
        return self.value

    def get_or_else(self, default_value: U) -> U:
        return self.value if self.value is not None else default_value

    def is_some(self) -> bool:
        return self.value is not None

    def is_none(self) -> bool:
        return self.value is None

    def to_optional(self) -> Optional[T]:
        return self.value

    def fold(self, if_none: Callable[[], U], if_present: Callable[[T], U]) -> U:
        if self.value is None:
            return if_none()
        else:
            return if_present(self.value)


if __name__ == "__main__":

    def mapN(func: Callable[..., U], *options: 'Option[U]') -> 'Option[U]':
        mapped_values = [opt.value for opt in options if opt.value is not None]
        if len(mapped_values) == len(options):
            return Option(func(*mapped_values))
        else:
            return Option()

    opt1 = Option(1)
    opt2 = Option(2)
    opt3 = Option(3)

    result = mapN(lambda x, y, z: x + y + z, opt1, opt2, opt3)
    print(result.value)  # Output: 6