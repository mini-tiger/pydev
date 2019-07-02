

# 默认只有6个颜色
# 4-可视化库Seaborn/Seaborn-2Color.ipynb

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(rc={"figure.figsize": (6, 6)})

sns.palplot(sns.hls_palette(8, l=.7, s=.9))
# l-亮度 lightness
# s-饱和 saturation
plt.show()

# 分成8个不同颜色
data = np.random.normal(size=(20, 8)) + np.arange(8) / 2
sns.boxplot(data=data,palette=sns.color_palette("hls", 8))
plt.show()


# 逐渐变深
sns.palplot(sns.cubehelix_palette(8, start=.5, rot=-.75))
plt.show()


x, y = np.random.multivariate_normal([0, 0], [[1, -.5], [-.5, 1]], size=300).T
pal = sns.dark_palette("green", as_cmap=True)
sns.kdeplot(x, y, cmap=pal)
plt.show()