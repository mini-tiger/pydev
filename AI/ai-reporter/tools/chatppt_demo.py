import requests
resp=requests.request("PUT", "http://120.133.83.166:9001", timeout=10)
print(resp)