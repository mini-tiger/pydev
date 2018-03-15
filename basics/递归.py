# coding:utf-8


def jisuan(n, num):
    if n <= 0:
        print '除尽用了{}次'.format(num)
        global a
        a = num
        return num  # 不能返回num,只能赋值全局变量

    n = n // 2
    num += 1
    print num
    jisuan(n, num)

jisuan(100, 0)
print a

print '**' * 50

###使用生成器代替 jisuan
def generator_ex(n, num=0):
    while True:
        if n <= 0:
            print '除尽用了{}次'.format(num)
            raise StopIteration
        n = n // 2
        num += 1
        yield num

g = generator_ex(100)
for i in g:
    print i


print '**' * 50

mylist = [1, 2, [1, 1, 1], [3, 4], 3, [1, 2]]


def func1(l, result):
    if not l:
        return result  # 如果列表没有元素 返回
    for i in l:
        if isinstance(i, list):  # 如果是列表
            # result = func1(i,result)   ## 结果返回给result
            result += sum(i)
        else:
            result += i  # 不是列表 加法
    return result

r = func1(mylist, result=0)
print r

