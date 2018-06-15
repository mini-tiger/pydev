#-*- coding:utf-8 -*-
import sys
import urllib2
import requests
import json
# reload(sys)
# sys.setdefaultencoding('gbk')


class zabbixtools:

    # def items_get(self, hostid_list):
    #     for hostid in hostid_list:
    #         print hostid
    #         data = json.dumps({
    #             "jsonrpc": "2.0",
    #             "method": "item.get",
    #             "params": {
    #                 "output": ["hostid", "itemid", "key_", "name"],
    #                 "filter": {
    #                            "hostid": [
    #                                 hostid
    #                             ]
    #                 },
    #                 "search": {
    #                        "key_": "cpu",
    #                     "hostid": "1031"
    #                 },
    #             },

    #             "auth": self.authID,
    #             "id": 1,
    #         })

    #         request = urllib2.Request(self.url, data)
    #         for key in self.header:
    #             request.add_header(key, self.header[key])

    #         try:
    #             result = urllib2.urlopen(request)
    #         except urllib2.URLError as e:
    #             print "Auth Failed, Please Check Your Name AndPassword:", e
    #         else:
    #             response = json.loads(result.read())
    #             # print response
    #             # response=result.read()
    #             result.close()
    #             # print response
    #             list = response['result']
    #             print len(list)
    #             for k in list:
    #                 print k

    # def host_get(self, hostip=""):

    #     # Éú³Éjson¸ñÊ½Êý¾Ý
    #     data = json.dumps(
    #         {
    #             "jsonrpc": "2.0",
    #             "method": "host.get",
    #             "params": {
    #                 "output": [
    #                     "hostid",
    #                     "host"
    #                 ],
    #                 "selectInterfaces": [
    #                     "interfaceid",
    #                     "ip"
    #                 ]
    #             },
    #             "auth": self.authID,
    #             "id": 1
    #         })
    #     request = urllib2.Request(self.url, data)
    #     for key in self.header:
    #         request.add_header(key, self.header[key])

    #     try:
    #         result = urllib2.urlopen(request)
    #     except urllib2.URLError as e:
    #         print "Auth Failed, Please Check Your Name AndPassword:", e
    #     else:
    #         response = json.loads(result.read())
    #         # response=result.read()
    #         result.close()
    #         # print result
    #         list = response['result']
    #         for k in list:
    #             print k

    def __init__(self):
        self.url = "http://172.16.134.58/zabbix/api_jsonrpc.php"
        self.header = {'Accept': "application/json",
                       "Content-Type": "application/json"}
        self.method = 'post'
        # self.host_get()
        # self.hostgroup_get()

    def auth_token(self):
        auth_info = self.user_login()
        if auth_info.get('error'):
            print auth_info['error']
            return False
        else:
            self.authID = auth_info['result']
            return True

    def user_login(self, data=None):

        json_data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": "admin",
                    "password": "zabbix",
                    #"userData":  "true"
                },
                "id": 0,
            })
        # headers = {'Accept': "application/json"}##定义header头，用dict方式定义，即3
        try:
            res = requests.request(
                self.method, url=self.url, headers=self.header, data=json_data, timeout=5)
            # res  = requests.post(self.url,headers = self.header, data = json_data )
            # print res.text[]
            return res.json()
        except Exception as e:
            return {'error': str(e)}

    def host_get(self):

        json_data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": [
                        "hostid",
                        "host"
                    ],
                    "selectInterfaces": [
                        "interfaceid",
                        "ip"
                    ],
                    "filter": {
                        "status":0
                    },
                },
                "auth": self.authID,
                "id": 1
            })
        try:
            res = requests.request(
                self.method, url=self.url, headers=self.header, data=json_data, timeout=5)
            # res  = requests.post(self.url,headers = self.header, data = json_data )
            # print res.text[]
            # print res.json()
            hostid_list = map(lambda x: x['hostid'], res.json()['result'])
            # print hostid_list

            return hostid_list
        except Exception as e:
            print str(e)
            return {'error': str(e)}

    def items_get(self, hostid_list):
        for hostid in hostid_list:
            print hostid
            json_data = json.dumps({
                "jsonrpc": "2.0",
                "method": "item.get",
                "params": {
                    "output": ["hostid", "itemid", "key_", "name"],
                    "filter": {
                        "hostid": [
                            hostid
                        ]
                    },
                    "search": {
                        "key_": "cpu",
                        "hostid": hostid
                    },
                },

                "auth": self.authID,
                "id": 1,
            })

        try:
            res = requests.request(
                self.method, url=self.url, headers=self.header, data=json_data, timeout=5)
            # res  = requests.post(self.url,headers = self.header, data = json_data )
            # print res.text[]
            # print res.json()
            items_list = map(lambda x: x['itemid'], res.json()['result'])
            return {hostid: items_list}
        except Exception as e:
            print str(e)
            return {'error': str(e)}

    def Hostsitemsvalue(self, hostitems_dict):
        for hostid, items_list in hostitems_dict.items():
            # for item in items_list:
            # print items_list,type(items_list)
            json_data = json.dumps({'jsonrpc': '2.0',
                                    'method': "history.get",
                                    "params": {
                                        "output": "extend",
                                        "history": 3,
                                        "itemids": items_list,
                                        "sortfield": "clock",
                                        "sortorder": "DESC",
                                        "limit": len(items_list),
                                    },
                                    'auth': self.authID,
                                    'id': '6'
                                    })
        print self.requestJson(json_data)

    def requestJson(self, json_data):
        try:
            res = requests.request(
                self.method, url=self.url, headers=self.header, data=json_data, timeout=5)
            # res  = requests.post(self.url,headers = self.header, data = json_data )
            # print res.text[]
            # print res.json()
            # items_list = map(lambda x: x['itemid'], res.json()['result'])
            return res.json()
        except Exception as e:
            print str(e)
            return {'error': str(e)}

    def hostgroup_get(self):
        json_data = json.dumps({'jsonrpc': '2.0',
                                'method': 'hostgroup.get',
                                "params": {
                                    "output": "extend",
                                    'output': ['groupid', 'name']
                                    # "filter": {
                                    #     "name": [
                                    #        'Zabbix servers'
                                    #     ]
                                    # }
                                },
                                'auth': self.authID,
                                'id': '11'
                                })
        print self.requestJson(json_data)

    # 定义通过主机id获取开启关闭监控函数
    def hostidupdatehost(self, hostid, status):
        # 0 启动  1 停用
        json_data = json.dumps({'jsonrpc': '2.0',
                                'method': 'host.update',
                                'params': {
                                    "hostid": hostid,
                                    "status": status
                                },
                                'auth': self.authID,
                                'id': '4'
                                })
        print self.requestJson(json_data)

    # def user_login(self):  ##urllib 模块版本
    #     data = json.dumps(
    #         {
    #             "jsonrpc": "2.0",
    #             "method": "user.login",
    #             "params": {
    #                 "user": "admin",
    #                 "password": "zabbix",
    #                 #"userData":  "true"
    #             },
    #             "id": 0
    #         })
    #     request = urllib2.Request(self.url, data)
    #     user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    #     for key in self.header:
    #         request.add_header(key, self.header[key])

    #     try:
    #         result = urllib2.urlopen(request)
    #     except urllib2.URLError as e:
    #         print "Auth Failed, Please Check Your Name AndPassword:", e
    #     else:
    #         response = json.loads(result.read())
    #         # response=result.read()
    #         result.close()
    #     return response['result']


def main():
    test = zabbixtools()
    if test.auth_token():
        hostid_list = test.host_get()  # 主机id列表
        if isinstance(hostid_list, list):
            hostitems_dict = test.items_get(hostid_list)  # 主机下的 监控项
            if isinstance(hostitems_dict, dict):  # 监控项下 最近采集数据
                test.Hostsitemsvalue(hostitems_dict)
    test.hostgroup_get()
    test.hostidupdatehost(hostid_list[0], status=1)
    # test.host_get()
    # test.host_del()
    # test.host_create()
if __name__ == "__main__":
    main()
