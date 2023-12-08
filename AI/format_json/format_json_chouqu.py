import json

import sys
import os

current_directory=os.path.dirname(__file__)
# Get the parent directory path
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(parent_directory)
# Add the parent directory to sys.path
sys.path.append(parent_directory)

from models import data

# 将JSON字符串解析为Python字典
file_path = os.path.join(current_directory,"src_json_data","cmrc2018_trial.json")
out_path = os.path.join(current_directory,"json_data","chouqu.json")
# 读取JSON文件
with open(file_path, "r", encoding="utf-8") as json_file:
    file_data = json.load(json_file)

# print(data)


# 现在，data变量包含了从JSON文件中读取
# 转换为新格式
new_data = []
for item in file_data["data"]:
    for paragraph in item["paragraphs"]:
        context = paragraph["context"]
        # qa_list = []
        qa_item = data.PromptQA()
        for qa in paragraph["qas"]:
            question = qa["question"]
            answer = qa["answers"][0]["text"]
            # print(question,len(question))
            # print(answer,len(answer))
            if len(answer) <= 10:
                qa_item.put_data(question_std=question, answers_std=answer, answers_real="")
                break
            # qa_list.append(qa_item)
        if qa_item.question_std != "":

            qa_item.put_prompt(prompt="文本: %s \n 根据文本说出: %s" % (context, qa_item.question_std))
            new_data.append(qa_item.__dict__)

# 输出转换后的结果
new_json = json.dumps(new_data, ensure_ascii=False, indent=2)
print(new_json)
print(len(new_data))

# 将JSON字符串写入文件

with open(out_path, "w") as json_file:
    json_file.write(new_json)

print("JSON data has been written to", out_path)
