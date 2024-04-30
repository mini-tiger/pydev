from faker import Faker # 25.0
import csv

# 创建一个 Faker 实例，设置为中文
fake = Faker('zh_CN')

# 生成中文用户数据的函数
def generate_users(num_users):
    users = []
    for _ in range(num_users):
        user = {
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address(),
            "phone": fake.phone_number(),
        }
        users.append(user)
    return users

# 写入 CSV 文件的函数
def write_to_csv(users, file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "email", "address", "phone"])
        writer.writeheader()
        for user in users:
            writer.writerow(user)

if __name__ == '__main__':
    # 生成中文用户数据
    users = generate_users(10)

    # 将数据写入 CSV 文件
    write_to_csv(users, 'chinese_users.csv')

    print("CSV 文件已经生成，包含中文数据，并使用 UTF-8 编码。")
