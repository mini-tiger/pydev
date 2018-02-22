# coding:utf-8
from jinja2 import Environment, PackageLoader

import os
print os.getcwd()
env = Environment(loader=PackageLoader('explame1', 'template'))
template = env.get_template('index.html')
print template.render(abc='variables', aaa='here')