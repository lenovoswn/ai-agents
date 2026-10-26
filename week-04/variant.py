"""本周需要学生与 Agent 实现的入口。"""


def make_variant(source, seed, index, replacement):
    """返回可独立修改的追加方案，不改动 source。

    source 只含 seed 和 sample_sizes；sample_sizes 是非空正整数列表。
    seed、index、replacement 均合法，本题不要求检查非法输入。

    返回的新字典应更新 seed 和 sample_sizes[index]，其余内容保持。
    新字典、新列表与 source 独立；不同调用之间也不能共享它们。
    参数恰好与原配置相同，仍须返回独立方案。
    """
    # 第一层：复制字典，得到一个独立的新字典
    variant = source.copy()

    # 第二层：复制 sample_sizes 列表，得到一个独立的新列表
    # 不复制这一层，新老字典仍会共享同一个列表（shallow 故障）
    variant["sample_sizes"] = source["sample_sizes"].copy()

    # 在新字典、新列表上写入新值，不会触碰原 source
    variant["seed"] = seed
    variant["sample_sizes"][index] = replacement

    return variant
