L=range(10)

print(list(map(lambda x:x+1,L)))

print(list(filter(lambda x:x%2==0,L)))


d1=dict()
d2=dict()
d1.setdefault("a",[1,3])
d2.setdefault("a",[1,2])
print(d1==d2)

print("this is %s ,and %s"%(1,2))

print("this is {0}, and {1}".format(1,2))

print("网站名：{name}, 地址 {url}".format(name="菜鸟教程", url="www.runoob.com"))

# 通过字典设置参数
site = {"name": "菜鸟教程", "url": "www.runoob.com"}
print("网站名：{name}, 地址 {url}".format(**site))

# 通过列表索引设置参数
my_list = ['菜鸟教程', 'www.runoob.com']
print("网站名：{0[0]}, 地址 {0[1]}".format(my_list))  # "0" 是必须的