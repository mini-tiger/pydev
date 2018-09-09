# coding:utf-8
from collections import defaultdict


# 使用默认dict ，每个颜色的值放入列表
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d1 = dict()
for k, v in s:
	tmp_l = list()
	if not d1.has_key(k):
		d1.setdefault(k, tmp_l)
		d1[k].append(v)
	else:
		d1[k].append(v)
print d1 # {'blue': [2, 4], 'red': [1], 'yellow': [1, 3]}


# defautdict 默认生成 一个字典的值
d1=defaultdict(list) ## 没有value 用list代替
for k, v in s:
	d1[k].append(v)
print d1
print d1.get("blue")