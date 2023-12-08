import time

from sentence_transformers import SentenceTransformer, util

from AI.tools.tool import FusionJson
from tools import tool
import numpy as np
model = SentenceTransformer('all-MiniLM-L6-v2')
# model = SentenceTransformer('all-MiniLM-L12-v2')
# model = SentenceTransformer('all-mpnet-base-v2')

# 文本列表


# # 按照相似度分数进行排序打印
# pairs = sorted(pairs, key=lambda x: x['score'], reverse=True)
#
# for pair in pairs:
#     i, j = pair['index']
#     print("{:<30} \t\t {:<30} \t\t Score: {:.4f}".format(sentences[i], sentences[j], pair['score']))

class Similarity_Score(FusionJson):

    def process(self):
        print("!!! Current File: %s" % self.src_json_file_abspath)

        # print(src_json_file_abspath, src_rebuild_abspath)
        self.rebuild()
        # fusion.rebuild()

        # print(out_file)
        qas = self.read_json()
        # self.qas_list_func(qas)
        # self.compute()
        output = self.compute(qas)

        # print(output)

        self.write_json(output)

        # num format
        # num_file = os.path.join(out_dir, file_prefix) + "_%s.modified_score.txt" % (file_date)
        self.num_format()
        print()
        print("Current File: %s,num_format completed,output: %s" % (self.num_out_file, self.num_modify_file))
        # 提取问题

        self.read_json_and_write()
        print("Current File: %s,提取问题 completed,output: %s" % (self.src_json_file_abspath, self.questions_file))

    def compute(self,qas):
        # 计算embeddings
        embeddings = model.encode(qas, convert_to_tensor=True)

        # 计算不同文本之间的相似度
        cosine_scores = util.cos_sim(embeddings, embeddings)
        # print(cosine_scores)
        # 将余弦相似度矩阵转换为 NumPy 数组
        cosine_scores_np = np.array(cosine_scores)
        # print(cosine_scores_np)
        # 保存结果
        # pairs = []
        # for i in range(len(cosine_scores) - 1):
        #     for j in range(i + 1, len(cosine_scores)):
        #         pairs.append({'index': [i, j], 'score': cosine_scores[i][j]})
        #
        # print(pairs)

        return cosine_scores_np

    def qas_list_func(self, qas):
        self.qas_list = [q.prompt for q in qas]
        # print(qas_list)

    def __init__(self, **kwargs):
        # self.file_date = tool.DateStr()
        # self.file_prefix = kwargs["file_prefix"]
        # self.run_type = kwargs["run_type"]

        # self.src_json_file = "%s.json" % (self.file_prefix)
        #
        # self.src_json_file_abspath = "/mnt/AI_Json/%s" % (self.src_json_file)
        # self.src_rebuild_abspath = self.src_json_file_abspath + "_%s.%s_rebuild.json" % (self.file_date, self.run_type)
        FusionJson.__init__(self, file_prefix=kwargs["file_prefix"], run_type=kwargs["run_type"], target= kwargs["run_type"])

        # 中文句向量模型(CoSENT)，中文语义匹配任务推荐，支持fine-tune继续训练
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.qas_list = []
        self.num_out_file = self.src_json_file_abspath + "_%s.%s_score.txt" % (self.file_date, self.run_type)
        self.num_modify_file = self.src_json_file_abspath + "_%s.%s_modified_score.txt" % (
        self.file_date, self.run_type)

        self.questions_file = self.src_json_file_abspath + "_%s.%s_prompt_output.txt" % (self.file_date, self.run_type)


if __name__ == "__main__":
    file_list = ["evdc", "全域托管云", "上海外高桥", "ccib", "dc", "超互联"]
    # file_list = ["上海外高桥荷丹数据中心QA", "超互联_全域托管云等白皮书", ]
    # file_list = ["超互联", "荷丹", ]
    for f in file_list:
        start = time.time()
        ss = Similarity_Score(file_prefix=f, run_type="Transformer", target=0.9)
        ss.process()
        end = time.time()
        print("完成时间: %f s" % (end - start))  #
