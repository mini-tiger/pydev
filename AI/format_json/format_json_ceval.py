import json
from models import data
import os, csv


class FormatCeval():
    def __init__(self, **kwargs):
        self.file = kwargs["file"]
        self.out_dir = kwargs["out_dir"]
        self.out_file = os.path.join(self.out_dir, "%s.json" % os.path.basename(self.file))
        self.csv_data = []
        self.new_data = []

    def read_csv(self):
        try:
            with open(self.file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if 'question' in row:
                        # The key 'key_to_check' exists in the current row
                        # You can access its value using row['key_to_check']
                        q = row["question"]
                    else:
                        # The key 'key_to_check' does not exist in the current row
                        q = row["Question"]
                    if 'answer' in row:
                        # The key 'key_to_check' exists in the current row
                        # You can access its value using row['key_to_check']
                        a = row["answer"]
                    else:
                        # The key 'key_to_check' does not exist in the current row
                        a = row["Answer"]
                    question_data = {
                        # "id": row["id"],
                        "question": q,

                        "A": row["A"],
                        "B": row["B"],
                        "C": row["C"],
                        "D": row["D"],
                        "answer": a
                    }

                    self.csv_data.append(question_data)
        except Exception as e:
            print(self.file,e)
        # print(self.csv_data)
        # print(len(self.csv_data))

    def covert_qa(self):
        self.new_data = []

        for qa in self.csv_data:
            # qa_list = []
            qa_item = data.PromptQA()
            if qa["question"].find("_") != -1:
                questation = "%s %s A. %s B. %s C. %s D. %s" % (
                qa["question"], "前面下划线位置应该填入哪个选项,只输出选项字母", qa["A"], qa["B"], qa["C"], qa["D"])
            # questation = questation.replace("____", "哪个选项,只输出正确选项")
            else:
                questation = "%s A. %s B. %s C. %s D. %s" % (
                qa["question"],  qa["A"], qa["B"], qa["C"], qa["D"])
            # print(question,len(question))
            # print(answer,len(answer))
            qa_item.put_data(question_std=questation, answers_std=qa["answer"], answers_real="")
            # qa_list.append(qa_item)
            if qa_item.question_std != "":
                qa_item.put_prompt(prompt=questation)
                self.new_data.append(qa_item.__dict__)

    def process(self):
        self.read_csv()
        self.covert_qa()
        self.write_csv()

    def write_csv(self):
        new_json = json.dumps(self.new_data, ensure_ascii=False, indent=2)
        with open(self.out_file, "w") as json_file:
            json_file.write(new_json)


if __name__ == "__main__":
    # src_dir="/mnt/AI_Json/ceval-exam/val"
    src_dir = "/mnt/AI_Json/cmmlu_v1_0_1/test"
    file_list = os.listdir(src_dir)
    print(file_list)
    current_directory = os.path.dirname(__file__)
    # 将JSON字符串解析为Python字典
    # file_path = os.path.join("/mnt/AI_Json/ceval-exam/val/accountant_val.csv")
    for fi in file_list:
        # out_path = os.path.join(current_directory, "json_data", "ceval", "translation.json")
        f = FormatCeval(file=os.path.join(src_dir, fi), out_dir=os.path.join(current_directory, "json_data", "cmmlu"))
        f.process()
