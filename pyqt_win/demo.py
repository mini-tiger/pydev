import tkinter as tk
from tkinter import ttk

class ProjectWindow:
    def __init__(self, master):
        self.master = master
        master.title("简历分析工具")

        # 应用自定义样式
        self.custom_style()

        # 使窗口最大化 只能在windows
        # master.state('zoomed')

        self.analysis_type = tk.IntVar()
        self.analysis_type.set(1)

        self.radio1 = ttk.Radiobutton(master, text="逐条分析", variable=self.analysis_type, value=1,
                                      style='TRadiobutton', command=self.radio_selected)
        self.radio1.grid(row=0, column=0, padx=(5, 2), pady=10, sticky="w")

        self.radio2 = ttk.Radiobutton(master, text="整体分析", variable=self.analysis_type, value=2,
                                      style='TRadiobutton', command=self.radio_selected)
        self.radio2.grid(row=0, column=1, padx=(5, 2), pady=10, sticky="w")

    def custom_style(self):
        style = ttk.Style()
        style.configure('TRadiobutton', font=('Arial', 12))

    def radio_selected(self):
        print(f"Selected analysis type: {self.analysis_type.get()}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectWindow(root)
    root.mainloop()
