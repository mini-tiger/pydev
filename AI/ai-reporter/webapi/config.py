import os, json


class BaseConfig(object):
    @staticmethod
    def generate_openai_url_list(RUN_TYPE, VECTOR_OPEN):
        if os.environ.get("OPENAI_API_BASE") is not None:
            openai_api_base_str = os.environ.get("OPENAI_API_BASE", "")
            OPENAI_API_BASE_LIST = openai_api_base_str.split(
                ",")  # export  OPENAI_API_BASE=http://api1_url/v1,http://api2_url/v1,http://api3_url/v1
        else:
            if int(VECTOR_OPEN) == 1:
                OPENAI_API_BASE_LIST = ["http://120.133.75.252:28006/v1","http://120.133.63.162:33382/v1"]
                # OPENAI_API_BASE_LIST = ["http://120.133.63.166:8002/v1"]
            else:
                if RUN_TYPE == "dev":
                    OPENAI_API_BASE_LIST = ["http://120.133.63.166:8003/v1",
                                            "http://120.133.63.166:8000/v1",
                                            "http://120.133.63.166:8002/v1"]
                else:
                    OPENAI_API_BASE_LIST = ["http://127.0.0.1:8000/v1",
                                            "http://127.0.0.1:8001/v1",
                                            "http://127.0.0.1:8002/v1",
                                            "http://127.0.0.1:8003/v1",
                                            "http://127.0.0.1:8004/v1",
                                            "http://127.0.0.1:8005/v1"]
        return OPENAI_API_BASE_LIST

    RUN_TYPE = os.environ.get("RUN_TYPE", default="dev")
    current_directory = os.path.dirname(__file__)
    base_dir = os.path.dirname(current_directory)  # os.environ.get("HOMEDIR")

    Log_File = os.environ.get('LOG_TXT', default="log.txt")
    Semaphore_Timeout = os.environ.get('Semaphore_Timeout', default=7200)

    # llm
    # vector
    VECTOR_OPEN = os.environ.get("VECTOR_OPEN", default=1)
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", default="EMPTY")
    OPENAI_API_BASE_LIST = generate_openai_url_list(RUN_TYPE, VECTOR_OPEN)
    MODEL_NAME = os.environ.get("MODEL_NAME", default="Baichuan2-13B-Chat")

    if RUN_TYPE == "dev":

        GENERATE_SLEEP = os.environ.get("GENERATE_SLEEP", default=0.3)

        DOWNLOAD_URL = os.environ.get("DOWNLOAD_URL", default="http://172.22.220.21:5001/attachment/download/")
        VIEW_URL = os.environ.get("VIEW_URL",
                                  default="http://120.133.63.166:8012/onlinePreview?url=@replace@&officePreviewType=pdf")

    else:
        GENERATE_SLEEP = os.environ.get("GENERATE_SLEEP", default=2)
        DOWNLOAD_URL = os.environ.get("DOWNLOAD_URL", default="http://120.133.63.166:5001/attachment/download/")
        VIEW_URL = os.environ.get("VIEW_URL",
                                  default="http://120.133.63.166:8012/onlinePreview?url=@replace@&officePreviewType=pdf")

    WORD_MULTIPLE = 1
    # 并发限制
    CONCURRENT_LIMIT = os.environ.get("CONCURRENT_LIMIT", default=0)

    # VECTOR_INDEX_FILE = os.environ.get("VECTOR_INDEX_FILE",
    #                                    default=os.path.join(current_directory, "db", "faiss_index"))
    # PDF_DIR = os.environ.get("PDF_DIR", default=os.path.join(current_directory, "pdf", "zhongzi"))
    # EMBEDDING_DIR = os.environ.get("EMBEDDING_DIR", default=os.path.join(current_directory, "db", "export_model"))
    # EMBEDDING_DIR = os.environ.get("EMBEDDING_DIR", default=os.path.join(current_directory, "db", "m3e-base"))
    SCORE = os.environ.get("SCORE", default=0.8)

    # rag
    LANGCHAIN_RAG = os.environ.get("LANGCHAIN_RAG", default=0)  # 10section 930s
    GPUOS_PLATFORM = os.environ.get("GPUOS_PLATFORM", default=1)  # 10section 350s
    GPUOS_PLATFORM_URL = os.environ.get("GPUOS_PLATFORM_URL",
                                        default="http://120.133.83.136:11017/api/v1/chat/completions")

env_dist = os.environ  # environ是在os.py中定义的一个dict environ = {}

import logging
# 打印所有环境变量，遍历字典
for key in env_dist:
    logging.info(key + ' : ' + env_dist[key])


