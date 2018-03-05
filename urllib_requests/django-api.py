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

url = 'http://127.0.0.1:8000/myapi/'

##print db data

# s=uu.util_myapi(url)
# for i in json.loads(s):
# 	print uu.util_myapi(url=url+str(i.get('id')))




## create db data
# j={
#     "title": "",
#     "code": "foo = \"bar\"\n",
#     "linenos": 'false',
#     "language": "python",
#     "style": "friendly"
# }

# print uu.util_myapi(url=url,method='post',json=j)#json=j or data=j

# edit db data
# jid=11
# j={
#     "title": "111",
#     "code": "foo = \"bar\"\n",
#     "linenos": 'false',
#     "language": "python",
#     "style": "friendly"
# }

# print uu.util_myapi(url=url+str(jid),method='PUT',json=j)

# delete db data
jid=11

print uu.util_myapi(url=url+str(jid),method='delete')