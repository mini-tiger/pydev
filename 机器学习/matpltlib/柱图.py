import pandas as pd
reviews = pd.read_csv('fandango_scores.csv')
cols = ['FILM', 'RT_user_norm', 'Metacritic_user_nom', 'IMDB_norm', 'Fandango_Ratingvalue', 'Fandango_Stars']
norm_reviews = reviews[cols]
print(norm_reviews[:1])

import matplotlib.pyplot as plt
from numpy import arange
#The Axes.bar() method has 2 required parameters, left and height.
#We use the left parameter to specify the x coordinates of the left sides of the bar.
#We use the height parameter to specify the height of each bar
num_cols = ['RT_user_norm', 'Metacritic_user_nom', 'IMDB_norm', 'Fandango_Ratingvalue', 'Fandango_Stars']

bar_heights = norm_reviews.ix[0, num_cols].values # 取其中5列的数据
#print bar_heights
bar_positions = arange(5) + 0.75 #每个柱子的 偏移，离 原点 多远
#print bar_positions
fig, ax = plt.subplots()
ax.bar(bar_positions, bar_heights, 0.5) # 0.5 是柱子的宽度
plt.show()

###########################
num_cols = ['RT_user_norm', 'Metacritic_user_nom', 'IMDB_norm', 'Fandango_Ratingvalue', 'Fandango_Stars']

bar_widths = norm_reviews.ix[0, num_cols].values
bar_positions = arange(5) + 0.75
tick_positions = range(1,6)
fig, ax = plt.subplots()
ax.barh(bar_positions, bar_widths, 0.5)   # 柱子 横向显示

ax.set_yticks(tick_positions)  # y轴显示的 尺度
ax.set_yticklabels(num_cols)   # x轴显示的 尺度
ax.set_ylabel('Rating Source') #  # y轴显示的 标签
ax.set_xlabel('Average Rating')
ax.set_title('Average User Rating For Avengers: Age of Ultron (2015)')
plt.show()