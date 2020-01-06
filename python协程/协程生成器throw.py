# 在并发高，连接活跃度不高的情况下，Epoll 比Select 好
# 在并发不高，连接活跃度高的情况 下，select 比epool 好


import random, time


def genNum():
    yield 1
    try:
        yield 2
    except Exception as e:
        print("error exception")
    yield 3

if __name__ == "__main__":
    g = genNum()
    print(next(g))  # todo 第一次启动生成器必须要用next()或者 g.send(None)
    print(next(g))  # 这里是 yield 2
    try:
        g.throw(Exception, "create err") # todo 这里是在 yield 2的位置，也就是不往下 到  yield 3

    except StopIteration as e:
        print("error : stop")

