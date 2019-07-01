import pandas as pd
import numpy as np

titanic_survival = pd.read_csv("titanic_train.csv")


def hundredth_row(column):  # column 是每一列
    # Extract the hundredth item
    hundredth_item = column.iloc[99]  # iloc 按照索引提取 ，每列第100行数据
    # hundredth_item = column.head()
    return hundredth_item


# Return the hundredth item from each column
hundredth_row = titanic_survival.apply(hundredth_row)
print(hundredth_row)

print("*" * 100)


# 每个包含缺失值列的  缺失的个数

def not_null_count(column):
    column_null = pd.isnull(column)  # [False,True...]  列表

    null = column[column_null]  # 数值
    return len(null)
    # return len(list(filter(lambda x: x == True, column_null)))

column_null_count = titanic_survival.apply(not_null_count,axis=0)
print(column_null_count)

print("*" * 100)
# 一等舱室  更名为 First Class
def which_class(row):
    pclass = row['Pclass']
    if pd.isnull(pclass):
        return "Unknown"
    elif pclass == 1:
        return "First Class"
    elif pclass == 2:
        return "Second Class"
    elif pclass == 3:
        return "Third Class"

classes = titanic_survival.apply(which_class, axis=1) # 按照行取值，默认是0
print(classes.head(3))
print("*" * 100)

#综合
# 年轻人，与老年人  的分别 幸存人数
def generate_age_label(row):
    age = row["Age"]
    if pd.isnull(age):
        return "unknown"
    elif age < 18:
        return "年轻人"
    else:
        return "老年人"

age_labels = titanic_survival.apply(generate_age_label, axis=1)
# print(age_labels)
titanic_survival['age_labels'] = age_labels # 数据集加入 自定义数据标签
age_group_survival = titanic_survival.pivot_table(index="age_labels", values="Survived",aggfunc=np.sum) # , aggfunc=np.mean 默认
print(age_group_survival)