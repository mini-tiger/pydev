# coding:utf-8

try:
#	1 / 0
	with open('11123.txt','rb') as f:
		f.read(0)
except ZeroDivisionError as e:
	print '除数不能为0'

except IOError as e:
	print '没有这个文件'
except Exception as e:
	print '其它错误'
else:
	print '没有错误'
finally:
	print '完毕'

##自定义异常
#方法一:
class myerr(Exception):
	def __init__(self,err='1111'):
		super(myerr, self).__init__()
		# Exception.__init__(self)

		self.err=err
	def __str__(self):
		return self.err


try:
	raise myerr('1')   
except myerr as e:
	print e


#方法二
try:
	raise Exception("hello exception")
except Exception as e:
	print e