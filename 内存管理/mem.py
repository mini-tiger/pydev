# coding:utf-8
# pip install -U memory_profiler


# todo 运行方式 c:\Python27\python.exe -m  memory_profiler mem.py
'''
Line #    Mem usage(内存使用)    Increment（增长量）   Line Contents（代码行）
'''

from memory_profiler import profile


class A(object):
	__slots__ = ["a", "b"]  # todo 只能定义已经定义好的变量


# v = 1  # todo 类变量不受影响

# def __init__(self):
# self.a = 1
# self.b = 2


class AA(object):
	pass


# def __init__(self):
# 	self.aa = 3
# 	self.bb = 3


@profile(precision=4)  # 内存在小数点后几位
def my_func():
	a = [1] * (10 ** 6)
	b = [2] * (2 * 10 ** 7)
	del b
	del a
	aa2 = AA()
	aa1 = A()
	aa2.a = [1] * (10 ** 6)
	aa2.b = [1] * (10 ** 6)
	aa1.a = [1] * (10 ** 6)
	aa1.b = [1] * (10 ** 6)
	print u"加上__slots__参数的类，对于没有多加变量的类，没有少占内存"
	aa2.c = [1] * (10 ** 6)
	del aa1
	del aa2

@profile(precision=4)  # 内存在小数点后几位
def my_func1():
	a = [1] * (10 ** 6)
	a = [1] * (10 ** 6) # 不会叠加内存
	del a
	a = [1] * (10 ** 6)
	b = a # 这样是 两个变量引用同一个内存地址，不会增加内存
	del a # 删除一个，内存不用减
	del b

if __name__ == '__main__':
	print "*" * 20 + "slots" + "*" * 20
	my_func()
	print "*" * 20 + u"对象不删除，直接赋值内存是否会继续增长" + "*" * 20
	my_func1()