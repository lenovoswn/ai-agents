"""W5 学生实现：先读 EXPERIMENT.txt，再与 Agent 完成三个函数。"""


def pop_last(items):
    """原地删除整数列表的最后一项并返回它；空列表返回 None。"""
    if not items:
        return None
    # list.pop() 不带参数时删除并返回最后一项，原列表当场变短。
    return items.pop()


def positive_squares(values):
    """返回正数项平方组成的新列表，保留顺序与重复项，不改输入。

    values 是普通整数列表或一维整数 NumPy 数组。
    空输入或没有正数时返回空列表。
    """
    # 逐项遍历原序列：先判断是否大于 0，再算平方，结果放进新列表。
    # 0 不是正数；不改原序列，也不为了去重而转成 set，所以顺序和重复项都保留。
    # int() 让 NumPy 整数也变成 Python int，结果始终是普通整数列表。
    return [int(value) ** 2 for value in values if value > 0]


def positive_square_map(record):
    """返回保留正数值并取平方的新字典，不改原字典。

    record 的键是字符串，值是整数；保留键的原相对顺序。
    空输入或没有正数值时返回空字典。
    """
    # 按键值对遍历，把符合条件的键写进新字典。
    # dict 保持插入顺序，因此按原顺序遍历就能保住键的相对顺序。
    return {key: int(value) ** 2 for key, value in record.items() if value > 0}
