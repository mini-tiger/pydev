import pandas as pd


def read_json_and_write(file, output_file):
    df = pd.read_json(file)
    with open(output_file, "w") as out_file:
        for index, row in df.iterrows():
            q = row.get("question")
            out_file.write("%d  %s\n" % (index, q))

if __name__ == "__main__":
    input_file = "/mnt/AI_Json/re/上海静安数据中心QA_20230918.json "
    output_file = "/mnt/prompt_output.txt"
    read_json_and_write(input_file, output_file)
