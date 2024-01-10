from fastapi import APIRouter
from fastapi_demo.views import mysqlview

Router = APIRouter(
    # prefix="/mysql",
    # tags=["mysql"],
    responses={404: {"description": "Not Found"}}
)

Router.add_api_route(methods=['POST'], path="/filter", endpoint=mysqlview.mysqlfilter)
# Router.add_api_route(methods=['GET'], path="/", endpoint=apiview.apiIndex)

