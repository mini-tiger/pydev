# coding=utf-8
import struct,os

d = r"C:\work\go-dev\src\godev\basic"

with open(os.path.join(d,"bin_python_slice_file.txt"), "rb") as f:
	data = f.read(22)
	a = struct.unpack('<2s2s2s2i', data)
	print(a)  # 将二进制数据转化为10进制数据。
	# data = f.read(16)
	# a = struct.unpack('<i', data)
	# print(a)  # 将二进制数据转化为10进制数据。
# todo 格式说明
# https://blog.csdn.net/shudaqi2010/article/details/78133120
# https://blog.csdn.net/zhongbeida_xue/article/details/79026333