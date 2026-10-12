"""蒲丰投针实验 (Buffon's Needle Experiment)"""

import csv
import math
import random


def crosses_line(distance, angle, length=0.5, spacing=1.0):
    """判断针是否与平行线相交。"""
    if distance < 0:
        raise ValueError(f"distance 不能为负: {distance}")
    if distance > spacing / 2:
        raise ValueError(f"distance 不能超过 spacing/2: {distance} > {spacing/2}")
    if angle < 0 or angle > math.pi / 2:
        raise ValueError(f"angle 应在 [0, π/2] 范围内: {angle}")
    if length <= 0:
        raise ValueError(f"length 必须为正: {length}")
    if length > spacing:
        raise ValueError(f"length 不能大于 spacing: {length} > {spacing}")
    if spacing <= 0:
        raise ValueError(f"spacing 必须为正: {spacing}")

    half_length = length / 2.0
    vertical_reach = half_length * math.sin(angle)
    return distance <= vertical_reach


def estimate_pi(n, crossings, length=0.5, spacing=1.0):
    """用投针结果估计 π。"""
    if n <= 0:
        raise ValueError(f"投针次数必须为正: {n}")
    if crossings < 0:
        raise ValueError(f"相交次数不能为负: {crossings}")
    if crossings > n:
        raise ValueError(f"相交次数不能大于投针次数: {crossings} > {n}")
    if crossings == 0:
        raise ValueError("相交次数为 0，无法估计 π")

    return 2.0 * length * n / (spacing * crossings)


def simulate(n, seed=42, length=0.5, spacing=1.0):
    """执行蒲丰投针实验。"""
    if n <= 0:
        raise ValueError(f"投针次数必须为正: {n}")

    rng = random.Random(seed)
    crossings = 0

    for _ in range(n):
        distance = rng.uniform(0, spacing / 2.0)
        angle = rng.uniform(0, math.pi / 2.0)

        if crosses_line(distance, angle, length=length, spacing=spacing):
            crossings += 1

    pi_estimate = estimate_pi(n, crossings, length=length, spacing=spacing)

    return {
        "n": n,
        "crossings": crossings,
        "pi_estimate": pi_estimate,
        "seed": seed,
        "length": length,
        "spacing": spacing,
        "needle_length": length,
        "line_spacing": spacing,
    }


def save_results_to_csv(results_list, filename="results.csv"):
    """把多组实验结果保存到 CSV 文件。"""
    fieldnames = ["seed", "n", "crossings", "pi_estimate", "needle_length", "line_spacing"]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results_list:
            row = {k: r[k] for k in fieldnames}
            writer.writerow(row)


def main():
    """运行默认的三组投针实验。"""
    length = 0.5
    spacing = 1.0
    seed = 42

    results = []
    for n in [1000, 10000, 100000]:
        result = simulate(n, seed=seed, length=length, spacing=spacing)
        results.append(result)
        print(f"N={n:>6d}  K={result['crossings']:>6d}  "
              f"π ≈ {result['pi_estimate']:.6f}")

    save_results_to_csv(results)
    print(f"\n结果已保存到 results.csv")


if __name__ == "__main__":
    main()
