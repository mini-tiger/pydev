# coding:utf-8

ti = '''题目:有四个数字：1、2、3、4，能组成多少个互不相同且无重复数字的三位数？各是多少？'''
print("{:<106}".format(ti))

# 方法一
l = []
for i in xrange(1, 5):
    for m in xrange(1, 5):
        for n in xrange(1, 5):
            if i != m and i != n and m != n:
                l.append(i * 100 + m * 10 + n)
print l

# 方法二
list_num = xrange(1, 5)
l = [i * 100 + j * 10 +
     k for i in list_num for j in list_num for k in list_num if (j != i and k != j and k != i)]

print l

from itertools import permutations
l = permutations(xrange(1, 5), 3)  # (1,2,3),(1,2,4)....
print map(lambda (x, y, z): x * 100 + y * 10 + z, l)

print
print
ti = '''题目：企业发放的奖金根据利润提成。利润(I)低于或等于10万元时，奖金可提10%；利润高于10万元，低于20万元时，低于10万元的部分按10%提成，高于10万元的部分，可提成7.5%；20万到40万之间时，高于20万元的部分，可提成5%；40万到60万之间时高于40万元的部分，可提成3%；60万到100万之间时，高于60万元的部分，可提成1.5%，高于100万元时，超过100万元的部分按1%提成，从键盘输入当月利润I，求应发放奖金总数？ '''
print("{:<106}".format(ti))

x = 500001  # 利润

if x <= 100000:
    bonus = x * 0.1
    print u"奖金:", bonus, u"元"
elif 100001 < x <= 200000:
    bonus = 10000 + (x - 100000) * 0.075
    print u"奖金:", bonus, u"元"
elif 200001 < x <= 400000:
    bonus = 10000 + 7500 + (x - 200000) * 0.05
    print u"奖金:", bonus, u"元"
elif 400001 < x <= 600000:
    bonus = 10000 + 7500 + 10000 + (x - 400000) * 0.03
    print u"奖金:", bonus, u"元"
elif 600001 < x <= 1000000:
    bonus = 10000 + 7500 + 10000 + 6000 + (x - 600000) * 0.015
    print u"奖金:", bonus, u"元"
elif 600001 < x <= 1000000:
    bonus = 10000 + 7500 + 10000 + 6000 + 6000 + (x - 600000) * 0.01
    print u"奖金:", bonus, u"元"

print
print
ti = '''题目：输入某年某月某日，判断这一天是这一年的第几天？'''
print("{:<106}".format(ti))
# 方法一
import time
import datetime
d = '2017-1-5'

timeArray = time.strptime(d, "%Y-%m-%d")

d1 = d.split('-')  # 转换为2017-1-1
d1[1] = '1'
d1[2] = '1'
d1 = '-'.join(d1)

timeArray1 = time.strptime(d1, "%Y-%m-%d")
tt = int(time.mktime(timeArray))
tt1 = int(time.mktime(timeArray1))

print(tt - tt1) / 86400 + 1

# 方法二
t = time.strptime(d, "%Y-%m-%d")
print time.strftime("今年的第%j天", t)  # %j  一年第几天


print
print
ti = '输入三个整数x,y,z，请把这三个数由小到大输出'
print("{:<106}".format(ti))

x = 2
y = 1
z = 100
l = [x, y, z]
l.sort()


ti = '输出 9*9 乘法口诀表'
print("{:<106}".format(ti))
# 方法一
for i in xrange(1, 10):
    print
    for j in xrange(1, i + 1):
        print '{0} * {1} = {2} ;'.format(i, j, i * j),
print
print
ti = '打印出所有的"水仙花数"，所谓"水仙花数"是指一个三位数，其各位数字立方和等于该数本身。例如：153是一个"水仙花数"，因为153=1的三次方＋5的三次方＋3的三次方。'
print("{:<106}".format(ti))

for i in range(100, 999):
    b = str(i)[0]
    s = str(i)[1]
    g = str(i)[2]
    if int(b)**3 + int(s)**3 + int(g)**3 == i:
        print i

print
print
ti = '输入一行字符，分别统计出其中英文字母、空格、数字和其它字符的个数'
print("{:<106}".format(ti))
# 方法一
s = '111111112dsfxfdhndfxfdftt33123  d e13'

import re
r = re.compile('[0-9]')
print 'digits {} '.format(str(len(re.findall(r, s))))


r = re.compile('[a-zA-Z]')
print 'ascii_letters {} '.format(str(len(re.findall(r, s))))


r = re.compile('\s')
print '空格 {} '.format(str(len(re.findall(r, s))))
# 方法二
letters = 0
space = 0
others = 0
digit = 0

for c in s:
    if c.isalpha():
        letters += 1
    elif c.isspace():
        space += 1
    elif c.isdigit():
        digit += 1
    else:
        others += 1

print 'digit {} ,letters {},space {}'.format(digit, letters, space)

ti = '求s=a+aa+aaa+aaaa+aa...a的值，其中a是一个数字。例如2+22+222+2222+22222(此时共有5个数相加)，几个数相加由键盘控制'

print
print
print("{:<106}".format(ti))

s = '2'
n = 5  # ('几位叠加:')
# 方法一
ss = 0
for i in xrange(1, n + 1):
    _s = s * int(i)
    print '数字: {}'.format(_s)
    ss += int(_s)

print 'result : {}'.format(ss)

