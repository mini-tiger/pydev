import os


class BaseConfig():

    RUN_TYPE = os.environ.get("RUN_TYPE", default="dev")
    PROFILE_VERSION= os.environ.get("PROFILE_VERSION",default=None)
    Big_MODEL_EFFECT = os.environ.get("Big_MODEL_EFFECT", default=True)
    MAX_DIFF_LINE = 10
    MIN_LINE_LEN = 5  # 几个字以下跳过
    current_directory = os.path.dirname(__file__)
    Log_File = os.environ.get('LOG_TXT',default="mail_his.txt")
    # mail
    MAIL_CRED_USER = os.environ.get("MAIL_CRED_USER", default=r'21VIANET\tao.jun')
    MAIL_CRED_PWD = os.environ.get("MAIL_CRED_PWD", default=r'Taojun207')
    MAIL_SERVER = os.environ.get("MAIL_SERVER", default='mail.21vianet.com')
    MAIL_ACCOUNT = os.environ.get("MAIL_ACCOUNT", default='tao.jun@neolink.com')

    # run dir
    SOURCE_DOCS_PATH = os.environ.get("SOURCE_DOCS_PATH", default=os.path.join(current_directory, "source_docx"))
    SOURCE_TXT_PATH = os.environ.get("SOURCE_TXT_PATH", default=os.path.join(current_directory, "source_txt"))
    DOWNLOAD_PATH = os.environ.get("DOWNLOAD_PATH", default=os.path.join(current_directory, "download_files"))
    CONVERT_PATH = os.environ.get("CONVERT_PATH", default=os.path.join(current_directory, "convert_files"))
    DIFF_DOCS_PATH = os.environ.get("DIFF_DOCX_PATH", default=os.path.join(current_directory, "diff_docx"))
    TEMPLATE_DIR = os.environ.get("TEMPLATE_DIR", default=os.path.join(current_directory, "template"))

    # llm
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", default="EMPTY")
    OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", default="http://120.133.75.252:28006/v1")
    # OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", default="http://120.133.83.145:8000/v1")
    OPENAI_API_TYPE = os.environ.get("OPENAI_API_TYPE", default="baichuan2") # yi-34b

    # OPENAI_PROXY = os.environ.get("OPENAI_PROXY", default="")
    PROXY = os.environ.get("PROXY", "http://172.22.190.30:80")
    # minio
    MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", default="172.22.50.25:31088")
    MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY", default="fbKdRuYYPsu5nXew")
    MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY", default="v1uKl3ZPe8sSBpZZRQZqIncvbQrlS2sh")

    # postgresql
    PG_VCT_HOST = os.environ.get("PG_VCT_HOST", default="172.22.50.25")
    PG_VCT_PORT = os.environ.get("PG_VCT_PORT", default="31867")
    PG_VCT_DB = os.environ.get("PG_VCT_DB", default="postgres")
    PG_VCT_USER = os.environ.get("PG_VCT_USER", default="test")
    PG_VCT_PWD = os.environ.get("PG_VCT_PWD", default="test123")
