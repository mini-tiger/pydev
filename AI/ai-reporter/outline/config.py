import argparse
import os.path

def parsers():
    RUN_TYPE = os.environ.get("RUN_TYPE", default="dev")
    if RUN_TYPE == "dev":
        ip1 = "120.133.63.166"
        ip2 = "120.133.83.145"
    else:
        ip1 = "127.0.0.1"
        ip2 = "120.133.83.145"
    OUTLINE_MODEL_TYPE = os.environ.get("OUTLINE_MODEL_TYPE", default="model_3")
    bert_classify_model_url = os.environ.get("bertclassifymodelurl", default=f"http://{ip1}:8000/search/reportClassify")
    parser = argparse.ArgumentParser(description="agent of argparse")
    parser.add_argument("--qwen_model_url", type=str, default=f"http://{ip2}:8011/v1/")
    parser.add_argument("--yi_model_url", type=str, default=f"http://{ip1}:8002/v1/")
    parser.add_argument("--bert_classify_model_url", type=str, default=bert_classify_model_url)

    parser.add_argument("--intelligent_generation", type=str, default="智能生成")
 
    parser.add_argument("--execute_count", type=str, default=2)
    parser.add_argument("--create_chapter_count", type=str, default=9)
    parser.add_argument("--create_outline_model", type=str, default=f"{OUTLINE_MODEL_TYPE}")
    args = parser.parse_args()
    return args