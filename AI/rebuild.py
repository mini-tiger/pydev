# coding:utf-8
import json

# 从原始文件读取数据
with open("/mnt/荷丹数据中心QA.txt", "r", encoding="utf-8") as original_file:
    original_data = json.load(original_file)

# 构建目标数据
target_data = []
for data in original_data:
    target = {
        "prompt": data["question"],
        "chosen": data["answer"],
        "response": "",
        "rejected": ""
    }
    target_data.append(target)

# 将目标数据写入文件
with open("target.json", "w", encoding="utf-8") as target_file:
    json.dump(target_data, target_file, ensure_ascii=False, indent=2)

print("Conversion completed.")
