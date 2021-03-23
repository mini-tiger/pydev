from fastapi import FastAPI
from routers import api, mysqlrouter,mongorouter
import uvicorn
from utils import resp

# todo web路由表 http://192.168.43.28:8000/docs

app = FastAPI()  # 创建 api 对象

# 加载路由表
app.include_router(api.Router, prefix="/v1", tags=["v1"])  # url suffix ,tags web在路由表的显示, todo 上传文件
app.include_router(mysqlrouter.Router, prefix="/mysql", tags=["mysql"])  # url suffix ,tags web在路由表的显示
app.include_router(mongorouter.Router, prefix="/mongo", tags=["mongo"])  # url suffix ,tags web在路由表的显示


@app.get("/")  # 根路由
def root():
    # return {"Hello World"}
    return resp.resp_200(data="Hello World")  # json response


@app.get("/say/{data}")  # get 参数
def say(data: str, q: int):
    return {"data": data, "item": q}


if __name__ == "__main__":
    uvicorn.run(app='main:app', host="0.0.0.0", port=8000, reload=True, debug=True)
