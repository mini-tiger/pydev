import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
from openai import OpenAI
import re
import PyQt5


class ProjectWindow:
    def __init__(self, master):
        self.master = master
        master.title("简历分析工具")

        # 应用自定义样式
        self.custom_style()

        # 使窗口最大化
        master.state('zoomed')

        # 单选钮的共享变量
        self.analysis_type = tk.IntVar()
        self.analysis_type.set(1)  # 默认选择逐条分析

        # 单选钮1 - 逐条分析，放在最左边，减少左侧间隔
        self.radio1 = ttk.Radiobutton(master, text="逐条分析", variable=self.analysis_type, value=1,
                                      style='TRadiobutton')
        self.radio1.grid(row=0, column=0, padx=(5, 2), pady=10, sticky="w")

        # 单选钮2 - 总体分析，减少间隔使其更紧凑
        self.radio2 = ttk.Radiobutton(master, text="总体分析", variable=self.analysis_type, value=2,
                                      style='TRadiobutton')
        self.radio2.grid(row=0, column=1, padx=2, pady=10, sticky="w")

        # 单选钮3 - 职业培训建议，同样减少间隔
        self.radio3 = ttk.Radiobutton(master, text="职业培训建议", variable=self.analysis_type, value=3,
                                      style='TRadiobutton')
        self.radio3.grid(row=0, column=2, padx=2, pady=10, sticky="w")

        # 单选钮4 - 其他，调整右侧间隔以保持一致性
        self.radio4 = ttk.Radiobutton(master, text="其他", variable=self.analysis_type, value=4, style='TRadiobutton')
        self.radio4.grid(row=0, column=3, padx=(2, 5), pady=10, sticky="w")

        # 下拉框
        self.label_model = ttk.Label(master, text="选择大模型", style='TLabel')
        self.label_model.grid(row=0, column=4, padx=5, pady=10, sticky="w")
        self.model_options = ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"]
        self.combobox_model = ttk.Combobox(master, values=self.model_options, height=len(self.model_options),
                                           style='TCombobox')
        self.combobox_model.grid(row=0, column=5, padx=5, pady=10, sticky="ew")
        self.combobox_model.set(self.model_options[0])  # 设置默认选择第一个选项

        # 文本框1，长度变为原来的3倍
        self.entry1 = ttk.Entry(master, width=30, font=('TkDefaultFont', 10), style='TEntry')
        self.entry1.grid(row=0, column=6, padx=5, pady=10, sticky="ew")

        # 按钮1 - "选择简历"
        self.button1 = ttk.Button(master, text="选择简历", command=self.select_resume, style='TButton')
        self.button1.grid(row=0, column=7, padx=5, pady=10)

        # 文本框2，长度变为原来的3倍
        self.entry2 = ttk.Entry(master, width=30, font=('TkDefaultFont', 10), style='TEntry')
        self.entry2.grid(row=0, column=8, padx=5, pady=10, sticky="ew")

        # 按钮2 - "选择岗位匹配表"
        self.button2 = ttk.Button(master, text="选择岗位匹配表", command=self.select_job_matching, style='TButton')
        self.button2.grid(row=0, column=9, padx=5, pady=10)

        # 新增按钮 - "开始分析"
        self.button_analyze = ttk.Button(master, text="开始分析", command=self.analyze_clicked, style='TButton')
        self.button_analyze.grid(row=0, column=10, padx=5, pady=10)

        # 在现有控件下方添加一个新的文本框和标签
        self.label_match_rule = tk.Label(master, text="匹配规则", bg='white', fg='black')
        self.label_match_rule.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # 创建一个文本框，假设每行可以显示50个字符，高度设置为能显示6行
        self.text_match_rule = tk.Text(master, width=50, height=6, bg='white', fg='black')
        self.text_match_rule.grid(row=1, column=1, columnspan=10, padx=5, pady=5, sticky="ew")
        default_text = ("第一个文件是求职者简历，第二个excel文件的每一行都是不同技术技能的期望要求，"
                        "请分析求职者简历，并逐条给出各个技能的符合程度分析，最好能逐条给出分值，满分100分。"
                        "请按照以下的语句样式进行分析："
                        "1、高端机械校准件技术-1 (LF~20/26.5GHz, SOTL类型，难度等级4)："
                        "评分：0分分析：求职者简历中未提及机械校准件技术，缺乏直接相关经验。")
        self.text_match_rule.insert(tk.END, default_text)  # 配置第二行的列权重，确保文本框水平扩展
        master.grid_columnconfigure(1, weight=1)

        # 创建一个Style对象
        style = ttk.Style()
        style.theme_use("clam")

        # 尝试通过增加边框来模拟网格线效果
        style.configure("Treeview", bordercolor="black", borderwidth=1)
        style.configure("Treeview.Heading", bordercolor="black", borderwidth=1)

        # 初始化表格，增加四列
        self.tree = ttk.Treeview(master, columns=("序号", "技能要求", "匹配度", "备注"), show='headings',
                                 style='Treeview')
        self.tree.heading("序号", text="序号")
        self.tree.heading("技能要求", text="技能要求")
        self.tree.heading("匹配度", text="匹配度")
        self.tree.heading("备注", text="备注")

        # 调整列宽度
        self.tree.column("序号", width=20, anchor='center')
        self.tree.column("技能要求", width=250, anchor='center')
        self.tree.column("匹配度", width=20, anchor='center')
        self.tree.column("备注", width=800, anchor='center')

        self.tree.grid(row=2, column=0, columnspan=11, padx=10, pady=10, sticky="nsew")

        # 配置行列的权重，确保表格控件能够随窗口调整大小
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(2, weight=1)

        # 绑定事件，用于隔行变色已经不再需要，直接配置tag的背景色
        self.tree.tag_configure('odd', background='#E8E8E8')
        self.tree.tag_configure('even', background='white')

        # 确保表格隔行变色
        self.apply_row_coloring()

    def apply_row_coloring(self):
        for index, row_id in enumerate(self.tree.get_children()):
            tag = 'even' if index % 2 == 0 else 'odd'
            self.tree.item(row_id, tags=(tag,))

    def select_resume(self):
        # 打开文件选择窗口，默认选择PDF文件
        filepath = filedialog.askopenfilename(
            title="选择简历",
            filetypes=[("所有文件", "*.*")],  # 只允许选择PDF文件
            initialdir="/"  # 初始目录为根目录，可根据需要调整
        )
        if filepath:
            self.entry1.delete(0, tk.END)  # 清除文本框中现有的内容
            self.entry1.insert(0, filepath)  # 插入新选择的文件路径

    def select_job_matching(self):
        # 打开文件选择窗口，默认选择XLSX文件
        filepath = filedialog.askopenfilename(
            title="选择岗位匹配表",
            filetypes=[("所有文件", "*.*")],  # 只允许选择XLSX文件
            initialdir="/"  # 初始目录为根目录，可根据需要调整
        )
        if filepath:
            self.entry2.delete(0, tk.END)  # 清除文本框中现有的内容
            self.entry2.insert(0, filepath)  # 插入新选择的文件路径

    def analyze_clicked(self):
        # 获取文本框1和文本框2的内容
        resume_path = self.entry1.get()
        job_description_path = self.entry2.get()
        client = OpenAI(
            api_key="sk-FPO8iAP6oogKpi6K2Bh3PVYosDIUUfXT8nWSNw8oODsEc8Vb",
            base_url="https://api.moonshot.cn/v1",
        )
        print(resume_path)
        print(job_description_path)
        file_object = client.files.create(file=Path(resume_path), purpose="file-extract")

        file_content = client.files.content(file_id=file_object.id).text

        file_object2 = client.files.create(file=Path(job_description_path), purpose="file-extract")

        file_content2 = client.files.content(file_id=file_object2.id).text

        messages = [
            {
                "role": "system",
                "content": file_content2,
            },
            {
                "role": "system",
                "content": file_content,
            },

            {"role": "user", "content": self.text_match_rule.get("1.0", tk.END)},
        ]

        print(messages[2])
        print(self.combobox_model.get())
        # 然后调用 chat-completion, 获取 kimi 的回答
        completion = client.chat.completions.create(
            model=self.combobox_model.get(),
            messages=messages,
            temperature=0.3,
            max_tokens=4096,
            stream=True,
        )

        # 清空表格中的现有内容
        for i in self.tree.get_children():
            self.tree.delete(i)

        # 分行处理completion.choices[0].message.content，并将每行作为一个新条目插入到表格中

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
                    # 插入到表格中
                    self.tree.insert("", tk.END, values=(serial, skill, score, analysis))
                    self.master.update_idletasks()  # 强制更新界面

                collected_messages = []
                # 使用正则表达式匹配所需内容
                pattern = r'(\d+)、(.*?：评分：\d+分)\n分析：(.*?)\n'

        #            chunk_message_content = chunk_message.content.replace('\n', '').replace('\r', '')

        #            print(f"#{idx}: {''.join(collected_messages)}")

        # 查找所有匹配项并插入到表格中
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
        #     # 插入到表格中
        #     self.tree.insert("", tk.END, values=(serial, skill, score, analysis))
        #     self.master.update_idletasks()  # 强制更新界面

    def custom_style(self):
        style = ttk.Style()
        style.theme_use('clam')  # 'clam' theme allows for more customization

        # Configure a dark theme
        style.configure('TFrame', background='#000000')
        style.configure('TButton', background='white', foreground='black', borderwidth=1)
        style.configure('TLabel', background='#000000', foreground='white')
        style.configure('TEntry', background='white', foreground='black', borderwidth=1, padding=5)
        style.configure('TCombobox', background='white', foreground='black', borderwidth=1)
        style.configure('TRadiobutton', background='white', foreground='black', selectcolor='#555')
        style.map('TButton', background=[('active', '#666')], foreground=[('active', 'white')])
        style.map('TEntry', fieldbackground=[('!disabled', 'white')], foreground=[('!disabled', 'black')])
        style.map('TCombobox', fieldbackground=[('!disabled', 'white')], selectbackground=[('!disabled', 'white')],
                  selectforeground=[('!disabled', 'black')])
        style.map('TRadiobutton', background=[('active', '#666')], foreground=[('active', 'white')])

        # Custom configuration for the dialog buttons
        style.configure('Dialog.TButton', background='#89CFF0', foreground='black')
        style.map('Dialog.TButton', background=[('active', '#555')], foreground=[('active', 'white')])


root = tk.Tk()
my_window = ProjectWindow(root)
root.mainloop()

