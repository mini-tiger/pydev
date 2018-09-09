# coding:utf-8
from collections import deque
# 类似有顺序的list

# 可以插入到后面 ，前面
# 从后面或前面提取
d = deque(range(10))
print d

d.append(00) # 后面插入
d.appendleft(11) # 前面插入

print d # deque([11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0])

print d.pop()  # 0
print d.popleft() # 11
print d # deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])