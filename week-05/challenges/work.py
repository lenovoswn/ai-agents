"""W5 综合选做：按合同完成函数，使用 challenges 中的公开测试验收。"""
#C题

import numpy as np


def summarize_values(values):
    """整理普通整数列表；不修改输入。

    返回 {"unique": 首次出现顺序的去重列表,
          "counts": 每个整数的出现次数字典,
          "repeated": 出现次数大于 1 的整数集合}。
    空输入返回 {"unique": [], "counts": {}, "repeated": set()}。
    每次调用产生独立结果，结果中的列表、字典、集合可以单独修改。
    """
    raise NotImplementedError("请实现 summarize_values")


def apply_changes(original, updates, removals):
    """在新字典上应用修改清单；三个输入均不修改。

    original 为字符串键、整数值的字典。
    updates 为按顺序执行的 (键, 值) 元组列表，后一次更新覆盖前一次。
    所有更新完成后，再按 removals 删除；缺失键与重复删除均可忽略。
    返回 {"record": 新字典, "changed": 最终相对 original 变化的键集合}。
    改回原值、新增后又删除都不算最终变化；字典键顺序不作要求。
    每次调用产生独立结果。
    """
    raise NotImplementedError("请实现 apply_changes")


def compare_measurements(ids, baseline, current, threshold):
    """对齐两次测量；不修改输入，返回独立的新结果。

    ids 为无重复的字符串列表；baseline、current 为等长的一维整数
    NumPy 数组；值范围为 [-1000000, 1000000]；threshold 为非负整数。
    返回 {"delta": 新的一维整数数组 current - baseline,
          "alerts": abs(delta) > threshold 的编号列表，保留输入顺序,
          "normal": 其余编号到 current 值的字典}。
    恰好等于阈值属于正常；空输入也要返回三个对应的空容器。
    先把 NumPy 整数转成 Python int 再计算，避免小 dtype 溢出。
    """
    # 逐位取出两次测量，先转成 Python int 再相减：避免 int8 / uint8
    # 这类小 dtype 直接做数组减法时溢出（例如 0 - 255 会绕回 1）。
    delta = np.array(
        [int(after) - int(before) for before, after in zip(baseline, current)],
        dtype=np.int64,
    )

    alerts = []
    normal = {}
    # zip 把三个序列按位置对齐：同一位置对应同一编号的两次测量。
    for name, change, value in zip(ids, delta, current):
        # 严格大于才算异常：幅度恰好等于阈值属于正常。
        if abs(int(change)) > threshold:
            alerts.append(name)
        else:
            # normal 保存的是新的测量值，不是变化量。
            normal[name] = int(value)

    return {"delta": delta, "alerts": alerts, "normal": normal}
