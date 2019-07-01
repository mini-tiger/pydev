import pandas as pd
import matplotlib.pyplot as plt
reviews = pd.read_csv('fandango_scores.csv')
cols = ['FILM', 'RT_user_norm', 'Metacritic_user_nom', 'IMDB_norm', 'Fandango_Ratingvalue']
norm_reviews = reviews[cols]
# print(norm_reviews[:5])

fandango_distribution = norm_reviews['Fandango_Ratingvalue'].value_counts()
fandango_distribution = fandango_distribution.sort_index()

imdb_distribution = norm_reviews['IMDB_norm'].value_counts() # 数据统计，每个得分分别有多少个
imdb_distribution = imdb_distribution.sort_index()

print(fandango_distribution)
print(imdb_distribution)

fig, ax = plt.subplots()
# todo bins  代表将   多个 数值 分成 区间 [range(10)] 可以分成2 个区间 [0-5,5-10]
ax.hist(norm_reviews['Fandango_Ratingvalue']) # hist 带有bin的柱形图,bins 默认是10,  将数据分成10个区间
ax.hist(norm_reviews['Fandango_Ratingvalue'],bins=20)
ax.hist(norm_reviews['Fandango_Ratingvalue'], range=(4, 5),bins=20) # range 只取 4，5之间的数值显示，并且bins 显示20个区间
plt.show()





fig = plt.figure(figsize=(5,20))
ax1 = fig.add_subplot(4,1,1) # 在画布 4行1列，第1个位置
ax2 = fig.add_subplot(4,1,2)
ax3 = fig.add_subplot(4,1,3)
ax4 = fig.add_subplot(4,1,4)

ax1.hist(norm_reviews['Fandango_Ratingvalue'], bins=20, range=(0, 5))
ax1.set_title('Distribution of Fandango Ratings')
ax1.set_ylim(0, 50) # Y轴区间

ax2.hist(norm_reviews['RT_user_norm'], 20, range=(0, 5))
ax2.set_title('Distribution of Rotten Tomatoes Ratings')
ax2.set_ylim(0, 50)

ax3.hist(norm_reviews['Metacritic_user_nom'], 20, range=(0, 5))
ax3.set_title('Distribution of Metacritic Ratings')
ax3.set_ylim(0, 50)

ax4.hist(norm_reviews['IMDB_norm'], 20, range=(0, 5))
ax4.set_title('Distribution of IMDB Ratings')
ax4.set_ylim(0, 50)

plt.show()

# todo 盒图， 数据集中在 哪几个分值， 红色线 代表中间值， 上下的横线 代表最大最小值
num_cols = ['RT_user_norm', 'Metacritic_user_nom', 'IMDB_norm', 'Fandango_Ratingvalue']
fig, ax = plt.subplots()
ax.boxplot(norm_reviews[num_cols].values) ## 多个指标的盒图
ax.set_xticklabels(num_cols, rotation=45)
ax.set_ylim(0,5)
plt.show()