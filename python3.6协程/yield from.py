# def my_chain(*args):
#     for my_iter in args:
#         yield from my_iter # todo 可异步 返回 my_iter 可迭代对象的元素
#         # for v in my_iter:
#         #     yield v
#
#
# for value in my_chain([1, 2, 3], {"a": 1, "b": 2}, range(0, 3)):
#     print(value)


import random, time


def genNum(n):
	for i in range(0, n):
		n = yield random.randint(0, 10)  # 使用send方法，这里每次都会被覆盖
		print(n)
		m = yield 3
		print(m)
		print("this is random int", n, m, i)


def g1(gen):
	yield from gen


def main():
	g = g1(genNum(5))
	g.send(None)
	g.send(1)  # 覆盖第一个yield
	g.send(2)  # 覆盖第二个yield


# main 是调用方 ，g1 是委托生成器，gen 是子生成器
# yield form 会在调用方与 子生成器之间 ，建立 双向通道， 透过g1,send,throw方法发送过去


if __name__ == "__main__":
	# main()
	main()
