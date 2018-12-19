# coding:utf-8
print "*" * 20 + "__slots__" + "*" * 20


class A(object):
	__slots__ = ["a", "b"]  # todo 只能定义已经定义好的变量
	v = 1  # todo 类变量不受影响

	def __init__(self):
		self.a = 1
		self.b = 2


a1 = A()
try:
	a1.c = 2
except Exception as e:
	print "This is a1.c Err: %s" % str(e)


class B(A):
	pass


b1 = B()
b1.c = 2  # todo 子类不受影响

print "*" * 20 + "del" + "*" * 20

