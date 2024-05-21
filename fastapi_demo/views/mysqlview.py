from typing import List, Set
from utils import resp  # 默认路径 fastapi-demo
from fastapi import params, requests
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from modules import mysqlconn


class mysqlfilterReq(BaseModel):
    tablename: str


async def mysqlfilter(req: mysqlfilterReq):
    print(req)
    print(jsonable_encoder(req))
    print(req.tablename)
    sql = "select * from {tablename}".format(**jsonable_encoder(req))
    print(sql)
    results = mysqlconn.selectAll(sql)  # 列表中每个元素不是元组 而是对象
    data = [dict(zip(result.keys(), result)) for result in results]
    print(data)
    return resp.resp_200(data=data)
