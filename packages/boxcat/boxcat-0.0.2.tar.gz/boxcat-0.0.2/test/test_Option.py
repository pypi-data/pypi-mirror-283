# tests/test_Option.py

import pytest

from boxcat.Option import Option


def test_option_some():
    some = Option(5)
    assert some.is_some()


def test_option_is_none():
    some = Option(5)
    assert not some.is_none()


def test_option_map():
    some = Option(5)
    option_ten = some.map(lambda x: x * 2)
    assert option_ten.get_or_else(0) == 10


def test_option_flat_map():
    some = Option(5)
    option_ten = some.flat_map(lambda x: Option(x * 2))
    assert option_ten.get_or_else(0) == 10


def test_option_fold():
    some = Option(5)
    assert some.fold(lambda: 0, lambda x: x) == 5


def test_option_get_or_else():
    some = Option(5)
    assert some.get_or_else(0) == 5


def test_option_none():
    none = Option(None)
    assert not none.is_some()
    assert none.is_none()
    assert none.map(lambda x: x * 2).get_or_else(0) == 0
    assert none.flat_map(lambda x: Option(x * 2)).get_or_else(0) == 0
    assert none.fold(lambda: 0, lambda x: x) == 0
    assert none.get_or_else(5) == 5


if __name__ == "__main__":
    pytest.main()
