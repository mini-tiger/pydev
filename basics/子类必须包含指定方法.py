import abc


class Foo(abc.ABC):
    @abc.abstractmethod
    def fun(self):
        pass


try:
    a = Foo()
except Exception as e:
    print(e)


# 实例化报错
# TypeError: Can't instantiate abstract class Foo with abstract methods fun
# 下面子类继承该方法
class Sub_foo(Foo):
    def f(self):
        print('This is sub foo!')


try:
    c = Sub_foo()

except Exception as e:
    print(e)


# 子类并没有实现fun 方法，实例化子类sub_foo同样报错
# TypeError: Can't instantiate abstract class Sub_foo with abstract methods fun
# fixme 只有在在子类实现fun方法：
class Sub_foo(Foo):
    def fun(self):
        print("From sub_foo")

    def f(self):
        print('This is sub foo!')


c = Sub_foo()
c.fun()
c.f()
