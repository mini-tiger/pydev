# -*- coding: utf-8 -*-
from blueking.component.client import ComponentClient  # APP应用ID

bk_app_code = "bk1"
# APP安全密钥
bk_app_secret = "c50f40fe-c35b-4a23-89cd-5591b4d55bf0"
# 用户登录态信息
# common_args = {'bk_token': 'xxx'}
common_args = {'bk_username': 'admin',"app_id":1}
# APP应用ID和APP安全密钥如未提供，默认从django settings中获取
client = ComponentClient(app_code=bk_app_code, app_secret=bk_app_secret, common_args=common_args)
# 参数

j={
    "ip": {
        "data": [],
        "exact": 1,
        "flag": "bk_host_innerip"
    },
    "condition": [
        {
            "bk_obj_id": "host",
            "fields": [],
            "condition": []
        },
        {
            "bk_obj_id": "object",
            "fields": [],
            "condition": [
                {
                    "field": "bk_host_id",
                    "operator": "$neq",
                    "value": 0
                }
            ]
        }
    ],
    "page": {
        "start": 0,
        "limit": 100,
        "sort": "bk_host_name"
    },
    "pattern": ""
}


kwargs = {'bk_biz_id': 2}
result = client.cc.get_app_host_list(j)
print result
# if __name__ == "__main__":
