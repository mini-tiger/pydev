from openpyxl import load_workbook
from types import SimpleNamespace
import json
# Specify the XLSX file path and the sheet name
from AI.models import data
import sys
import os

current_directory = os.path.dirname(__file__)

xlsx_file_path = "/mnt/AI_Json/Colo_20230830.xlsx"
sheet_name = "detail"  # Change to the actual sheet name
out_path = os.path.join(current_directory, "json_data", "Colo_20230830.xlsx.json")
# Load the workbook and select the specified sheet
workbook = load_workbook(filename=xlsx_file_path)
sheet = workbook[sheet_name]

# Extract data from A and D columns
column_a_data = [cell.value for cell in sheet["A"]]
column_d_data = [cell.value for cell in sheet["D"]]

# Print the extracted data
# print("Data from A column:", column_a_data[1:])
# print("Data from D column:", column_d_data[1:])
tmp_result = zip(column_a_data[1:], column_d_data[1:])
result = []
for i in tmp_result:
    if i[1].find("无") != -1 and len(i[1]) < 4:
        continue
    s = SimpleNamespace()
    s.question = i[0]
    s.answer = i[1]
    result.append(s)

# 转换为新格式
new_data = []
for item in result:
    qa_item = data.PromptQA()
    qa_item.put_data(question_std=item.question, answers_std=item.answer, answers_real="")

    # qa_list.append(qa_item)

    new_data.append(qa_item.__dict__)

# 输出转换后的结果
new_json = json.dumps(new_data, ensure_ascii=False, indent=2)
print(new_json)
print(len(new_data))

# 将JSON字符串写入文件

with open(out_path, "w") as json_file:
    json_file.write(new_json)

print("JSON data has been written to", out_path)
