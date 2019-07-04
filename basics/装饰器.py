# coding:utf-8

# 装饰器

from functools import wraps
import time


def w(func):
    @wraps(func)
    def bibao(*args, **kw):
        if kw:
            ret = func(*args, **kw)
            return ret
        else:
            return func(a=2)

    return bibao


@w
def aaa(a):
    return a


print(aaa(a=1))
print(aaa())
# 不加上面的 @wraps(func),会打印bibao
print(aaa.__name__)


def wrapp(a):
    def bibao1(func):
        def bibao(n):
            print('%d %5d %s' % (a, func(n), 3))

        return bibao

    return bibao1


@wrapp(a=1)
def func1(n):
    return n


f1 = func1(2)  # 1 2 3


###
def wrapp1(func):
    def bibao():
        print(func())

    return bibao


@wrapp1
def func2():
    return 1


func2()


##
def wrapp2(var):
    def bibao(func):
        def bibao1(a, b):
            # print x,y
            if var > 10:
                a = 1
                b = 2
                return func(a, b)
            else:
                a = 2
                b = 3
                return func(a, b)

        return bibao1

    return bibao


@wrapp2(10)
def func3(x, y):
    print(x + y)


func3(2, 3)


##
def wrapp3(cls):
    def bibao(*a):
        a = cls(*a)
        return a.test()

    return bibao


@wrapp3
class cls(object):
    def __init__(self, *a):
        # super(cls, self).__init__()
        self.a = a

    def test(self):
        print(self.a)


c = cls(1)

print("===" * 50)


def output(name):
    print("name:%s" % name)

    def out(fun):
        def inner(*args, **kwargs):
            start = time.time()
            a = fun(*args, **kwargs)  ## 这里已经执行了 time.sleep(2)
            end = time.time()
            print(end - start)  # 由于上面执行了，所以这里是2秒
            return a  # 这里需要上面都执行完才会返回，this is f args:1 在最后

        return inner

    return out


@output(name="abc")
def f(aa):
    time.sleep(2)
    return "this is f args:%s" % aa


a = f(1)
print(a)
print("===" * 50)


class C(object):
    fns = []

    @staticmethod
    def commons(arg):
        def abc(fn):
            C.fns.append((fn(arg), fn.__name__))

        return abc

    @staticmethod
    def commons1(fun):
        C.fns.append((fun, fun.__name__))


@C.commons("1")  # 这里会直接调用 ，不需要额外调用
def func(s):
    return s


@C.commons1
def func1(s):
    return s

from inspect import isfunction
a = [ x(1) for x, _ in C.fns if isfunction(x)]
print(a)
