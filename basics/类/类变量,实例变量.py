class A(object):
	cls_a = 1

	def __init__(self):
		A.cls_a += 1

# todo 类变量 类似是 实例中的共享变量

print(A.cls_a)  # 没有实例化前 是 1
a1 = A()  # 执行了两次加1
a2 = A()
print(a1.cls_a)  # 3
print(a2.cls_a)  # 3

