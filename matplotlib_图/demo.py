import matplotlib.pyplot as plt
import matplotlib

# print(matplotlib.rc_params())       #方式二
# print(matplotlib.rcParamsDefault)   #方式三
# print(matplotlib.rcParams['font.sans-serif'])
# 中文字体
matplotlib.rcParams['font.sans-serif']=['SimHei']
matplotlib.rcParams['axes.unicode_minus']=False
# import shutil
# folder_path = matplotlib.get_cachedir()
# shutil.rmtree(folder_path)

print(matplotlib.matplotlib_fname())
# print(matplotlib.get_backend())    #返回matplotlib的后端
print(f"matplotlib cache: {matplotlib.get_cachedir()}")   #缓存目录

print(f"matplotlib configdir: {matplotlib.get_configdir()}")  #配置目录
print(matplotlib.get_data_path())  #数据路径


plt.legend()
# plt.rcParams['font.sans-serif']=['SimHei']
# plt.rcParams['axes.unicode_minus']=False

# 数据
频率 = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
周期 = [10, 5, 3.36, 2.48, 2, 1.68, 1.44, 1.28, 1.12, 1]

matplotlib.use('TkAgg')   #弹出
# 创建图表
plt.figure(figsize=(8, 6))
plt.plot(频率, 周期, marker='o', linestyle='-')
plt.title('周期随着频率变化')
plt.xlabel('频率(Hz)')
plt.ylabel('周期(ms)')
plt.grid(True)

# 显示图表
plt.show()


