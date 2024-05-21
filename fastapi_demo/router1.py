from fastapi import FastAPI, APIRouter

# 创建主应用
app = FastAPI()

# 创建嵌套路由器
router_v1 = APIRouter(prefix="/v1", tags=["Version 1"])

# 在嵌套路由器中定义端点
@router_v1.get("/endpoint1")
async def read_endpoint1():
    return {"version": "1", "message": "Hello from Endpoint 1"}

# 创建另一个嵌套路由器，并在第一个路由器中包含它
router_v2 = APIRouter(prefix="/v2", tags=["Version 2"])

@router_v2.get("/endpoint3")
async def read_endpoint3():
    return {"version": "2", "message": "Hello from Endpoint 3"}

# 将 router_v2 包含到 router_v1 中
router_v1.include_router(router_v2)

# 在主应用中将嵌套路由器添加到路径
app.include_router(router_v1)
