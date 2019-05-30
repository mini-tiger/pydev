# -*- coding: utf-8 -*-
# Python 2.x中默认都是经典类，只有显式继承了object才是新式类
# Python 3.x中默认都是新式类，不必显式的继承object
# 其次：
# ------新式类对象可以直接通过__class__属性获取自身类型:type
# ------继承搜索的顺序发生了改变,
# 经典类多继承属性搜索顺序: 先深入继承树左侧，再返回，开始找右侧;
# 新式类多继承属性搜索顺序: 先水平搜索，然后再向上移动
#
# ------新式类增加了__slots__内置属性, 可以把实例属性的种类锁定到__slots__规定的范围之中\
# ------新式类增加了__getattribute__方法



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

print_func("super 新式方法类继承顺序")
class A(object):
    def go(self):
        print("go A go!")
    def stop(self):
        print("stop A stop!")
    def pause(self):
        raise Exception("Not Implemented")

class B(A):
    def go(self):
        super(B, self).go()
        print("go B go!")

class C(A):
    def go(self):
        super(C, self).go()
        print("go C go!")
    def stop(self):
        super(C, self).stop()
        print("stop C stop!")

class D(B,C):
    def go(self):
        super(D, self).go()
        print("go D go!")
    def stop(self):
        super(D, self).stop()
        print("stop D stop!")
    def pause(self):
        print("wait D wait!")

class E(B,C):
    pass

d=D()
d.go()
# go A go!
# go C go!
# go B go!
# go D go!