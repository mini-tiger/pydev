import os, json


def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        print(f"delete {file_path}")
        os.remove(file_path)
        # print(f"文件 {file_path} 已删除")
    # else:
    #     print(f"文件 {file_path} 不存在，跳过删除操作")


def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def yield_return(msg):
    yield format_sse_json(json.dumps(msg,ensure_ascii=False))

def format_sse_json(msg,status="data"):
    return 'data: {}\n\n'.format(json.dumps({"type":status,"msg": msg}, ensure_ascii=False))
