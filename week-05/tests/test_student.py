"""可修改的小测试示例：另选输入，保留自己的预期与解释。

测试通过参数接收课程 fixture，--impl 才能切换候选实现。
不要直接 from operations import pop_last 绕过这个开关。
"""

import numpy as np


def test_my_pop_example(pop_last):
    items = [7, 4]

    result = pop_last(items)

    assert result == 4
    assert items == [7]


def test_my_pop_last_empty_returns_none(pop_last):
    """我选的输入：空列表返回 None，且仍然是空列表。"""
    items = []

    result = pop_last(items)

    assert result is None
    assert items == []


def test_my_pop_last_keeps_order_and_removes_only_the_last(pop_last):
    """我选的输入：含重复项与负数，只能少最后一项，其他顺序不变。"""
    items = [3, -1, 3, 0]

    result = pop_last(items)

    assert result == 0
    assert items == [3, -1, 3]


def test_my_positive_squares_keeps_repeats_and_drops_zero(positive_squares):
    """我选的输入：重复项要保留两份，0 会被丢掉。"""
    values = [4, 0, -4, 4, 1]
    before = values.copy()

    result = positive_squares(values)

    assert isinstance(result, list)
    assert result == [16, 16, 1]
    assert values == before
    assert result is not values


def test_my_positive_squares_from_numpy_array(positive_squares):
    """我选的输入：一维 NumPy 数组，返回普通 Python 列表，原数组不变。"""
    values = np.array([5, -5, 0, 2], dtype=np.int32)
    before = values.copy()

    result = positive_squares(values)

    assert isinstance(result, list)
    assert result == [25, 4]
    assert all(isinstance(value, int) for value in result)
    np.testing.assert_array_equal(values, before)


def test_my_positive_square_map_keeps_key_order(positive_square_map):
    """我选的输入：保留正数值的键及其相对顺序，原字典完全不变。"""
    record = {"later": -3, "middle": 0, "first": 2, "last": 3}
    before_keys = list(record)

    result = positive_square_map(record)

    assert result == {"first": 4, "last": 9}
    assert list(result) == ["first", "last"]
    assert result is not record
    assert record == {"later": -3, "middle": 0, "first": 2, "last": 3}
    assert list(record) == before_keys


def test_my_positive_square_map_empty_result(positive_square_map):
    """我选的输入：没有正数值时，返回空字典而不是 None。"""
    record = {"a": 0, "b": -2}

    result = positive_square_map(record)

    assert result == {}
    assert list(result) == []
    assert record == {"a": 0, "b": -2}
