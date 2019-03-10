import copy
b = ["h", "e", "l", "l", "o"]


def func(b):
	a=copy.deepcopy(b)
	print(a,b)
	print(id(a), id(b))

	print(b == a)
	print(a is b)


if __name__ == "__main__":
	func(b)
