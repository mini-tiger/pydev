import seaborn as sns
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def sinplot(flip=1):
    x = np.linspace(0, 14, 100)  # 0到14之间的100个数
    for i in range(1, 7):
        plt.plot(x, np.sin(x + i * .5) * (7 - i) * flip)

# sns.set() # seaborn 的默认参数

# sns.set_style("whitegrid") # 设置风格
# darkgrid
# whitegrid
# dark
# white
# ticks

data = np.random.normal(size=(20, 6)) + np.arange(6) / 2
# sns.boxplot(data=data)

# sinplot()
sns.despine(left=True)  # 为空去掉四个方向 的轴线，left=True 保留左边的轴

sns.violinplot(data)
sns.despine(offset=10) # 图形距离 X轴的距离
plt.show()

# 子图风格不同
with sns.axes_style("darkgrid"):
    plt.subplot(211)
    sinplot()
plt.subplot(212)
sinplot(-1)
plt.show()


sns.set() # 清空设置

sns.set_context("paper") # 画出的大小，paper,talk,poster,notebook 从小到大
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5}) # font_scale 字体大小，rc 线的粗细

plt.figure(figsize=(8, 6))

sinplot()
plt.show()


