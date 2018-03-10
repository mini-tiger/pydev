# coding:utf-8

import random
import string


list_ex = lambda x: random.sample(string.digits + string.letters, x)

str_ex = lambda x:''.join(list_ex(x))

if __name__ == "__main__":
    print list_ex(10)
    print str_ex(10)
