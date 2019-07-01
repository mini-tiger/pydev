
import pandas as pd
import matplotlib.pyplot as plt
unrate = pd.read_csv('unrate.csv')
# print(unrate['DATE'])
unrate['DATE'] = pd.to_datetime(unrate['DATE']) # to_datetime 转换为标准时间格式
# print(unrate.head(12))

first_twelve = unrate[0:12]
print(first_twelve)
#          DATE  VALUE
# 0  1948-01-01    3.4
# 1  1948-02-01    3.8
# 2  1948-03-01    4.0.....

plt.plot(first_twelve['DATE'], first_twelve['VALUE']) # (x轴,y轴)
plt.xticks(rotation=45) # X轴 45度倾斜
plt.xlabel('Month') # x轴 示例
plt.ylabel('Unemployment Rate') # y轴 示例
plt.title('Monthly Unemployment Trends, 1948') # 图片 标题
plt.show()