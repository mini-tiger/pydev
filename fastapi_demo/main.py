import time

from fastapi import FastAPI
from routers import api
import uvicorn
from utils import resp
import asyncio
# todo web路由表 http://192.168.43.28:8000/docs

app = FastAPI()  # 创建 api 对象

# 加载路由表
app.include_router(api.Router, prefix="/v1", tags=["v1"])  # url suffix ,tags web在路由表的显示, todo 上传文件
# from routers import mysqlrouter,mongorouter
# app.include_router(mysqlrouter.Router, prefix="/mysql", tags=["mysql"])  # url suffix ,tags web在路由表的显示
# app.include_router(mongorouter.Router, prefix="/mongo", tags=["mongo"])  # url suffix ,tags web在路由表的显示


@app.get("/")  # 根路由
def root():
    # return {"Hello World"}
    return resp.resp_200(data="Hello World")  # json response


@app.get("/say/{data}")  # get 参数
def say(data: str, q: int):
    return {"data": data, "item": q}

@app.get("/a")
async def a():
    time.sleep(1)
    return {"message": "异步模式，但是同步执行sleep函数，执行过程是串行的"}


@app.get("/b")
async def b():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, time.sleep, 1)
    return {"message": "线程池中运行sleep函数"}


@app.get("/c")
async def c():
    await asyncio.sleep(1)
    return {"message": "异步模式，且异步执行sleep函数"}


@app.get("/d")
def d():
    time.sleep(1)
    return {"message": "同步模式，但是FastAPI会放在线程池中运行，所以很快"}

if __name__ == "__main__":
    uvicorn.run(app='main:app', host="0.0.0.0", port=8000, reload=True)
