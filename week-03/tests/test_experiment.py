"""蒲丰投针实验的公开测试"""

import math
import os
import tempfile

import pytest

import experiment


class TestCrossesLine:
    """测试触线判据"""

    def test_crossing_known_positions(self):
        """已知针位的测试：针长 0.5，线距 1，夹角 π/2"""
        L = 0.5  # 针长
        angle = math.pi / 2  # 垂直

        # 半根针垂直伸出的距离 = 0.25
        # 中心距 0.4 > 0.25，够不到线
        assert experiment.crosses_line(0.4, angle, L) is False

        # 中心距 0.1 < 0.25，相交
        assert experiment.crosses_line(0.1, angle, L) is True

        # 中心距 0.25 == 0.25，恰好触线，也记为相交
        assert experiment.crosses_line(0.25, angle, L) is True

    def test_parallel_needle_on_line(self):
        """针平行且落在线上：distance=0, angle=0"""
        # angle=0 时 sin(0)=0，垂直伸出=0
        # distance=0 <= 0，应该相交
        assert experiment.crosses_line(0.0, 0.0, 0.5) is True

    def test_no_crossing_when_away(self):
        """距离很远时不相交"""
        assert experiment.crosses_line(0.5, math.pi / 4, 0.5) is False


class TestEstimator:
    """测试 π 估计公式"""

    def test_estimator_has_a_hand_calculable_answer(self):
        """手算答案：100 次投针，32 次触线
        π ≈ 2 * 0.5 * 100 / (1 * 32) = 100 / 32 = 3.125
        """
        result = experiment.estimate_pi(100, 32, needle_length=0.5, line_spacing=1.0)
        assert result == pytest.approx(3.125)

    def test_zero_crossings_raises(self):
        """相交次数为 0 时应该报错"""
        with pytest.raises(ValueError):
            experiment.estimate_pi(100, 0)


class TestSimulation:
    """测试模拟实验"""

    def test_seed_is_reproducible(self):
        """相同 seed 应该得到相同结果"""
        r1 = experiment.simulate(1000, seed=42)
        r2 = experiment.simulate(1000, seed=42)
        assert r1["crossings"] == r2["crossings"]
        assert r1["pi_estimate"] == pytest.approx(r2["pi_estimate"])

    def test_different_seeds_different_results(self):
        """不同 seed 结果应该不同"""
        r1 = experiment.simulate(1000, seed=42)
        r2 = experiment.simulate(1000, seed=99)
        assert r1["crossings"] != r2["crossings"]

    def test_crossings_within_bounds(self):
        """相交次数应该在合理范围内"""
        result = experiment.simulate(10000, seed=42)
        assert 0 < result["crossings"] < 10000

    def test_result_dict_keys(self):
        """结果字典应该包含所有必需的键"""
        result = experiment.simulate(100, seed=42)
        expected_keys = {"num_tosses", "crossings", "pi_estimate",
                        "seed", "needle_length", "line_spacing"}
        assert expected_keys.issubset(result.keys())


class TestCSVOutput:
    """测试 CSV 输出"""

    def test_csv_saved_correctly(self):
        """CSV 文件应该正确保存结果"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "results.csv")

            results = [experiment.simulate(100, seed=42)]
            experiment.save_results_to_csv(results, filename=filepath)

            assert os.path.exists(filepath)

            import csv
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                assert len(rows) == 1
                assert rows[0]["seed"] == "42"
                assert rows[0]["num_tosses"] == "100"
