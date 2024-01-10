from typing import List, Set
from fastapi_demo.utils import resp  # 默认路径 fastapi-demo
from fastapi import params, requests
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from modules import mongoconn
import asyncio


class mongofilterReq(BaseModel):
    filter: dict


async def mongofilter(req: mongofilterReq):
    print(req)
    print(jsonable_encoder(req))
    print(req.filter)

    onedata = mongoconn.fectchOne("dms-content","605952526b32a90594a0ce84")
    # print(onedata)
    data = mongoconn.fetchAll("dms-content", req.filter)
    # print(data)
    return resp.resp_200(data=jsonable_encoder(data))
