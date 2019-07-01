import pandas as pd
import matplotlib.pyplot as plt
from numpy import arange

reviews = pd.read_csv('fandango_scores.csv')
cols = ['FILM', 'RT_user_norm', 'Metacritic_user_nom', 'IMDB_norm', 'Fandango_Ratingvalue', 'Fandango_Stars']
norm_reviews = reviews[cols]
# print(norm_reviews[:1])

fig, ax = plt.subplots()
ax.scatter(norm_reviews['Fandango_Ratingvalue'], norm_reviews['RT_user_norm'])  #scatter 载入数据
ax.tick_params(bottom="off", top="off", left="off", right="off")
ax.set_xlabel('Fandango')
ax.set_ylabel('Rotten Tomatoes')
plt.show()


#############
fig = plt.figure(figsize=(5,10))
ax1 = fig.add_subplot(2,1,1) # 2行一列的 画布， 在第1个位置
ax2 = fig.add_subplot(2,1,2) # 2行一列的 画布， 在第2个位置
ax1.scatter(norm_reviews['Fandango_Ratingvalue'], norm_reviews['RT_user_norm'])
ax1.set_xlabel('Fandango')
ax1.set_ylabel('Rotten Tomatoes')
ax2.scatter(norm_reviews['RT_user_norm'], norm_reviews['Fandango_Ratingvalue'])
ax2.set_xlabel('Rotten Tomatoes')
ax2.set_ylabel('Fandango')
plt.show()

