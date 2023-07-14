import jieba
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import TfidfVectorizer

# 示例句子
sentence1 = "我喜欢吃水果"
sentence2 = "水果是我喜欢吃的"

# 使用jieba进行分词和预处理
tokens1 = jieba.lcut(sentence1)
tokens2 = jieba.lcut(sentence2)

# 合并分词结果为字符串
text1 = " ".join(tokens1)
text2 = " ".join(tokens2)

# 构建TF-IDF向量
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform([text1, text2]).toarray()

# 计算余弦相似度
similarity = 1 - cosine(vectors[0], vectors[1])

# 打印结果
print("余弦相似度:", similarity)


import jieba

# 示例句子
sentence1 = "我喜欢吃水果"
sentence2 = "水果是我喜欢吃的"

# 使用jieba进行分词
tokens1 = set(jieba.lcut(sentence1))
tokens2 = set(jieba.lcut(sentence2))

# 计算Jaccard相似度
intersection = len(tokens1 & tokens2)
union = len(tokens1 | tokens2)
jaccard_similarity = intersection / union

# 打印结果
print("Jaccard相似度分数:", jaccard_similarity)
