# env python 3.6
# 1. 前面 是u
# 作用：后面字符串以 Unicode 格式 进行编码，一般用在中文字符串前面，防止因为源码储存格式问题，导致再次使用时出现乱码
print("abc")
print("abc中文")
print(u"abc中文")

# 2. 前面是 r
# 作用：声明后面的字符串是普通字符串，相对的，特殊字符串中含有：转义字符 \n \t 什么什么的。
print("\n\tabc")
print(r"\n\t abc")

# 3. 前面是 b
# 作用：python3.x里默认的str是unicode类,
#
# py2.x的str是 bytes类,
#
# xxx b“我(python 3)的str是 bytes” 代表的就是bytes类 。
#
# python2.x里, b前缀没什么具体意义， 只是为了兼容python3.x的这种写法
print(b"abc")
print("abc")

# todo 3. 前面是 f
# 作用 : 字符串格式化（python 3.6 新增),执行内容
vers = 'python3.6'
print(f"Hello , {vers}")
print(f"Hello , {vers.upper()}")

print(f"{2 * 3}")  # 6


class Comedian:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def __str__(self):
        return f"{self.first_name} {self.last_name} is {self.age}."

    def __repr__(self):
        return f"{self.first_name} {self.last_name} is {self.age}. Surprise!"


new_comedian = Comedian("Eric", "Idle", "74")
print(f"{new_comedian}")  # __str__
print(f"{new_comedian!r}")  # __repr__
