from typing import List

import pytest

from boxcat.Seq import Seq


# Test cases for the PyfunList class
def test_map():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    pyfunList = Seq(numbers)

    assert pyfunList.map(lambda x: x + 1).back_to_python_list() == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


def test_flat_map():

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    pyfunList = Seq(numbers)

    assert pyfunList.flat_map(lambda x: [x + 1]).back_to_python_list() == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


def test_fold_left():

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    pyfunList = Seq(numbers)

    assert pyfunList.fold_left(0)(lambda x, y: x + y) == 55


# If you want to run tests from the command line using pytest
if __name__ == "__main__":
    pytest.main()
