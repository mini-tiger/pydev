import logging
import os
import re

from flask import Blueprint, abort, request, send_file
from werkzeug.utils import secure_filename
import webapi.config  as   config
# 附件存放目录
ATTACHMENT_DIR = os.path.join(config.BaseConfig.current_directory,"app",'attachments')

attachmentBP = Blueprint('attachmentBP', __name__, url_prefix='/attachment')


@attachmentBP.route('download/<attachment_name>', methods=['GET'])
def download(attachment_name):
    try:
        exists_file = False

        # 构建附件的完整路径
        attachment_path = os.path.join(ATTACHMENT_DIR, attachment_name)
        # 检查文件是否存在
        if os.path.isfile(attachment_path):
            exists_file = True
        logging.info(f"attachment_name: {attachment_name}")
        logging.info(f"attachment_path: {attachment_path}")
        if not exists_file:
            # 使用正则表达式查找日期部分
            match = re.search(r'-\d{8}T', attachment_name)

            date = match.group(0)

            date = date[1:-1]  # 去掉 "-" 和 "T"
            # 构建附件的完整路径
            attachment_path = os.path.join(ATTACHMENT_DIR, date, attachment_name)
            logging.info(f"match {attachment_name} ,re result:{date},attachment_path:{attachment_path}")
            # 检查文件是否存在
            if os.path.isfile(attachment_path):
                exists_file = True

        if not exists_file:
            raise FileNotFoundError(f'Attachment {attachment_name} not found')

        # 找到最后一个 "-" 的索引
        last_dash_index = attachment_name.rfind("-")
        # 截取字符串，去掉最后一个 "-" 到 ".docx" 之间的内容
        download_name = attachment_name[:last_dash_index] + attachment_name[attachment_name.rfind('.'):]

        # 发送附件文件
        return send_file(attachment_path, as_attachment=True, download_name=download_name)
    except FileNotFoundError as e:
        return str(e), 404  # 返回文件不存在的错误信息和 HTTP 404 状态码
    except Exception as e:
        return str(e), 500  # 返回其他异常信息和 HTTP 500 状态码

