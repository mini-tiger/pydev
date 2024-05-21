# import platform
# import sys
#
# # 获取 Python 版本号
# python_version = sys.version.split()[0]
#
# # 获取 Python 位数
# python_bits = platform.architecture()[0]
#
# print("Python Version:", python_version)
# print("Python Architecture:", python_bits)
# import platform

import re
s="章节: [第十章 数字治理的未来展望] ,小节 [第二节  数字治理的创新趋势] 完成"
sub_match = re.search(r'\[第(\S+)节\s+(\S+)\]', s)
print(sub_match.group(1))
print(sub_match.group(2))