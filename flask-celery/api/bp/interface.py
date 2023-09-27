import time

from flask import Flask, jsonify, request, make_response, send_file
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from api import config
from api.service import score
from api.db import conn

testbp = Blueprint('testbp', __name__, url_prefix='/testapi')


@testbp.route('/')
def index():
    return 'User blueprint, index page'


@testbp.route('/uploadFile', methods=["POST"])  # 上传文件 以及参数   postman  form-data 方式  file:文件  , 其他参数
def uploadFile():
    f_obj = request.files['file']

    print("上传文件名:", f_obj.filename)
    if f_obj is None:
        return jsonify({"status": config.GeneralCfg.fail})
    file_path = os.path.join(config.GeneralCfg.upload_qa_file_dir, f_obj.filename)
    f_obj.save(file_path)

    try:
        result = score.get_score_excel.delay(file_path)
        conn.insert_job_score_db(f_obj.filename, result.id, 1, time.time(), 0)
        # conn.update_job_score_db(result.id, 1, 0)
        return jsonify({"status": config.GeneralCfg.success, "resultId": result.id})
    except Exception as e:
        print(e)
        return jsonify({"status": config.GeneralCfg.fail, "resultId": 0})
    # print("上传参数:", request.form.to_dict())
    # return jsonify({"status": config.GeneralCfg.success, "resultId": result.id})


@testbp.route('/joblist', methods=["POST"])  # 上传文件 以及参数   postman  form-data 方式  file:文件  , 其他参数
def joblist():
    joblist = conn.query_db('''
    select id,filename,downloadurl,job_id,
    (select job_type from job_type where job_score.job_type_num=job_type.job_num) as job_type,
    datetime(created_at,"unixepoch","localtime") as create_at,datetime(finish_at,"unixepoch","localtime") as finish_at from job_score order by created_at desc
    ''')
    return jsonify({"data": joblist})


from celery.result import AsyncResult


@testbp.route("/result/<id>")
def task_result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }


@testbp.route("/download")
def download_file():
    """
    下载src_file目录下面的文件
    eg：下载当前目录下面的123.tar 文件，eg:http://localhost:5000/download?fileId=123.tar
    :return:
    """
    file_name = request.args.get('file')
    file_name = "%s.xlsx" % os.path.splitext(file_name)[0]
    # print(file_name)
    # file_path = "/data/work/pydev/neolink-dataset/test/api/file_store/uploadfile/石桥数据中心QA对.xlsx"
    file_path = os.path.join(config.GeneralCfg.excel_file_dir, file_name)
    print(file_path)
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "The downloaded file does not exist"
