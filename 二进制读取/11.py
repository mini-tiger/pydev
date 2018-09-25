# coding=utf-8
import struct

with open("bin_python_slice_file.txt", "rb") as f:
	data = f.read(6)  # 这样data是一个b开头的ASCII数字。
	a = struct.unpack('<2s2s2s', data)
	print(a)  # 将二进制数据转化为10进制数据。
