import time,os,shutil
from datetime import datetime
def contains_any(string, substrings):
    return any(substring in string for substring in substrings)
import os

def get_file_size(file_path):
    """
    Get the size of the specified file.

    :param file_path: Path to the file
    :return: Size of the file in bytes
    """
    if os.path.isfile(file_path):
        return os.path.getsize(file_path)
    else:
        return 0
def list_of_dicts_to_string(data):
    result = []
    for item in data:
        parts = [f"{key}: {value}" for key, value in item.items()]
        result.append("{ " + ", ".join(parts) + " }")
    return "[ " + ", ".join(result) + " ]"


def generate_class_info(cls):
    info = []
    for column in cls.__table__.columns:
        column_name = column.name
        if column_name == "id" or column_name == "insert_time":
            continue
        if not column.comment:
            continue
        comment = column.comment if column.comment else "无注释"
        info.append(f"{column_name}: {comment}")
    return ", ".join(info)


def generate_timestamped_filename(filename):
    # 获取当前时间戳
    timestamp = int(time.time())

    # 获取文件名前5位
    prefix = filename[:8]

    # 组合时间戳和文件名前5位
    result = f"{prefix}_{timestamp}"

    return result


def recreate_directory(directory_path):
    # 如果目录存在，则删除
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)

    # 创建新的目录
    os.makedirs(directory_path)


import xml.etree.ElementTree as ET


def add_dict_to_xml(file_path, data_dict):
    # 读取现有的XML文件
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 查找现有的report标签


    # 如果存在report标签，添加键值对
    if root is not None:
        for key, value in data_dict.items():
            # 创建一个子元素，并设置其文本为相应的值
            entry = ET.Element(key)
            entry.text = str(value)
            root.append(entry)

    # 将修改后的XML写回文件
    tree.write(file_path, encoding="utf-8", xml_declaration=True)

import xmltodict
def read_xml_to_dict(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()
        data_dict = xmltodict.parse(xml_content)
    return data_dict

def get_current_time():
    # 获取当前时间
    current_time = datetime.now()

    # 格式化时间为 yyyy-mm-dd HH:MM:ss 格式
    return  current_time.strftime('%Y-%m-%d %H:%M:%S')


def move_file_to_directory(filename, output_directory):
    """
    将文件移动到指定的输出目录。

    参数:
    filename (str): 需要移动的文件的绝对路径。
    output_directory (str): 目标输出目录的路径。

    返回:
    bool: 移动是否成功。
    """
    # 获取文件名
    file_basename = os.path.basename(filename)

    # 构建目标路径
    destination = os.path.join(output_directory, file_basename)

    try:
        # 移动文件
        print(shutil.move(filename, destination))

        return True
    except Exception as e:

        return False