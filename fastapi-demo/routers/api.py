from fastapi import APIRouter

from views import apiview  # 相对路径,todo 如果报错，pycharm  标记目录为源根

Router = APIRouter(
    # prefix="/v1",
    # tags=["v1"],
    responses={404: {"description": "Not Found"}}
)

Router.add_api_route(methods=['POST'], path="/offer", endpoint=apiview.offer_view)
Router.add_api_route(methods=['GET'], path="/", endpoint=apiview.apiIndex)

Router.add_api_route(methods=['POST'], path="/uploadfile", endpoint=apiview.create_upload_file)
