# coding:utf-8

import random
import string


list_ex = lambda x: random.sample(string.digits + string.letters, x)

str_ex = lambda x: ''.join(list_ex(x))


set_ex1 = (x for x in xrange(10) if x > 5)


if __name__ == "__main__":
    print list_ex(10)
    print str_ex(10)
    print set_ex1  # 生成器
    print [x for x in range(5) if x > 2 ]
    print {x:y for x,y in enumerate(list_ex(5))}
    print {x for x in range(5) if x > 2 }