# 方法二
_l = []
for i in xrange(1, n + 1):
    _s = s * int(i)
    print '数字: {}'.format(_s)
    _l.append(int(_s))

print 'result : {}'.format(sum(_l))


ti = '20, 一球从100米高度自由落下，每次落地后反跳回原高度的一半；再落下，求它在第10次落地时，共经过多少米？第10次反弹多高？'

print
print
print("{:<106}".format(ti))


global hight, totle


def luo(hight, n, totle):
    print hight, n, totle
    if hight <= 0 or n == 10:
        return hight, n
    else:

        n += 1
        totle += hight
        hight = luo(hight / 2, n, totle)


luo(100.0, 0, totle=100)  # 总高度 100 起始


ti = '21, 猴子吃桃问题：猴子第一天摘下若干个桃子，当即吃了一半，还不瘾，又多吃了一个第二天早上又将剩下的桃子吃掉一半，又多吃了一个。以后每天早上都吃了前一天剩下的一半零一个。到第10天早上想再吃时，见只剩下一个桃子了。求第一天共摘了多少'

print
print
print("{:<106}".format(ti))

global geshu, cishu, totle


def luo(geshu, cishu):
    print geshu, cishu
    if cishu == 1:
        return
    else:
        cishu -= 1
        geshu = luo((geshu + 1) * 2, cishu)


luo(*(1, 10))

ti = '22, 两个乒乓球队进行比赛，各出三人。甲队为a,b,c三人，乙队为x,y,z三人。已抽签决定比赛名单。有人向队员打听比赛的名单。a说他不和x比，c说他不和x,z比，请编程序找出三队赛手的名单'

print
print
print("{:<106}".format(ti))

_l = []
for i in ('a', 'b', 'c'):
    for l in ('x', 'y', 'z'):
        if (i == 'a' and l == 'x') or (i == 'c' and l in ('x', 'z')):
            continue
        else:
            _l.append((i, l))
print _l

ti = '打印出如下图案（菱形）:'
'''
   *
  ***
 *****
*******
 *****
  ***
   *
'''
print
print
print("{:<106}".format(ti))


_list = range(1, 8, 2)

for i in _list:
    s = '*' * i
    print("{:^10}".format(s))

_list.pop(-1)

for i in sorted(_list, reverse=True):
    s = '*' * i
    print("{:^10}".format(s))


ti = 'NO.24 有一分数序列：2/1，3/2，5/3，8/5，13/8，21/13...求出这个数列的前20项之和'

print
print
print("{:<106}".format(ti))

_l = []

a=1
def fe(s1, s2, n, _l):
    # print s1, s2
    if n == 20:
        return
    n += 1

    _s = s2  # 暂存一下 s2 后面那个数的值
    s2 = s1 + s2  # 后面的数  等于前面数相加
    s1 = _s  # 前面数 等于  没加之前的，后面那个数
    _l.append(s1)
    s2 = fe(s1, s2, n, _l)


_l.append(1)

fe(1, 2, 1, _l)  # 分母
from copy import deepcopy

fenmu = deepcopy(_l)

_l = []
_l.append(2)
fe(2, 3, 1, _l)  # 分子

fenzi = deepcopy(_l)

sum = 0
for m, n in zip(fenzi, fenmu):
    sum += (float(m) / n)

print fenzi
print fenmu
print sum

ti = 'NO.27 利用递归函数调用方式，将所输入的5个字符，以相反顺序打印出来。'

print
print
print("{:<106}".format(ti))
# 方法一
a = [2, 5, 8, 4, 5]
print a[::-1]
# 方法二


def reverse1(l):
    if not l:
        return
    print l.pop(-1)
    reverse1(l)


reverse1(a)

ti = '''
NO.28 有5个人坐在一起，问第五个人多少岁？他说比第4个人大2岁。问第4个人岁数，他说比第3个人大2岁。问第三个人，又说比第2人大两岁。问第2个人，说比第一个人大两岁。最后问第一个人，他说是10岁。请问第五个人多大？
程序分析：利用递归的方法，递归分为回推和递推两个阶段。要想知道第五个人岁数，需知道第四人的岁数，依次类推，推到第一人（10岁），再往回推'''

print
print
print("{:<106}".format(ti))

# 方法一


def n(x, y, z): return x + y * z  # x起始10岁，还有4个人，每个人差2岁


print n(10, 4, 2)


# 方法二

def nnn(x, n):
    n += 1
    if n == 5:
        return x

    x = n * 2 + 10
    return nnn(x, n)


print nnn(0, 1)


ti = '''
NO.29 给一个不多于5位的正整数，要求：一、求它是几位数，二、逆序打印出各位数字
'''

print
print
print("{:<106}".format(ti))

n = 12345
sn = str(n)
print '{} 位数'.format(len(sn))

r = range(len(sn))
r.sort(reverse=True)

for i in r:
    print str(n)[i]


ti = '''
NO.30 一个5位数，判断它是不是回文数。即12321是回文数，个位与万位相同，十位与千位相同。
'''

print
print
print("{:<106}".format(ti))

import random
import string


def n(x): return random.sample(string.digits, x)


l = [str(''.join(n(5))) for x in range(10)]

print l  # 生成 若干个五位数 字符串
l.append('12321')  # 添加一个 回文数，防止没有随机生成

ll = filter(lambda x: int(x[-1]) == int(x[0]) and int(x[-2]) == int(x[1]), l)
print ll
