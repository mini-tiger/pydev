import requests,json
dc="上海外高桥"
res=requests.request("GET",f"http://172.22.50.25:31857/dc/usage?dc_area={dc}")
print(json.loads(res.text))