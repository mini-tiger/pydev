def f1(lIn):
    l1 = sorted(lIn)
    l2 = [i for i in l1 if i < 0.5]
    return [i * i for i in l2]


def f2(lIn):
    l1 = [i for i in lIn if i < 0.5]
    l2 = sorted(l1)
    return [i * i for i in l2]


def f3(lIn):
    l1 = [i * i for i in lIn]
    l2 = sorted(l1)
    return [i for i in l1 if i < (0.5 * 0.5)]


def f4(lIn):
    # l1 = [i for i in lIn if i < 0.5]
    # l2 = sorted(lIn)
    return map(lambda x: x * x, sorted([i for i in lIn if i < 0.5]))


import cProfile, random

lIn = [random.random() for i in range(100000)]
# cProfile.run('f1(lIn)')  # 0.043 seconds
cProfile.run('f2(lIn)')  # 0.027 seconds
# cProfile.run('f3(lIn)')  #  0.046 seconds
cProfile.run('f4(lIn)')  # 0.026 seconds
