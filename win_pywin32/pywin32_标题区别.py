import win32com.client

def read_and_merge_headings(file_path, start_level=1):
    # 创建 Word 应用程序的 COM 对象
    word_app = win32com.client.Dispatch("Word.Application")

    # 设置为不可见，防止弹出 Word 应用程序窗口
    word_app.Visible = False

    # 打开 Word 文档
    doc = word_app.Documents.Open(file_path)

    # 用于存储章节序号及其子序号的关系
    section_hierarchy = {}

    # 遍历文档中的段落
    for paragraph in doc.Paragraphs:
        list_string = paragraph.Range.ListFormat.ListString

        # 判断是否为第一级标题（格式为 x，如 1，2，3）
        if '.' not in list_string:
            section_hierarchy[start_level] = list_string
            parent_level = start_level
        else:
            # 获取当前段落的标题级别
            heading_level = list_string.count('.') + start_level

            # 获取上一级标题的序号
            parent_level = heading_level - 1
            parent_list_string = section_hierarchy.get(parent_level, "")

            # 合并章节序号和子序号
            combined_list_string = f"{parent_list_string}.{list_string.split('.')[-1]}"

            # 存储当前标题级别的序号
            section_hierarchy[heading_level] = combined_list_string

        # 输出合并后的序号和文本内容
        print(f"{section_hierarchy[parent_level]} {paragraph.Range.Text}")

    # 关闭文档和 Word 应用程序
    doc.Close()
    word_app.Quit()

if __name__ == "__main__":
    import os
    # 替换为你的 Word 文档路径
    current_directory = os.path.dirname(__file__)
    doc_path = os.path.join(current_directory, "diff.docx")

    # 替换为你想要的起始标题等级
    start_heading_level = 1

    read_and_merge_headings(doc_path, start_heading_level)
