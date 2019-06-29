import numpy as np

a = np.arange(12)
b = a  # 同一个内存地址
# a and b are two names for the same ndarray object
print(b is a)  #
b.shape = 3, 4
print(a.shape)
print(id(a))
print(id(b))

##
c = a.view()  # 浅复制 不是同一内存地址
print(c is a)  # false
c.shape = 2, 6
# print a.shape
c[0, 4] = 1234
print(a)

##
d = a.copy() # False
print(d is a)
d[0, 0] = 9999
print(d)
print(a)
