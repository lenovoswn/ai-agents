"""蒲丰投针实验 (Buffon's Needle Experiment)"""

import csv
import math
import random


def crosses_line(distance, angle, needle_length=0.5):
    """判断针是否与平行线相交。

    参数:
        distance: 针中心到最近一条线的垂直距离
        angle: 针与平行线的夹角（弧度）
        needle_length: 针的全长

    返回:
        True 表示相交（包括恰好触线），False 表示不相交
    """
    half_length = needle_length / 2.0
    # 半根针在垂直方向上伸出的距离
    vertical_reach = half_length * math.sin(angle)
    # 中心距 <= 伸出距离 就算相交，包括恰好触线
    return distance <= vertical_reach


def estimate_pi(num_tosses, crossings, needle_length=0.5, line_spacing=1.0):
    """用投针结果估计 π。

    公式: π ≈ 2 * L * N / (d * K)
    其中 L=针长, N=投针数, d=线距, K=相交次数

    参数:
        num_tosses: 投针总次数 N
        crossings: 相交次数 K
        needle_length: 针长 L
        line_spacing: 线距 d

    返回:
        估计的 π 值；K=0 时抛出 ValueError
    """
    if crossings == 0:
        raise ValueError("相交次数为 0，无法估计 π")
    return 2.0 * needle_length * num_tosses / (line_spacing * crossings)


def simulate(num_tosses, seed=42, needle_length=0.5, line_spacing=1.0):
    """执行蒲丰投针实验。

    参数:
        num_tosses: 投针次数
        seed: 随机数种子，默认 42
        needle_length: 针长，默认 0.5
        line_spacing: 线距，默认 1.0

    返回:
        dict 包含 num_tosses, crossings, pi_estimate, seed,
              needle_length, line_spacing
    """
    rng = random.Random(seed)
    crossings = 0

    for _ in range(num_tosses):
        # 均匀取样: distance ∈ [0, d/2], angle ∈ [0, π/2]
        distance = rng.uniform(0, line_spacing / 2.0)
        angle = rng.uniform(0, math.pi / 2.0)

        if crosses_line(distance, angle, needle_length):
            crossings += 1

    pi_estimate = estimate_pi(num_tosses, crossings, needle_length, line_spacing)

    return {
        "num_tosses": num_tosses,
        "crossings": crossings,
        "pi_estimate": pi_estimate,
        "seed": seed,
        "needle_length": needle_length,
        "line_spacing": line_spacing,
    }


def save_results_to_csv(results_list, filename="results.csv"):
    """把多组实验结果保存到 CSV 文件。"""
    fieldnames = ["seed", "num_tosses", "crossings", "pi_estimate",
                  "needle_length", "line_spacing"]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results_list:
            writer.writerow(r)


def main():
    """运行默认的三组投针实验。"""
    needle_length = 0.5
    line_spacing = 1.0
    seed = 42

    results = []
    for n in [1000, 10000, 100000]:
        result = simulate(n, seed=seed,
                         needle_length=needle_length,
                         line_spacing=line_spacing)
        results.append(result)
        print(f"N={n:>6d}  K={result['crossings']:>6d}  "
              f"π ≈ {result['pi_estimate']:.6f}")

    save_results_to_csv(results)
    print(f"\n结果已保存到 results.csv")


if __name__ == "__main__":
    main()
