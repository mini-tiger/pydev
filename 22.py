import os

def test(*arg,**kwarg):
	def wrap(func):
		def warp1(*arg):
			print arg
			print kwarg
			return 11111
			print func(arg)
		return warp1
	return wrap



@test(11,22,aa=11)
def func(*arg):
	return 1


print func(1,2)
import sys
print sys.path
from basics import baseic
print baseic.create_str(2)
print baseic.__name__