from __future__ import print_function
import random
import time

with open("c:\\test.log", "r") as f:
	print(f.readlines())

x = lambda: time.time()
s = "abc"


def dd():
	for i in range(1, 10):
		for j in range(1, i + 1):
			print("%d * %d = %d \t" % (j, i, i * j), end="")
		print()


if __name__ == "__main__":
	print(x())
	dd()
