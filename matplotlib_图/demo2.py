import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 生成一些示例数据
x = np.linspace(0, 10, 100)
y1 = np.sin(x) * 550
y2 = np.cos(x) * 55

# 设置Seaborn样式
sns.set(context='notebook', style="whitegrid")

# 创建图表和子图
fig, ax = plt.subplots(figsize=(8, 6),dpi=200)

# 绘制两条曲线
ax.plot(x, y1, label='sin(x)', linestyle='-', marker='o')
ax.plot(x, y2, label='cos(x)', linestyle='--', marker='s')

# 添加标题和标签
ax.set_title('Sin and Cos Curves')
ax.set_xlabel('X-axis')
# ax.set_ylabel('Y-axis')
# 设置 Y 轴标签在 Y 轴的上方
ax.yaxis.set_label_coords(0.00, 1.01) # 左右，上下
ax.set_ylabel('Y-axis', rotation=0, ha='right')
# 显示图例
ax.legend()

# 调整右侧空白宽度
right_margin = 0.01
fig.subplots_adjust(right=1 - right_margin)
left_margin = 0.08
fig.subplots_adjust(left=left_margin)
# 移除右边和上边的边框
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)

# 显示网格线
ax.grid(color='gray', linestyle='--', linewidth=0.5)
plt.savefig("temp.png")
# 显示图表
plt.show()

