import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
from openai import OpenAI
import re
import PyQt5
from markdown_strings import header, table, code_block,table_from_rows

class ProjectWindow:
    def __init__(self):
        self.resume_path = r"E:\codes\pydev\project_sjhl\马小龙-射频西安.pdf"
        self.job_description_path = r"E:\codes\pydev\project_sjhl\renzhizige-RF-3.xlsx"
        self.markdown_table_row = [["序号","技能","分数","分析"]]

    def generate_markdown_table(self):
        data = self.markdown_table_row
        if not data or not data[0]:
            return ""

        # Get the number of columns
        num_columns = len(data[0])

        # Ensure all data elements are strings and escape any special characters
        def escape_markdown_special_chars(text):
            return str(text).replace('|', '\\|').replace('\n', ' ')

        # Generate the header
        header = "| " + " | ".join(escape_markdown_special_chars(cell) for cell in data[0]) + " |"

        # Generate the separator
        separator = "| " + " | ".join(["---"] * num_columns) + " |"

        # Generate the rows
        rows = ["| " + " | ".join(escape_markdown_special_chars(cell) for cell in row) + " |" for row in data[1:]]

        # Combine all parts
        markdown_table = "\n".join([header, separator] + rows)

        return markdown_table

    def write_md(self,markdown_table):
        with open('output.md', 'w', encoding='utf-8') as file:
            file.write(markdown_table)

    def analyze_clicked(self):

        client = OpenAI(
            api_key="sk-FPO8iAP6oogKpi6K2Bh3PVYosDIUUfXT8nWSNw8oODsEc8Vb",
            base_url="https://api.moonshot.cn/v1",
        )

        file_object = client.files.create(file=Path(self.resume_path), purpose="file-extract")

        file_content = client.files.content(file_id=file_object.id).text

        file_object2 = client.files.create(file=Path(self.job_description_path), purpose="file-extract")

        file_content2 = client.files.content(file_id=file_object2.id).text
        default_text = '第一个文件是求职者简历，第二个excel文件的每一行都是不同技术技能的期望要求，请分析求职者简历，并逐条给出各个技能的符合程度分析，最好能逐条给出分值，满分100分。请按照以下的语句样式进行分析：1、高端机械校准件技术-1 (LF~20/26.5GHz, SOTL类型，难度等级4)：评分：0分分析：求职者简历中未提及机械校准件技术，缺乏直接相关经验。\n'
        messages = [
            {
                "role": "system",
                "content": file_content2,
            },
            {
                "role": "system",
                "content": file_content,
            },

            {"role": "user", "content": default_text},
        ]
        print(messages[2])
        # 然后调用 chat-completion, 获取 kimi 的回答
        completion = client.chat.completions.create(
            model="moonshot-v1-32k",
            messages=messages,
            temperature=0.3,
            max_tokens=4096,
            stream=True,
        )


        # 分行处理completion.choices[0].message.content，并将每行作为一个新条目插入到表格中
        # i = 1
        collected_messages = []
        for idx, chunk in enumerate(completion):
            chunk_message = chunk.choices[0].delta
            if not chunk_message.content:
                continue
            # 解析chunk_message.content的内容，并逐行插入到表格中
            collected_messages.append(chunk_message.content)  # save the message
            if chunk_message.content == "。\n\n":
                full_conversation = ''.join(collected_messages) + "\n"
                print(f"Full conversation received: {full_conversation}")
                pattern = r'(\d+)、(.*?：评分：\d+分)\n分析：(.*?)\n'
                for match in re.finditer(pattern, full_conversation):
                    serial = match.group(1)  # 序号，作为第一列
                    skill_and_score = match.group(2)  # 技能和评分，需要进一步分割
                    analysis = match.group(3)  # 分析，作为第四列

                    # 进一步分割技能和评分
                    skill, score = skill_and_score.split("：评分：")
                    print(f"serial:{serial},analysis:{analysis},skill:{skill},score:{score}")
                    self.markdown_table_row.append([serial,skill,score,analysis])
                collected_messages = []
                    # self.markdown_table_row.append([serial,skill,score,analysis])
        #
        #             # 插入到表格中
        #             self.tree.insert("", tk.END, values=(serial, skill, score, analysis))
        #             self.master.update_idletasks()  # 强制更新界面
        #
                # collected_messages = []
        #         # 使用正则表达式匹配所需内容
        #         pattern = r'(\d+)、(.*?：评分：\d+分)\n分析：(.*?)\n'
        #
        # #            chunk_message_content = chunk_message.content.replace('\n', '').replace('\r', '')
        #
        # #            print(f"#{idx}: {''.join(collected_messages)}")
        #
        # # 查找所有匹配项并插入到表格中
        # full_conversation = ''.join(collected_messages) + "\n"
        # pattern = r'(\d+)、(.*?：评分：\d+分)\n分析：(.*?)\n'
        # for match in re.finditer(pattern, full_conversation):
        #     serial = match.group(1)  # 序号，作为第一列
        #     skill_and_score = match.group(2)  # 技能和评分，需要进一步分割
        #     analysis = match.group(3)  # 分析，作为第四列
        #
        #     # 进一步分割技能和评分
        #     skill, score = skill_and_score.split("：评分：")
        #
        #     # # 插入到表格中
        #     # self.tree.insert("", tk.END, values=(serial, skill, score, analysis))
        #     # self.master.update_idletasks()  # 强制更新界面
        #
        #     print(f"2--serial:{serial},analysis:{analysis},skill:{skill},score:{score}")

if __name__=="__main__":
    p=ProjectWindow()
    p.analyze_clicked()
    md_data = p.generate_markdown_table()
    p.write_md(md_data)
    # p.output_markdown()
