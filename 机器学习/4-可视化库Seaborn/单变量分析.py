import numpy as np
import pandas as pd
from scipy import stats, integrate
import matplotlib.pyplot as plt

import seaborn as sns

sns.set(color_codes=True)
np.random.seed(sum(map(ord, "distributions")))
x = np.random.normal(size=100)
# sns.distplot(x, kde=False) # 直方图 KDE 密度估计
# sns.distplot(x, bins=20, kde=False)  # bins  Y贺范围
sns.distplot(x, kde=False, fit=stats.gamma) # fit 数据分布情况（拆线）
plt.show()



# 散点图  根据均值和协方差生成数据
# 上 方与 右方 是X,Y的 直方图
mean, cov = [0, 1], [(1, .5), (.5, 1)]
data = np.random.multivariate_normal(mean, cov, 200)
df = pd.DataFrame(data, columns=["x", "y"])
sns.jointplot(x="x", y="y", data=df)
plt.show()


# 散点图，
x, y = np.random.multivariate_normal(mean, cov, 1000).T
with sns.axes_style("white"):
    sns.jointplot(x=x, y=y, color="k")  # 正常散点
plt.show()

x, y = np.random.multivariate_normal(mean, cov, 1000).T
with sns.axes_style("white"):
    sns.jointplot(x=x, y=y, kind="hex", color="k") # 对应热度
plt.show()


# 加载 有 4 种 特征的数据集，
# 每两种特征 做散点图，共 4*4 16张图， 两种特征一样，则是直方图
iris = sns.load_dataset("iris") #
print(iris)
sns.pairplot(iris)
plt.show()