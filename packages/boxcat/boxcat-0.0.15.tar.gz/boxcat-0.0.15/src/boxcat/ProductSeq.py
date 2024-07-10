from typing import TypeVar

from boxcat.Seq import Seq

T = TypeVar('T')
U = TypeVar('U')


class ProductSeq:
    values: tuple['Seq[T]', ...]

    def __init__(self, *sequences: 'Seq[T]'):
        self.values = sequences

    def mapN(self, func) -> 'Seq[U]':
        return Seq([func(Seq(items.list)) for items in self.values])

    def get(self):
        return self.values
