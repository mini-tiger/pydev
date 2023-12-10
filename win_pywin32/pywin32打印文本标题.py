import win32com.client

def read_word_document(file_path):
    word_app = win32com.client.Dispatch("Word.Application")
    word_app.Visible = False  # 可以设置为True，以显示Word应用程序

    doc = word_app.Documents.Open(file_path)

    content_lines = []

    for paragraph in doc.Paragraphs:
        # 获取章节序号
        section_number = paragraph.Range.ListFormat.ListString

        # 获取段落文本
        paragraph_text = paragraph.Range.Text.strip()

        # 将章节序号和文本合并
        if section_number:
            combined_text = f"{section_number} {paragraph_text}"
        else:
            combined_text = paragraph_text

        # 将合并后的文本添加到列表
        content_lines.append(combined_text)

    # 关闭Word文档
    doc.Close()

    # 关闭Word应用程序
    word_app.Quit()

    return content_lines

# 使用示例
file_path = r"G:\codes\python\pydev\win_pywin32\output_document.docx"
content_lines = read_word_document(file_path)

# 输出每一行的内容
for line in content_lines:
    print(line)


# 使
