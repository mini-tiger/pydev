# -*- coding: utf-8 -*-
import requests
def util(url):
    headers = {'Accept': "application/json"}##定义header头，用dict方式定义，即3

    res = requests.get(url,headers=headers, auth=('admin','admin' ))
    return str(res.text)

view_name='myapi'

url = 'http://127.0.0.1:8000/%s/'%view_name ##定义http请求的地址，即1


headers = {'Accept': "application/json"}##定义header头，用dict方式定义，即3

res = requests.get(url,headers=headers, auth=('admin','admin' ))
s=str(res.text)
print s
true='true'
false='false'
for i in eval(s):
    print util(url=url+str(i.get('id')))