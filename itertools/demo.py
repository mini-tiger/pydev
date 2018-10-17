# coding:utf-8
import itertools
# todo count
for i in itertools.count(1):  # 无限打印 累加1,从1开始
	if i == 10:
		break
	print i

l = range(2, 11)
# for i in itertools.cycle("abc"): # todo 字符串是序列  a,b,c

# todo cycle
for i in itertools.cycle(l):
	# 无限打印 按照字符串索引2,3,4,5 无限
	print i
	if i == 5:
		break
# todo repeat
for i in itertools.repeat("ab", 2):  # 2代表重复次数 ab  ab
	print i
