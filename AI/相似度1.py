from sentence_transformers import SentenceTransformer, util
import torch,os
os.environ['HTTP_PROXY']='http://localhost:1081'
os.environ['HTTPS_PROXY']='http://localhost:1081'
from huggingface_hub import hf_hub_download
# hf_hub_download('unstructuredio/yolo_x_layout', 'yolox_l0.05.onnx')
def calculate_similarity(sentence1, sentence2, model_name='all-MiniLM-L6-v2'):
    # 加载模型
    model = SentenceTransformer(model_name)

    # 编码句子
    embedding1 = model.encode(sentence1, convert_to_tensor=True)
    embedding2 = model.encode(sentence2, convert_to_tensor=True)

    # 计算余弦相似度
    similarity_score = util.pytorch_cos_sim(embedding1, embedding2).item()

    return similarity_score

# 使用示例
sentence1 = "The quick brown fox jumps over the lazy dog."
sentence2 = "A fast auburn canine leaps above an idle hound."

similarity = calculate_similarity(sentence1, sentence2)
print(f"句子1: {sentence1}")
print(f"句子2: {sentence2}")
print(f"相似度分数: {similarity:.4f}")

# 另一个例子
phrase1 = "陶钧参与过几个项目"
phrase2 = "2022年陶钧负责项目的数量"

similarity = calculate_similarity(phrase1, phrase2)
print(f"\n短语1: {phrase1}")
print(f"短语2: {phrase2}")
print(f"相似度分数: {similarity:.4f}")

# 使用不同的模型
print("\n使用不同的模型:")
similarity = calculate_similarity(phrase1, phrase2, model_name='shibing624/text2vec-base-chinese')
print(f"短语1: {phrase1}")
print(f"短语2: {phrase2}")
print(f"相似度分数: {similarity:.4f}")