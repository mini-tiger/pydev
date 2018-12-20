# coding:utf-8
from memory_profiler import profile
from collections import namedtuple


class people:
	name = ''
	age = 0
	__weight = 0

	def __init__(self, n, a, w):
		self.name = n
		self.age = a
		self.__weight = w

	@profile(precision=4)
	def speak(self):
		a = 'a' * 1024
		b = 'b' * 1024 * 1024
		print("%s is speaking: I am %d years old" % (self.name, self.age))
		del a, b
		print(u"dict namedtuple 内存哪个占用多")

		NewNamedTuple()  # namedtuple 高一些，dict 也可以直接比较
		NewDict()

def NewDict():
	l = list()
	for i in range(10000):
		ad = dict()
		ad.setdefault("name", "a")
		ad.setdefault("addr", "bj")
		ad.setdefault("old", "18")
		l.append(ad)
	print(len(l))
	del l


def NewNamedTuple():
	ll = list()
	city = namedtuple('city', 'name addr old')
	for i in range(10000):
		an = city('a', 'bj', 18)
		ll.append(an)
	print(len(ll))
	del ll


if __name__ == '__main__':
	p = people('tom', 10, 30)
	p.speak()
