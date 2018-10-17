# coding:utf-8
from collections import OrderedDict

# 有序key字典

d1 = {}
d1["a"] = 1
d1["b"] = 2
d1["c"] = 3
print d1  # 顺序不固定

d2 = OrderedDict()
d2["a"] = 1
d2["b"] = 2
d2["c"] = 3
print d2  # 按照key插入顺序固定
