"""我自己选择的一份输入与预期：W5 综合题 C｜对齐两次测量。

不导入任何参考实现，只使用 conftest 提供的同名 fixture。
测试函数名包含 compare_measurements，题目验收命令的 -k 也能选中。
"""

import numpy as np


def build_input(baseline_values, current_values, dtype):
    """统一构造本文件使用的 NumPy 输入。"""
    return (
        np.array(baseline_values, dtype=dtype),
        np.array(current_values, dtype=dtype),
    )


def test_my_compare_measurements_case(compare_measurements):
    """我选的输入：p / q 的幅度恰好等于阈值 3，都应判为正常；只有 s 异常。"""
    ids = ["p", "q", "r", "s", "t"]
    baseline, current = build_input([100, 50, 0, -7, 12], [103, 47, 0, -3, 12], np.int32)

    before_ids = ids.copy()
    before_baseline = baseline.copy()
    before_current = current.copy()

    result = compare_measurements(ids, baseline, current, 3)

    assert set(result) == {"delta", "alerts", "normal"}
    np.testing.assert_array_equal(
        result["delta"], np.array([3, -3, 0, 4, 0], dtype=np.int64)
    )
    assert result["alerts"] == ["s"]
    # normal 里是新的测量值，不是变化量；r 的值是 0 但它没有变化。
    assert result["normal"] == {"p": 103, "q": 47, "r": 0, "t": 12}

    # 三个输入都要保持原样。
    assert ids == before_ids
    np.testing.assert_array_equal(baseline, before_baseline)
    np.testing.assert_array_equal(current, before_current)


def test_my_compare_measurements_zero_threshold(compare_measurements):
    """边界：阈值为 0 时，完全没变的编号仍然算正常，只有真正变化的才是异常。"""
    ids = ["same", "up", "down"]
    baseline, current = build_input([7, 7, 7], [7, 8, 6], np.int64)

    result = compare_measurements(ids, baseline, current, 0)

    np.testing.assert_array_equal(result["delta"], np.array([0, 1, -1], dtype=np.int64))
    assert result["alerts"] == ["up", "down"]
    assert result["normal"] == {"same": 7}
