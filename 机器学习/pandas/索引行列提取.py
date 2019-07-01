import pandas

food_info = pandas.read_csv("food_info.csv")
# print(food_info.loc[0])
# print(food_info.loc[0:2]) # todo 注意这里是包含 索引2的
# print(food_info.loc[[2, 3]])  # 这里是 第2，3 索引行
twoRows = food_info.loc[0:1]
print(twoRows[food_info.columns[0]])  # 查看某列，
# 0    1001
# 1    1002
# Name: NDB_No, dtype: int64

print(food_info.loc[2,"Water_(g)"]) # 索引为2 是 第三行，Water_(g) 列的数据


cols = ["NDB_No", "Water_(g)"]
print(twoRows[cols]) # 指定列名，[["col1","col2"]]
#    NDB_No  Water_(g)
# 0    1001      15.87
# 1    1002      15.87

# todo 综合
col_names = food_info.columns.tolist() # 列名 转换为列表
#print col_names
gram_columns = []

for c in col_names:
    if c.endswith("(g)"):
        gram_columns.append(c)  # 所有列名中包含 (g) 关键字的
gram_df = food_info[gram_columns]
print(gram_df.head(5))
'''
Water_(g)  Protein_(g)  Lipid_Tot_(g)  ...  FA_Sat_(g)  FA_Mono_(g)  FA_Poly_(g)
0      15.87         0.85          81.11  ...      51.368       21.021        3.043
1      15.87         0.85          81.11  ...      50.489       23.426        3.012
2       0.24         0.28          99.48  ...      61.924       28.732        3.694
3      42.41        21.40          28.74  ...      18.669        7.778        0.800
4      41.11        23.24          29.68  ...      18.764        8.598        0.784

[5 rows x 10 columns]  显示了 5行其中的10列

'''
