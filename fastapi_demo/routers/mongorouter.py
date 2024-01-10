from fastapi import APIRouter
from views import mongoview

Router = APIRouter(
    # prefix="/mysql",
    # tags=["mysql"],
    responses={404: {"description": "Not Found"}}
)

Router.add_api_route(methods=['POST'], path="/filter", endpoint=mongoview.mongofilter)
# Router.add_api_route(methods=['GET'], path="/", endpoint=apiview.apiIndex)

