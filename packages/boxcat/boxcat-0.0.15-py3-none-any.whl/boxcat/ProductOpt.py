from typing import Callable, TypeVar

from boxcat.Option import Option

T = TypeVar('T')
U = TypeVar('U')


class ProductO:
    values: tuple['Option[T]', ...]

    def __init__(self, *options: 'Option[T]'):
        self.values = options

    def mapN(self, func: Callable[..., U]) -> 'Option[U]':
        mapped_values = [opt.value for opt in self.values if opt is not None]
        if len(mapped_values) == len(self.values):
            return Option(func(*mapped_values))
        else:
            return Option()

    def get(self):
        return self.values
