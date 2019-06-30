import pandas

food_info = pandas.read_csv("food_info.csv")

# print food_info["Iron_(mg)"]
# div_1000 = food_info["Iron_(mg)"] / 1000
# print div_1000
# Adds 100 to each value in the column and returns a Series object.
# add_100 = food_info["Iron_(mg)"] + 100

# Subtracts 100 from each value in the column and returns a Series object.
print(food_info["Iron_(mg)"].head() - 100)  # 按照列名 计算

# Multiplies each value in the column by 2 and returns a Series object.
# print(food_info["Iron_(mg)"].head() * 2)

# water_energy = food_info["Water_(g)"] * food_info["Energ_Kcal"]  # 多列数据提取计算

print("是否包含Iron_(g)列", len(list(filter(lambda x: x.find("Iron_(g)") != -1, food_info.columns.tolist()))) > 0, ",shape",
      food_info.shape)

iron_grams = food_info["Iron_(mg)"] / 1000
food_info["Iron_(g)"] = iron_grams  # 将数据 加入新的列

print("是否包含Iron_(g)列", len(list(filter(lambda x: x.find("Iron_(g)") != -1, food_info.columns.tolist()))) > 0, ",shape",
      food_info.shape)
print(food_info["Iron_(g)"].head(1))

print("*"*100)

max_calories = food_info["Energ_Kcal"].max()
print(food_info["Energ_Kcal"].max())  # 每一列最大值
print(food_info["Energ_Kcal"].min())
print(food_info["Energ_Kcal"].mean())# 每一列平均值


# Divide the values in "Energ_Kcal" by the largest value.
# normalized_calories = food_info["Energ_Kcal"] / max_calories
# normalized_protein = food_info["Protein_(g)"] / food_info["Protein_(g)"].max()
# normalized_fat = food_info["Lipid_Tot_(g)"] / food_info["Lipid_Tot_(g)"].max()
# food_info["Normalized_Protein"] = normalized_protein
# food_info["Normalized_Fat"] = normalized_fat