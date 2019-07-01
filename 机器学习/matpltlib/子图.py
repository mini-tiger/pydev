import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# fig = plt.figure()
# 添加三个 子图
# （2，2，1）在2 行2列  范围内，第一个位置
# ax1 = fig.add_subplot(2,2,1)
# ax2 = fig.add_subplot(2,2,2)
# ax3 = fig.add_subplot(2,2,4)  # （2，2，4）在2 行2列  范围内，第4个位置
# plt.show()


# fig = plt.figure()
fig = plt.figure(figsize=(8, 8))  # figsize 画布的 长与宽
ax1 = fig.add_subplot(2, 1, 1)  # 2行1列  1的位置
ax2 = fig.add_subplot(2, 1, 2)  # 2行1列  2的位置

ax1.plot(np.random.randint(low=1, high=5, size=5), np.arange(5))
ax2.plot(np.arange(10) * 3, np.arange(10))
plt.show()

###########################
fig = plt.figure(figsize=(10,6)) #初始化画布
unrate = pd.read_csv('unrate.csv')
unrate['DATE'] = pd.to_datetime(unrate['DATE'])
unrate['MONTH'] = unrate['DATE'].dt.month # 转换CSV中 DATE中的年 为  月
print(unrate["MONTH"].values)

colors = ['red', 'blue', 'green', 'orange', 'black']
for i in range(5):
    start_index = i*12  # csv文件中 每12条数据 会加一年， 则是 5年中，每个月的数据
    end_index = (i+1)*12
    subset = unrate[start_index:end_index]
    label = str(1948 + i)
    plt.plot(subset['MONTH'], subset['VALUE'], c=colors[i], label=label) # 循环5次，5 条线，label
plt.legend(loc='upper left') # label 在图中左侧,    best 是右侧
print(help(plt.legend))
plt.xlabel('Month, Integer')
plt.ylabel('Unemployment Rate, Percent')
plt.title('Monthly Unemployment Trends, 1948-1952')

plt.show()