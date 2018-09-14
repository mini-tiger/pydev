
import requests,json

#TODO:step
# params = {
# 	"start_time": start,
# 	"end_time": end,
# 	"consol_fun": cf,
# 	"hostnames": endpoints,
# 	"counters": counters,
# }
h = {"Content-type": "application/json"}
params = {'counters': [u'agent.alive'], 'start_time': 1536890032, 'hostnames': [u'falcon-win12-1'], 'end_time': 1536893512, 'consol_fun': u'AVERAGE'}
r = requests.post("http://192.168.43.26:8080/api/v1/graph/history", data=json.dumps(params),headers=h )

if r.status_code != 200:
	raise Exception("%s : %s" %(r.status_code, r.text))

print r.json()