from boxcat.Either import Left, Right


def test_is_left():
    left = Left("error")
    right = Right(42)
    assert left.is_left()
    assert not right.is_left()


def test_is_right():
    left = Left("error")
    right = Right(42)
    assert not left.is_right()
    assert right.is_right()


def test_map_on_right():
    right = Right(42)
    mapped = right.map(lambda x: x + 1)
    assert mapped.is_right()
    assert mapped.value == 43


def test_map_on_left():
    left = Left("error")
    mapped = left.map(lambda x: x + 1)
    assert mapped.is_left()
    assert mapped.value == "error"


def test_flat_map_on_right():
    right = Right(42)
    flat_mapped = right.flat_map(lambda x: Right(x + 1))
    assert flat_mapped.is_right()
    assert flat_mapped.value == 43


def test_flat_map_on_left():
    left = Left("error")
    flat_mapped = left.flat_map(lambda x: Right(x + 1))
    assert flat_mapped.is_left()
    assert flat_mapped.value == "error"


def test_fold_on_right():
    right = Right(42)
    result = right.fold(lambda l: f"Error: {l}", lambda r: f"Result: {r}")
    assert result == "Result: 42"


