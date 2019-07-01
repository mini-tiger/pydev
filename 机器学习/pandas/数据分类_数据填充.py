import pandas as pd
import numpy as np

titanic_survival = pd.read_csv("titanic_train.csv")
age = titanic_survival["Age"]
# print(age.loc[0:10])

age_is_null = pd.isnull(age)
# print(age_is_null) # bool 列表

age_null_true = age[age_is_null]  # 按照 bool列表 只打印true的
# print age_null_true
age_null_count = len(age_null_true)
print(age_null_count)

# 年龄平均值
mean_age = sum(titanic_survival["Age"]) / len(titanic_survival["Age"])
print(mean_age)  # NaN  由于数据中包含 缺失值

# 平均值
# 方法一
good_ages = titanic_survival["Age"][age_is_null == False]
# print good_ages
correct_mean_age = sum(good_ages) / len(good_ages)
print(correct_mean_age)

# 方法二
correct_mean_age = titanic_survival["Age"].mean()
print(correct_mean_age)

print("*" * 100)
# todo 数据填充
# https://blog.csdn.net/donghf1989/article/details/51167083

age1 = age.loc[15:20]  # 默认数据 包含两个  没有年龄的行
print(age1)
# 用0 填充缺失
print(age1.fillna(0))
# print(age1) # 原数组不会改变

# 用平均值填充
print(age1.fillna(age1.mean()))


print("*" * 100)
# todo 缺失值删除
print('Age' in titanic_survival.columns.values.tolist())
drop_na_columns = titanic_survival.dropna(axis=1) # 删除所有 带有 空数据的列,Age 列带有空数据
print('Age' in drop_na_columns.columns.values.tolist())

print(len(titanic_survival))
new_titanic_survival = titanic_survival.dropna(axis=0,subset=["Age", "Sex"]) # 这两列中，带有空数据的行，删除
print(len(new_titanic_survival))



print("*" * 100)
# todo 分组 分类 统计
passenger_classes = [1, 2, 3]  # 1,2,3等级 舱室
fares_by_class = {}
for this_class in passenger_classes:
    pclass_rows = titanic_survival[titanic_survival["Pclass"] == this_class]  # 例如 level 1级别 舱室的行
    pclass_fares = pclass_rows["Fare"]  # 找到 车票价格列
    fare_for_class = pclass_fares.mean()  # 计算车票价格平均值
    fares_by_class[this_class] = fare_for_class  # 统计保存
print(fares_by_class)

# 不同 舱室（pclass） 平均的 获救人数
# select avg(survived) from 数据表 group by Pclass
passenger_survival = titanic_survival.pivot_table(index="Pclass", values="Survived", aggfunc=np.mean)
print(passenger_survival)

# 不同 码头（Embarked） 总共的，船票费用 ， 获救人数
# select sum(Fare),sum(Survived) from 数据表 group by Embarked
port_stats = titanic_survival.pivot_table(index="Embarked", values=["Fare", "Survived"], aggfunc=np.sum)
print(port_stats)
