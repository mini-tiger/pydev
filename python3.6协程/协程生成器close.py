# 在并发高，连接活跃度不高的情况下，Epoll 比Select 好
# 在并发不高，连接活跃度高的情况 下，select 比epool 好


import random, time


def genNum():
    for i in range(0,5):
        yield i


if __name__ == "__main__":
    g = genNum()
    print(next(g))  # todo 第一次启动生成器必须要用next()或者 g.send(None)
    print(next(g))
    g.close() # 关闭以后，无论是不是生成器执行完成，都会stopIteration
    try:
        next(g)
    except StopIteration as e:
        print("error : stop")

