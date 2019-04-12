# coding:utf-8
import itertools


l = range(10)
l1 = itertools.count(1)
# print map(lambda x, y:x + y, l, list(l1))  # map 由于其中一个是无限序列，会无限下去,不接受生成器作为参数
# todo imap
l2 = itertools.imap(lambda x, y: x * y, l, l1)  # 按照短的序列或生成器，返回生成器
print(list(l2))  # [0, 2, 6, 12, 20, 30, 42, 56, 72, 90]

# todo ifilter
print(list(itertools.ifilter(lambda x: x % 2, range(10))))  # 1 3 5 7 9
