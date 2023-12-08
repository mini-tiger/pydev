import json
from models import data
import os

current_directory = os.path.dirname(__file__)
# 将JSON字符串解析为Python字典
file_path = os.path.join(current_directory, "src_json_data", "translation2019zh_valid.json")
out_path = os.path.join(current_directory, "json_data", "translation.json")
# 读取JSON文件
json_data = []
with open(file_path, "r", encoding="utf-8") as json_file:
    for line in json_file:
        # Assuming each line contains a JSON-serializable string
        data1 = json.loads(line.strip())
        json_data.append(data1)

# print(data)


# 现在，data变量包含了从JSON文件中读取
# 转换为新格式
new_data = []

for qa in json_data:
    # qa_list = []
    qa_item = data.PromptQA()

    # print(question,len(question))
    # print(answer,len(answer))
    qa_item.put_data(question_std=qa["english"], answers_std=qa["chinese"], answers_real="")
    # qa_list.append(qa_item)
    if qa_item.question_std != "":
        qa_item.put_prompt(prompt=qa["english"])
        new_data.append(qa_item.__dict__)

# 输出转换后的结果
new_json = json.dumps(new_data, ensure_ascii=False, indent=2)
print(new_json)
print(len(new_data))

# 将JSON字符串写入文件

with open(out_path, "w") as json_file:
    json_file.write(new_json)

print("JSON data has been written to", out_path)
