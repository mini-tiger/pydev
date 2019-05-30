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

print_func("super方法类继承顺序")
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