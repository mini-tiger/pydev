import json
import os
from models import data

current_directory = os.path.dirname(__file__)
# Get the parent directory path



# 将JSON字符串解析为Python字典
file_path = "/mnt/AI_Json/上海外高桥荷丹数据中心QA.json"
out_path = os.path.join(current_directory, "json_data", "datacenter.json")
# 读取JSON文件
with open(file_path, "r", encoding="utf-8") as json_file:
    file_data = json.load(json_file)


# 现在，data变量包含了从JSON文件中读取
# 转换为新格式
new_data = []

for qa in file_data:
    # qa_list = []
    qa_item = data.PromptQA()

    # print(question,len(question))
    # print(answer,len(answer))
    qa_item.put_data(question_std=qa["prompt"], answers_std=qa["chosen"], answers_real="")
    # qa_list.append(qa_item)
    if qa_item.question_std != "":
        qa_item.put_prompt(prompt=qa["prompt"])
        new_data.append(qa_item.__dict__)

# 输出转换后的结果
new_json = json.dumps(new_data, ensure_ascii=False, indent=2)
print(new_json)
print(len(new_data))

# 将JSON字符串写入文件

with open(out_path, "w") as json_file:
    json_file.write(new_json)

print("JSON data has been written to", out_path)
