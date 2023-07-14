import jieba
import nltk
import string
import os
os.environ["HTTP_PROXY"] = "http://172.22.50.191:1081"
os.environ["HTTPS_PROXY"] = "http://172.22.50.191:1081"
from collections import Counter
nltk.download('stopwords')
nltk.download('corpora')

import jieba
import math
from collections import Counter

def tokenize(text):
    tokens = jieba.lcut(text)
    return tokens

def calculate_cosine_similarity(tokens1, tokens2):
    vector1 = Counter(tokens1)
    vector2 = Counter(tokens2)

    # 计算向量的点积
    dot_product = sum(vector1[word] * vector2[word] for word in vector1 if word in vector2)

    # 计算向量的模长
    magnitude1 = math.sqrt(sum(vector1[word] ** 2 for word in vector1))
    magnitude2 = math.sqrt(sum(vector2[word] ** 2 for word in vector2))

    # 计算余弦相似度
    cosine_similarity = dot_product / (magnitude1 * magnitude2)
    return cosine_similarity

# 两个要比较的中文句子
sentence1 = "我喜欢吃水果"
sentence2 = "水果是我喜欢吃的"

# 分词
tokens1 = tokenize(sentence1)
tokens2 = tokenize(sentence2)

# 计算相似度
similarity = calculate_cosine_similarity(tokens1, tokens2)

print(f"句子1：{sentence1}")
print(f"句子2：{sentence2}")
print(f"相似度：{similarity}")
