import win32com.client
import re

def extract_table_contents(file_path):
    # 连接到 Word 应用程序
    word_app = win32com.client.Dispatch("Word.Application")
    word_app.Visible = False  # 设置 Word 应用程序不可见

    # 打开 Word 文档
    doc = word_app.Documents.Open(file_path)


    # 获取文档中的所有小节
    sections = doc.Paragraphs

    # 将小节名称及其对应的表格内容存储在字典中
    section_table_contents = {}
    current_section = None
    for paragraph in sections:
        # 获取小节名称
        section_name = paragraph.Range.Text.strip()
        print(section_name)
        print(paragraph.Range.Tables.Count)
    # 获取文档中的所有表格
    tables = doc.Tables

    # 提取表格内容
    all_table_contents = []
    for table in tables:
        # 将表格中每行的内容存储为一个独立的列表
        table_contents = []
        for row in table.Rows:
            row_content = [cell.Range.Text.strip() for cell in row.Cells]
            # 清除每个单元格中的换行符、空格和其他特殊字符
            row_content = [re.sub(r'\s+', ' ', cell) for cell in row_content]
            row_content = [re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\xff]', '', cell) for cell in row_content]
            table_contents.append(row_content)
        all_table_contents.append(table_contents)

    # 关闭 Word 文档
    doc.Close()

    # 退出 Word 应用程序
    word_app.Quit()

    return all_table_contents

# 测试示例
file_path = r"D:\codes\neolink-dataset\contract-sentinel-web\source_docx\硬件采购合同.docx"
table_contents = extract_table_contents(file_path)
for table in table_contents:
    print(table)
