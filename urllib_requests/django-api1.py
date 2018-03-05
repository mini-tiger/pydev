# -*- coding: utf-8 -*-
import requests,json
def util(url,method='get',data=None,json=None):
    headers = {'Accept': "application/json"}##定义header头，用dict方式定义，即3

    res = requests.request(method,url,headers=headers,data=data,json=json)
    print res.status_code
    return res.text

view_name='myapi_list/'
url='http://127.0.0.1:8000/'
url1 = url+view_name ##定义http请求的地址，即1

#query
# res = util(url=url1)
# j=json.loads(res)
# for i in j:
#     print util(url=url+'myapi_detail/'+str(i.get('id')))



# create
# j={"title": "16",
#     "code": "foo = \"bar\"\n",
#     "linenos": 'false',
#     "language": "python",
#     "style": "friendly"
# }
# r=util(method='post',url=url1,data=j)
# print r

# update
# j={"title": "",
#     "code": "foo = \"bar\"\n",
#     "linenos": 'false',
#     "language": "python",
#     "style": "friendly"
# }
# r=util(method='put',url=url+'myapi_detail/15/',data=j)
# print r

##delete
r=util(method='delete',url=url+'myapi_detail/17/')
print r