#  -*- coding:utf-8 -*-
# File http_post.py

import urllib
import urllib2
import json


def http_post():
    url = 'http://127.0.0.1:8000/app_center/capsule_save'
    values = {
            "task_name": "测试任务1", "task_tag": "测试任务标签",
            "task_desc": "1", "app_id": 1, "user_id": 2,
            "task_detail":
                [{"vmid": 1,
                  "product_list":
                      [{"product_id": 3, "order": 1},
                       {"product_id": 4, "order": 2}]},
                 {"vmid": 7,
                  "product_list":
                      [{"product_id": 1, "order": 1}]}
                 ]}

    # url = 'http://172.16.134.123:8000/app_center/Capsule_save'
    # values = {"data": \
    # [
    # {"vmname": "vmdk-zabbix-3", "vmid": 1, \
    # "product_list": \
    # [{"product_name": "\u6570\u636e\u5e93", "product_id": 1}]}, \
    # {"vmname": "rpmbuild-lixx", "vmid": 2, \
    # "product_list":
    # [{"product_name": "web", "product_id":2}]}], \
    # "task_name": "测试任务","task_tag":"测试任务标签","task_desc":"",\
    # "app_id":1,"user_id":2}

    jdata = json.dumps(values)             # 对数据进行JSON格式化编码
    req = urllib2.Request(url, jdata)       # 生成页面请求的完整数据
    response = urllib2.urlopen(req)       # 发送页面请求
    return response.read()                    # 获取服务器返回的页面信息

resp = http_post()
print resp
