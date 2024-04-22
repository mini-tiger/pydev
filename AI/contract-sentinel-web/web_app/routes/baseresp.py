from fastapi import status
from fastapi.responses import JSONResponse, Response  # , ORJSONResponse
from typing import Union
from pydantic import BaseModel
import json
from tools.utils import format_sse_json, delete_file_if_exists, create_directory_if_not_exists, yield_return

def resp_err_stream(msg):
    yield format_sse_json(status="error", msg=msg)

class ResponseModel(BaseModel):
    code: int
    message: str
    data: Union[list, dict, str]

def resp_200(*, data: Union[list, dict, str]) -> ResponseModel:
    return ResponseModel(code=200, message="success", data=data)


def resp_400(*, data: str = None, message: str = "BAD REQUEST") -> ResponseModel:
    return ResponseModel(code=400, message="fail", data=data)
