# -*- coding: utf-8 -*-

def print_func(str):
	print("=" * 20 + str + "="*20)

class A(object):
	def show(self):
		print("A")


class B(object):
	def show(self):
		print("B")

	def SwitchType(self):
		self.__class__ = A

print_func("类的继承与类的属性")
b = B()
b.show()  # B
b.__class__ = A
b.show()  # A

b1 = B()
b1.SwitchType()
b1.show()  # A

print_func("类默认方法")

class AA(object):
	def __init__(self,*args):
		pass
	def default(self,*args):
		print(args)

	def __getattr__(self,name):
		print(name)
		return self.default

aa=AA()
aa.fn1(2)