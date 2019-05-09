from copy import deepcopy
import itertools
l1=range(0,2)
l2=range(0,3)
l3=list(l1)+list(l2)
l3.sort()
print(l3)
for key, group in itertools.groupby(l3):  ## 返回分组, 连续相同的 元素，以及元素出现的生成器
	print (key, list(group))




