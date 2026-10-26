"""学生自测：另选一组合法输入，核验配置隔离的五项承诺。

每个测试通过函数参数 make_variant 接收课程 fixture，
不直接 import variant/examples 里的实现，否则 --impl 无法切换。
预期与原始配置都在这里独立写出，不用 before = source 保存旧内容。
"""

from copy import deepcopy

# 自己另选的一组合法输入（与教师 test_acceptance.py 的 CASES 不同）
ORIGINAL = {"seed": 5, "sample_sizes": [2000, 4000, 6000, 8000]}
NEW_SEED = 888
INDEX = 1
REPLACEMENT = 4500
EXPECTED = {"seed": 888, "sample_sizes": [2000, 4500, 6000, 8000]}


def fresh_source():
    """每次独立深拷贝出一份原配置，避免测试之间共享被污染。"""
    return deepcopy(ORIGINAL)


def test_returns_expected_content(make_variant):
    """承诺1：返回结果正确，只更新 seed 和指定位置，其余保持。"""
    source = fresh_source()
    result = make_variant(source, NEW_SEED, INDEX, REPLACEMENT)
    assert result == EXPECTED


def test_source_keeps_original_content(make_variant):
    """承诺2：调用后 source 仍是调用前的内容。"""
    source = fresh_source()
    make_variant(source, NEW_SEED, INDEX, REPLACEMENT)
    assert source == ORIGINAL


def test_dictionary_and_list_are_independent(make_variant):
    """承诺3：返回字典与 source 不同，返回的 sample_sizes 列表也与原列表不同。"""
    source = fresh_source()
    result = make_variant(source, NEW_SEED, INDEX, REPLACEMENT)
    assert result is not source
    assert result["sample_sizes"] is not source["sample_sizes"]


def test_later_edits_to_result_do_not_touch_source(make_variant):
    """承诺4：之后随便改返回结果，source 都不受影响。"""
    source = fresh_source()
    result = make_variant(source, NEW_SEED, INDEX, REPLACEMENT)

    result["seed"] = 999
    result["sample_sizes"][INDEX] = 0
    result["sample_sizes"].append(12345)

    assert source == ORIGINAL


def test_two_calls_can_be_modified_separately(make_variant):
    """承诺5：相同参数调两次，内容相等但各自独立；改第一份不影响第二份和 source。"""
    source = fresh_source()
    first = make_variant(source, NEW_SEED, INDEX, REPLACEMENT)
    second = make_variant(source, NEW_SEED, INDEX, REPLACEMENT)

    assert first == EXPECTED
    assert second == EXPECTED
    assert first == second
    assert first is not second
    assert first["sample_sizes"] is not second["sample_sizes"]

    first["seed"] = 1
    first["sample_sizes"][INDEX] = 2
    first["sample_sizes"].append(777)

    assert second == EXPECTED
    assert source == ORIGINAL
