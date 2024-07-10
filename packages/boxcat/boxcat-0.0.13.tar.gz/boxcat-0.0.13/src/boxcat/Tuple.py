from typing import Optional, Callable, TypeVar

T = TypeVar('T')
U = TypeVar('U')


class Option:

    def __init__(self, value: Optional[T]):
        self.value = value

    def mapN(func: Callable[..., U], *options: 'Option[U]') -> 'Option[U]':
        mapped_values = [opt.value for opt in options if opt.value is not None]
        if len(mapped_values) == len(options):
            return Option(func(*mapped_values))
        else:
            return Option()


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