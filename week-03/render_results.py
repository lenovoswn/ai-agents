"""根据 results.csv 生成图表和 LaTeX 表格"""

import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_results(filename="results.csv"):
    """读取实验结果"""
    results = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append({
                "num_tosses": int(row["num_tosses"]),
                "crossings": int(row["crossings"]),
                "pi_estimate": float(row["pi_estimate"]),
                "seed": int(row["seed"]),
                "needle_length": float(row["needle_length"]),
                "line_spacing": float(row["line_spacing"]),
            })
    return results


def make_plot(results, filename="results.png"):
    """生成投针次数与 π 估计值的对比图"""
    ns = [r["num_tosses"] for r in results]
    pis = [r["pi_estimate"] for r in results]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(ns, pis, "bo-", label="Estimated π", linewidth=2, markersize=8)
    ax.axhline(y=3.1415926535, color="r", linestyle="--", label="True π ≈ 3.1416")

    ax.set_xlabel("Number of Tosses", fontsize=12)
    ax.set_ylabel("Estimated π", fontsize=12)
    ax.set_title("Buffon's Needle: π Estimation vs. Sample Size", fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xscale("log")

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"图表已保存: {filename}")


def make_table_tex(results, filename="results-table.tex"):
    """生成 LaTeX 表格"""
    lines = [
        "\\begin{table}[htbp]",
        "\\centering",
        "\\caption{蒲丰投针实验结果}",
        "\\begin{tabular}{cccc}",
        "\\hline",
        "投针次数 N & 相交次数 K & 相交比例 K/N & 估计值 π \\\\",
        "\\hline",
    ]
    for r in results:
        ratio = r["crossings"] / r["num_tosses"]
        lines.append(
            f"{r['num_tosses']} & {r['crossings']} & "
            f"{ratio:.4f} & {r['pi_estimate']:.6f} \\\\"
        )
    lines.extend([
        "\\hline",
        "\\end{tabular}",
        "\\end{table}",
    ])

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"表格已保存: {filename}")


def make_params_tex(results, filename="results-params.tex"):
    """生成实验参数说明"""
    r = results[0]
    content = (
        f"实验参数：针长 $L = {r['needle_length']}$，"
        f"线距 $d = {r['line_spacing']}$，"
        f"随机种子 seed = {r['seed']}。"
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"参数说明已保存: {filename}")


def main():
    results = load_results()
    make_plot(results)
    make_table_tex(results)
    make_params_tex(results)


if __name__ == "__main__":
    main()
