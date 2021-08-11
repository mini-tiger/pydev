# coding:utf-8

# 装饰器

from functools import wraps


def mydec(func):
    @wraps(func)
    def mywrap(*args, **kw):
        print('hello this is decorator1')
        func(*args, **kw)

    return mywrap


@mydec
def hello_world():
    pass


# xxx 等价于执行mydec(hello_world)()
cur = mydec(hello_world)
cur()

print("===" * 50)


def mydec1(type_=None):
    def decorate(func):
        @wraps(func)
        def mywrap():
            if type_ is not None:
                print(type_)
            func()

        return mywrap

    return decorate


@mydec1(type_='test2')
def helloWorld():
    print('hello, world')


# xxx 等价于执行下面
cur1 = mydec1('test1')
cur2 = cur1(helloWorld)
cur2()

print("*" * 100)
# 有返回值

import time, random


def fun_retry_more(number=3, wait_time=2):
    def fun_retry(fun):
        @wraps(fun)  # 保留元信息  __name__ __doc__
        def retry(*args, **kwargs):
            # 重试次数
            for _ in range(number):
                print("Try the %d retry" % (_))
                try:
                    re_v = fun(*args, **kwargs)
                except:
                    time.sleep(wait_time)
                else:  # 如果成功运行
                    break
            return re_v

        return retry

    return fun_retry


@fun_retry_more(5, 1)
def ops(a, b="3.8"):
    """
    func ops
    """
    print("Run Func ops Version %s %s" % (a, b))
    if random.randint(1, 7) < 5:
        raise False
    return "Finish Func ops Version %s %s" % (a, b)


if __name__ == "__main__":
    print(ops.__name__)
    print(ops.__doc__)
    re_v = ops("python")

    print(re_v)
