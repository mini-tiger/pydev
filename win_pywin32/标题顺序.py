import json
import win32com.client

def convert_word_to_json(file_path):
    word_app = win32com.client.Dispatch("Word.Application")
    word_app.Visible = False  # 隐藏Word应用程序界面

    doc = word_app.Documents.Open(file_path)

    # 初始化JSON结构
    document_json = {
        "title": doc.Name,
        "content": []
    }

    current_heading = None
    current_paragraphs = []

    # 遍历文档段落
    for paragraph in doc.Paragraphs:
        if paragraph.Style and paragraph.Style.NameLocal.startswith("Heading"):
            # 如果当前存在标题，则保存上一个标题的信息
            if current_heading:
                current_heading["content"] = "\n".join(current_paragraphs)
                document_json["content"].append(current_heading)

            # 创建新的标题
            current_heading = {
                "level": int(paragraph.Style.Name.split()[-1]),
                "text": paragraph.Range.Text.strip(),
                "content": ""
            }

            # 重置段落列表
            current_paragraphs = []
        else:
            # 将段落文本添加到当前段落列表
            current_paragraphs.append(paragraph.Range.Text.strip())

    # 处理最后一个标题
    if current_heading:
        current_heading["content"] = "\n".join(current_paragraphs)
        document_json["content"].append(current_heading)

    # 关闭Word应用程序
    word_app.Quit()

    return document_json

def save_json(json_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)

# 示例用法
word_file_path = 'e:\\source_docx_modify\\a.docx'
output_json_file = 'output.json'

document_json = convert_word_to_json(word_file_path)
save_json(document_json, output_json_file)
