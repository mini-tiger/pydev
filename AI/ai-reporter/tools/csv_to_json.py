import csv
import json

# 读取 CSV 文件
csv_file = 'output.csv'

# 存储数据的列表
data = []

with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
    # 创建 CSV 读取器对象
    csv_reader = csv.DictReader(file)

    # 逐行读取 CSV 文件
    for row in csv_reader:
        # 将每一行数据添加到列表中
        data.append(row)

# 将数据列表转换为 JSON 格式
json_data = json.dumps(data, indent=4, ensure_ascii=False)

# 将 JSON 数据写入到文件中
with open('data.json', 'w',encoding="utf-8") as json_file:
    json_file.write(json_data)

print("CSV 文件已成功转换为 JSON 文件。")
