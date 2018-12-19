# coding:utf-8
from memory_profiler import profile


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


if __name__ == '__main__':
	p = people('tom', 10, 30)
	p.speak()
