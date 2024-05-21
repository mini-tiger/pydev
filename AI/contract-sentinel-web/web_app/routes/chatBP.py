import json
from enum import Enum
from pydantic import BaseModel, validator,field_validator
from fastapi import BackgroundTasks
from web_app.routes import global_lock
import os
from starlette.responses import StreamingResponse
from typing import List
from fastapi.responses import FileResponse
import pythoncom
from web_app.routes.baseresp import *
from run_demo_win32 import DocxProcess, SingleMailData
from service.llm import baichuan_llm
from run_init_db import match_data_list

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi import APIRouter
from tools.utils import format_sse_json, delete_file_if_exists, create_directory_if_not_exists, yield_return
import config
from service.g import logger

class process_word():
    def __init__(self, file, tpl):
        self.file = file
        self.tpl = tpl
        self.result = {}

    def process_single_docx(self):
        yield format_sse_json(status="data", msg='已保存文件至工作空间')
        # 线程初始化
        pythoncom.CoInitialize()
        file = self.file
        # 程序代码
        logger.info(f"current file: {file}")

        single_mail_data = SingleMailData()
        single_mail_data.email_doc_file = file
        config1 = config.BaseConfig

        dp = DocxProcess(convert_path=config1.CONVERT_PATH,
                         template_path=config1.TEMPLATE_DIR,
                         source_txt_path=config1.SOURCE_TXT_PATH,
                         source_docs_path=config1.SOURCE_DOCS_PATH,
                         diff_docs_path=config1.DIFF_DOCS_PATH,
                         single_mail_data=single_mail_data,
                         match_data_list=match_data_list,
                         baichuan_llm=baichuan_llm(
                             url=config1.OPENAI_API_BASE),
                         )
        yield from dp.single_attachment_handle_process()

        pythoncom.CoUninitialize()
        result = dp.get_result()

        yield format_sse_json(status="result", msg=json.dumps(result, ensure_ascii=False))
        delete_file_if_exists(self.file)


ALLOWED_EXTENSIONS = {'docx'}


class Tpl_Map_Item(BaseModel):
    name: str

def tpl_map():
    return [
        {"name": "硬件采购合同_source.docx"},
        {"name": "软件开发服务合同_source.docx"},
        {"name": "非锁定版(非标准合同)_IDC主协议_北京世纪互联宽带数据中心托管服务协议(2023年版)-（非预留机柜）.docx"},
    ]


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


async def upload_file(file: UploadFile = File(...)):
    if not allowed_file(file.filename):
        # raise HTTPException(status_code=400, detail="File extension not allowed")
        return resp_400(data="File extension not allowed")
    try:
        contents = await file.read()
        file_path = os.path.join(config.BaseConfig.DOWNLOAD_PATH, file.filename)
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        return resp_400(data=str(e))

    return resp_200(data=file.filename)
    # return StreamingResponse(event_stream(file_path), media_type="text/event-stream")


class SourceEnum(str, Enum):
    option1 = "diff"
    option2 = "tpl"


class download_request_struct(BaseModel):
    file: str
    source: SourceEnum = SourceEnum.option1
    @field_validator('file')
    def file_must_be_docx(cls, v):
        if not v.endswith('.docx'):
            raise ValueError('file 名称必须以 "docx" 结尾')
        return v


async def download_file(request_json: download_request_struct):
    file = request_json.file
    logger.info(f"download file params{request_json}")
    base_dir = config.BaseConfig.DIFF_DOCS_PATH if request_json.source == "diff" else config.BaseConfig.SOURCE_DOCS_PATH
    file_path = os.path.join(base_dir, file)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=file)


def release_lock(message):
    global_lock.release()


class Offer(BaseModel):
    tpl_name: str = r"非锁定版(非标准合同)_IDC主协议_北京世纪互联宽带数据中心托管服务协议(2023年版)-（非预留机柜）.docx"
    file: str
    @field_validator('file')
    def file_must_be_docx(cls, v):
        if not v.endswith('.docx'):
            raise ValueError('file 名称必须以 "docx" 结尾')
        return v

