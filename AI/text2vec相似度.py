import os
import decimal
from text2vec import Similarity, SimilarityType
import pandas as pd
import json, time
import numpy as np

from AI.tools.tool import FusionJson
from tools import tool


# https://www.sbert.net/docs/pretrained_models.html#sentence-embedding-models/


class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        return obj


class Similarity_Score(FusionJson):
    def compute(self, qas):
        result=self.sim_model.get_scores(qas,qas)
        return result

    def process(self):

        print("!!! Current File: %s" % self.src_json_file_abspath)
        # print(src_json_file_abspath, src_rebuild_abspath)
        self.rebuild()


        # print(out_file)
        qas = self.read_json()
        output = self.compute(qas)

        self.write_json(output)

        # num format
        # num_file = os.path.join(out_dir, file_prefix) + "_%s.modified_score.txt" % (file_date)
        self.num_format()
        print()
        print("Current File: %s,num_format completed,output: %s" % (self.num_out_file, self.num_modify_file))
        # 提取问题

        self.read_json_and_write()
        print("Current File: %s,提取问题 completed,output: %s" % (self.src_json_file_abspath, self.questions_file))


if __name__ == "__main__":
    file_list = ["全域托管云", "上海外高桥", "ccib", "dc","超互联","evdc",]
    # file_list = ["上海外高桥荷丹数据中心QA", "超互联_全域托管云等白皮书", ]
    # file_list = ["超互联",gpu2023!#@ "荷丹", ]
    for f in file_list:
        start = time.time()
        ss = Similarity_Score(file_prefix=f, run_type="text2vec", target=0.9)
        ss.process()
        end = time.time()
        print("完成时间: %f s" % (end - start))  #
