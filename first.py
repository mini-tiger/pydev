from __future__ import print_function
import random
import time

# with open("c:\\test.log", "r") as f:
# 	print(f.readlines())
#
x = lambda: time.time()
# s = "abc"


def dd():
	for i in range(1, 10):
		for j in range(1, i + 1):
			print("%d * %d = %d \t" % (j, i, i * j), end="")
		print()

def wrapp(a):
	def bibao1(aa):
		def bibao(b):
			print(aa(b))
			print(1)
			print(b)
		return bibao
	return bibao1

@wrapp(1)
def abc(b):
	return 123


abc(3)

if __name__ == "__main__":
	# print(x())
	# dd()
	if 1==1:
		print(1)

