# coding:utf-8
import itertools

loop = itertools.count(1)  # 无限打印 累加1,从1开始
# todo takewhile
l = itertools.takewhile(lambda x: x <= 10, loop)  # 给序列添加限制条件，返回生成器
print list(l)

from copy import deepcopy

d1 = zip(range(3), range(3, 5))
d2 = xrange(5, 7)
d3 = range(7, 11)


# todo chain
# d4 = itertools.chain(d1, d2, d3)
_tmp = [d1, d2, d3]
d4 = itertools.chain(*_tmp)  # 动态添加子列表方式
d5 = itertools.chain(d1, d2, d3)
print 6 in list(d4)

ls = deepcopy(list(d5))  # itertools.chain返回生成器,一次性，需要拷贝出来
print ls  # todo [(0, 3), (1, 4), 5, 6, 7, 8, 9, 10]  多个列表映射为一个 生成器
print 5 in ls  # True
print ls

# todo groupby
s1 = 'AAABBBCCAAA'  # todo groupby 之前要排序 相同元素在一起
for key, group in itertools.groupby(s1):  ## 返回分组, 连续相同的 元素，以及元素出现的生成器
	print key, list(group)
'''
A ['A', 'A', 'A']
B ['B', 'B', 'B']
C ['C', 'C']
A ['A', 'A', 'A']
'''
print "====" * 20
s1 = sorted(s1)  # 排序 ，将相同元素，排序在一起
for key, group in itertools.groupby(s1):  ## 返回分组
	print key, list(group)

print "====" * 20
s1 = 'AaaBBbCcAAA'
for key, group in itertools.groupby(s1, lambda x: x.upper()):  # todo 大小写按照一样的处理
	print key, list(group)
