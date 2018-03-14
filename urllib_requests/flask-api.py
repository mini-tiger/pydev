# -*- coding: utf-8 -*-
import requests,json
class util(object):
	def util_myapi(self,url,method='get',json=None,data=None):
	    headers = {'Accept': "application/json"}##定义header头，用dict方式定义，即3
	    url= url if url.rfind('/',-2) > 0 else url+'/'  #如果结尾 不是/
	    res = requests.request(method,url,headers=headers,json=json,data=data)
	    if res.status_code == 500:
	    	print res
	    	print dir(res)
	    else:
	    # res = requests.get(url,headers=headers, auth=('admin','admin' ))
	    	return res.text



#instance
uu=util()

url = 'http://127.0.0.1:8000/api/v1.0/'

#views ex_tasks   get 

# s=uu.util_myapi(url)
# print s




# ## views  ex_tasks  put
# j={
#     "title": "",
#     "code": "foo = \"bar\"\n",
#     "linenos": 'false',
#     "language": "python",
#     "style": "friendly"
# }

# print uu.util_myapi(url=url,method='PUT',json=j)#json=j or data=j

#views get_tasks_urlpath
s=uu.util_myapi(url+'get_tasks_urlpath/')
print s