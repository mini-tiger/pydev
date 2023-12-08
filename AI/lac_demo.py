
import numpy as np
matrix = np.loadtxt("/mnt/AI_Json/上海外高桥荷丹数据中心QA.score.txt")



# 创建一个示例矩阵
# matrix = np.array([[1.234567, 2.345678], [3.456789, 4.567890]])

# 设置打印选项，保留两位小数，不进行四舍五入
np.set_printoptions(precision=2, suppress=True)

np.savetxt('formatted_matrix.txt', matrix, fmt='%.2f')
