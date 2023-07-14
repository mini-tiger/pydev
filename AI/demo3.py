import jieba, distance
import math, json, requests
from collections import Counter
from text2vec import SentenceModel, cos_sim, Similarity, SimilarityType, EmbeddingType

# sim_model = Similarity("shibing624/text2vec-base-chinese")
sim_model = Similarity("shibing624/text2vec-base-chinese-paraphrase")

target = "http://172.22.240.90:8000"


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


def calculate_jaccard_similarity(tokens1, tokens2):
    set1 = set(tokens1)
    set2 = set(tokens2)

    # 计算Jaccard相似度
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    jaccard_similarity = intersection / union

    # 打印结果
    return jaccard_similarity


def overlay_similarity(tokens1, tokens2):
    set1 = set(tokens1)
    set2 = set(tokens2)
    # 计算重叠系数
    overlap_coefficient = len(set1 & set2) / min(len(set1), len(set2))

    # 打印结果
    return overlap_coefficient


# 两个要比较的中文句子
sentence1 = "我喜欢吃水果"
sentence2 = "水果是我喜欢吃的"

# 分词
tokens1 = tokenize(sentence1)
tokens2 = tokenize(sentence2)

# 计算相似度
cosine_similarity = calculate_cosine_similarity(tokens1, tokens2)
jaccard_similarity = calculate_jaccard_similarity(tokens1, tokens2)
overlap_coefficient = overlay_similarity(tokens1, tokens2)

print(f"句子1：{sentence1}")
print(f"句子2：{sentence2}")
print(f"余弦相似度：{cosine_similarity}")
print(f"Jaccard 相似度：{jaccard_similarity}")
print(f"重叠系数:", overlap_coefficient)
print(sim_model.get_score(sentence1, sentence2))
