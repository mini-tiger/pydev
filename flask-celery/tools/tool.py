import pandas as pd
from datetime import datetime
import json, csv, re
import numpy as np
from text2vec import Similarity, SimilarityType
import decimal, sys
from openpyxl import Workbook
import subprocess

# Check current encoding
current_encoding = sys.getdefaultencoding()
from openpyxl.styles import Side, Border, colors


# 定义边框样式
def my_border(t_border, b_border, l_border, r_border):
    border = Border(top=Side(border_style=t_border, color=colors.BLACK),
                    bottom=Side(border_style=b_border, color=colors.BLACK),
                    left=Side(border_style=l_border, color=colors.BLACK),
                    right=Side(border_style=r_border, color=colors.BLACK))
    return border


# 初始化制定区域边框为所有框线
def format_border(sheet, s_column, s_index, e_column, e_index):
    for row in tuple(sheet[s_column + str(s_index):e_column + str(e_index)]):
        for cell in row:
            cell.border = my_border('thin', 'thin', 'thin', 'thin')


def exec_shell(cmd):
    # 要执行的Shell命令
    command = cmd  # 例如，这里是执行 "ls" 命令

    # 使用subprocess运行Shell命令
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 获取命令的标准输出和标准错误输出
    output = result.stdout
    error = result.stderr

    # 打印输出和错误信息
    # print("标准输出：", output)
    # print("标准错误：", error)
    return output


def write_xlsx(file, data_list, fieldnames):
    # Specify XLSX file path
    xlsx_file_path = file

    workbook = Workbook()

    # Get the active worksheet
    sheet = workbook.active

    # Write column names

    sheet.append(fieldnames)

    format_res = []
    for i in data_list:
        row = []
        for field in fieldnames:
            # print(field,getattr(i,field))
            row.append(getattr(i, field))
        format_res.append(row)

    # Write data from PromptQA objects to the worksheet
    for row in format_res:
        sheet.append(row)

    # Save the workbook to XLSX file
    workbook.save(xlsx_file_path)

    print("Data written to", xlsx_file_path)


def write_csv(file, data_list, fieldnames, encodeing="gbk"):
    # 写入CSV文件
    csv_file_path = file
    with open(csv_file_path, mode="w", newline="", encoding=encodeing) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for instance in data_list:
            writer.writerow(instance.__dict__)

    print(f"CSV文件已创建：{csv_file_path}")


def DateStr():
    # 获取当前日期和时间
    now = datetime.now()

    # 提取年、月、日、小时和分钟
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

    # 格式化为字符串
    date_string = f"{year}{month:02d}{day:02d}"
    time_string = f"{hour:02d}{minute:02d}"

    # 合并日期和时间字符串
    full_string = f"{date_string}{time_string}"

    # print("完整字符串:", full_string)
    return full_string


def reDockerfile(dockerfile_path: str):
    # 打开 Dockerfile 文件并读取内容
    embedding_model_path = ""
    f = open(dockerfile_path, "r")
    lines = f.readlines()
    for line in lines:
        # 使用正则表达式来提取 ENV 指令中的 EMBEDDING_MODEL_PATH 值
        if line.find("EMBEDDING_MODEL_PATH") !=-1:
            line=line.split("ENV ")[1]
            line=line.split("=")[1]
            # print(f"EMBEDDING_MODEL_PATH value: {embedding_model_path}")
            return  line
        if line.find("embedding_model_path") !=-1:
            line=line.split("ENV ")[1]
            line=line.split("=")[1]
            # print(f"EMBEDDING_MODEL_PATH value: {embedding_model_path}")
            return  line
    return embedding_model_path


class QA:
    def __init__(self, q, a):
        self.prompt = q
        self.chosen = a

    def to_json(self):
        return {"instruction": self.prompt, "output": self.chosen}
