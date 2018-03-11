# coding:utf-8

import random
import string


list_ex = lambda x: random.sample(string.digits + string.letters, x)

str_ex = lambda x:''.join(list_ex(x))

dict_ex= lambda x:dict(zip(list_ex(x), list_ex(x)))

set_ex= lambda x:set(list_ex(x))