def process_single_docx(request_json: Offer, response: Response):
    logger.info(f"process params:{request_json}")
    file = request_json.file
    file_path = os.path.join(config.BaseConfig.DOWNLOAD_PATH, file)
    tpl = request_json.tpl_name
    tpl_path = os.path.join(config.BaseConfig.SOURCE_DOCS_PATH, tpl)
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"
    response.headers['media_type'] = "text/event-stream"
    response.headers['chunk_size'] = "65536"
    if os.path.exists(file_path) is False:
        return StreamingResponse(resp_err_stream(json.dumps({"error": "file not found"}, ensure_ascii=False)))

    if  global_lock.acquire(blocking=False):

        # tasks = BackgroundTasks()
        # tasks.add_task(release_lock, message="Success")  # callback 释放lock

        try:
            pw = process_word(file=file_path, tpl=tpl_path)
            return StreamingResponse(pw.process_single_docx(), media_type="text/event-stream")
        except Exception as e:
            return StreamingResponse(resp_err_stream(json.dumps({"error": str(e)}, ensure_ascii=False)))
        finally:
            global_lock.release()

    else:
        return StreamingResponse(resp_err_stream(json.dumps({"error": "最大并发1,超过上限"}, ensure_ascii=False)))


def chat_info():
    try:
        config_json=os.path.join(config.BaseConfig.current_directory,"config.json")
        pv = config.BaseConfig.PROFILE_VERSION
        # 打开JSON文件并加载数据
        with open(config_json, 'r') as file:
            data = json.load(file)

        if pv is not None:
            rebuild = []
            for v in data:
                v['project']['isEnabled']=True if v['project']['id']==int(pv) else False
                rebuild.append(v)

        return resp_200(data=data)
    except Exception as e:
        return resp_400(data=str(e))

Router = APIRouter(
    # prefix="/v1",
    # tags=["v1"],
    responses={404: {"description": "Not Found"}}
)

Router.add_api_route(methods=['POST'], path="/process", endpoint=process_single_docx, response_class=StreamingResponse,
                     responses={
                         200: {
                             "description": "SSE endpoint. Returns a stream of events.",
                             "content": {
                                 "text/event-stream": {
                                     "example": {"type": "data", "msg": "对比模板差异"}
                                 }
                             }
                         }
                     })
Router.add_api_route(methods=['GET','POST'], path="/download", endpoint=download_file, response_class=FileResponse,  # 指定响应类
                     responses={
                         200: {
                             "description": "Return the file as binary data.",
                             "content": {
                                 "application/octet-stream": {
                                     "example": "Binary data of the file"
                                 }
                             }
                         },
                         404: {
                             "description": "File not found."
                         }
                     })
Router.add_api_route(methods=['POST'], path="/uploadfile", endpoint=upload_file, response_model=ResponseModel)
Router.add_api_route(methods=['POST','GET'], path="/chat-info", endpoint=chat_info, response_model=ResponseModel)

Router.add_api_route(methods=['GET'], path="/tpl_map", endpoint=tpl_map, response_model=List[Tpl_Map_Item])

# if __name__ == "__main__":
# pythoncom.CoInitialize()
# file = r"D:\codes\neolink-dataset\contract-sentinel-web\download_files\硬件采购合同.docx"
# # 程序代码
# logger.info(f"current file: {file}")
#
# single_mail_data = SingleMailData()
# single_mail_data.email_doc_file = file
# config1 = config.BaseConfig
#
# dp = DocxProcess(convert_path=config1.CONVERT_PATH,
#                  template_path=config1.TEMPLATE_DIR,
#                  source_txt_path=config1.SOURCE_TXT_PATH,
#                  source_docs_path=config1.SOURCE_DOCS_PATH,
#                  diff_docs_path=config1.DIFF_DOCS_PATH,
#                  single_mail_data=single_mail_data,
#                  match_data_list=match_data_list,
#                  baichuan_llm=baichuan_llm(
#                      url=config1.OPENAI_API_BASE),
#                  )
#
# dp.single_attachment_handle_process()
#
# pythoncom.CoUninitialize()
# result = dp.get_result()
