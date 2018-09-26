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