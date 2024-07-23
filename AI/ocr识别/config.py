import os, json
from openai import OpenAI
import urllib.parse
class BaseConfig(object):
    RECREATE_TABLE = os.environ.get("RECREATE_TABLE", True)
    NEO4J_USE = os.environ.get("NEO4J_USE",False)

    # RUN_TYPE = os.environ.get("RUN_TYPE", default="dev")
    current_directory = os.path.dirname(__file__)
    download_success_record_file = os.path.join(current_directory,"download_success_record_file.txt")
    download_fail_record_file = os.path.join(current_directory,"download_fail_record_file.txt")
    output_dir_base =os.path.join(current_directory, 'output')  # 指定输出目录
    # base_dir = os.path.dirname(current_directory)  # os.environ.get("HOMEDIR")
    use_gpu = os.environ.get("USE_GPU", 0)
    pdf_files_dir = os.environ.get("PDFS_DIR", os.path.join(current_directory, "pdf_files"))
    err_pdf_files_dir = os.environ.get("ERR_PDFS_DIR", os.path.join(current_directory, "err_pdf_files"))
    success_pdf_files_dir = os.environ.get("SUCCESS_PDFS_DIR", os.path.join(current_directory, "success_pdf_files"))

    ocr_kw = {}
    passwd = "passwordtest"
    password_encoded = urllib.parse.quote_plus(passwd)
    db_uri = f"mysql+pymysql://root:{password_encoded}@120.133.63.166:9171/testdb?charset=utf8"

    neo4j_uri = "bolt://120.133.63.166:7687"
    neo4j_username = "neo4j"
    neo4j_password = "0123456789"
    zz = os.environ.get("ZZ",0)
    openai_base = "http://120.133.63.166:8023/v1"
    cls_model_dir = os.path.join(current_directory,"whl/cls/ch_ppocr_server_v2.0_rec_infer")
    rec_model_dir = os.path.join(current_directory, "whl/rec/ch_PP-OCRv4_rec_server_infer")
    det_model_dir = os.path.join(current_directory, "whl/det/ch/ch_PP-OCRv4_det_server_infer")

    # on A800
    if int(use_gpu) == 1:
        openai_base = "http://127.0.0.1:9099/v1"
        cls_model_dir = os.path.join(current_directory, "whl/cls/ch_ppocr_server_v2.0_rec_infer")
        rec_model_dir = os.path.join(current_directory, "whl/rec/ch_PP-OCRv4_rec_server_infer")
        det_model_dir = os.path.join(current_directory, "whl/det/ch/ch_PP-OCRv4_det_server_infer")
        neo4j_uri = "bolt://127.0.0.1:7687"
        db_uri = f"mysql+pymysql://root:{password_encoded}@172.17.0.7:3306/testdb?charset=utf8"

    if int(zz) == 1:
        openai_base = "http://172.21.10.143:33390/v1"
        # openai_base = "http://120.133.63.166:9099/v1"
        passwd = "vchat@QAZ"
        password_encoded = urllib.parse.quote_plus(passwd)
        # db_uri = f"mysql+pymysql://root:{password_encoded}@120.133.63.166:9171/testdb?charset=utf8"
        db_uri = f"mysql+pymysql://root:{password_encoded}@172.21.10.119:13306/testdb?charset=utf8"


    # upload_dir = os.path.join(current_directory,"upload_dir")
    # minio_base_url = "http://10.20.201.215:9000"
    # kimi_base_url = "https://api.moonshot.cn/v1"
    # kimi_api_key = "sk-RggH0r7aumh2RWlUHdMfAGPG9xsMFyN7O4cz0fDyhqYuzhr6"
    # kimi_client = OpenAI(
    #     api_key=kimi_api_key,
    #     base_url=kimi_base_url
    # )


