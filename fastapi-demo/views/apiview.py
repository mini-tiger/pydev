from pydantic import BaseModel
from typing import List, Set
from utils import resp

from fastapi import FastAPI, File, UploadFile
import sys, os


class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    tags: Set[str] = []
    # images: List[Image] = None
    image: Image = None


class Offer(BaseModel):
    name: str
    description: str = None
    price: float
    items: List[Item]


# @api.Router.post("/offer")  # 自定义请求json参数,不符合 自动返回错误
async def offer_view(offer: Offer):  # todo Offer 可以使用dict 代替
    return offer


# @api.Router.get("/")
async def apiIndex():
    return resp.resp_200(data="v1 Root")


# async def uploadfile(file: bytes = File(...)):
#     dir = sys.path[0]
#     with open(os.path.join(dir,"a.txt"), 'wb') as f:
#         f.write(file)
#
#     return {"fileSize": len(file),"filename":file}

async def create_upload_file(file: UploadFile = File(...)):
    file_data = await file.read()
    dir = sys.path[0]
    with open(os.path.join(dir, file.filename), 'wb') as fp:
        fp.write(file_data)
    fp.close()

    return {"filename": file.filename}
