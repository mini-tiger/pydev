import os

from fastapi import FastAPI, File, Response,Request
import web_app.routes.baseresp as resp
import web_app.routes.chatBP as chatBP
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

def create_app():
    app = FastAPI(swagger_ui_parameters={"syntaxHighlight": True},
                  title="Legal assistant api docs",
                  description='法务助手web版本',
                  summary="https://gitlabcode.21vianet.com/vnet/aienterprise/neolink-dataset",
                  version="0.0.1",
                  terms_of_service="http://example.com/terms/",
                  contact={
                      "name": "neolink",
                      "url": "https://gitlabcode.21vianet.com/vnet/aienterprise/neolink-dataset",
                      "email": "tao.jun@neolink.com",
                  },
                  license_info={
                      "name": "Apache 2.0",
                      "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
                  },
                  )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def catch_exceptions_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except StarletteHTTPException as exc:
            if exc.status_code == 422:
                body = await request.json()
                print(f"Invalid request body: {body}")
                # 或者进行其他形式的日志记录
            raise exc

    return app


# 打印所有路由
def print_all_routes(app):
    for route in app.routes:
        methods = ",".join(route.methods) if hasattr(route, "methods") else "None"
        print(f"Path: {route.path}, Methods: {methods}, Name: {route.name}")

import logging
def start_web():
    app = create_app()

    # 加载路由表
    app.include_router(chatBP.Router, prefix="/legal/v1", tags=["v1"])  # url suffix ,tags web在路由表的显示, todo 上传文件

    @app.get("/health")  # 根路由
    def root():
        # return {"Hello World"}
        return resp.resp_200(data="Hello World")  # json response

    # 在适当的时候调用这个函数
    print_all_routes(app)
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"

    uvicorn.run(app, host="0.0.0.0", log_config=log_config,port=os.environ.get("API_PORT", 5001))

# if __name__ == '__main__':
#     app = create_app()
#     app.run(host="0.0.0.0", port=os.environ.get('FLASK_PORT', 5001), debug=True)
