from docx import Document

def add_comment(paragraph, author, text):
    comment = paragraph.add_comment(text, author=author)
    return comment

# 替换为你的Word文档路径
doc_path = r"G:\codes\python\pydev\win_pywin32\output_document.docx"

# 打开文档
doc = Document(doc_path)

# 替换为你要增加批注的段落
target_paragraph_index = 10
target_paragraph = doc.paragraphs[target_paragraph_index]

# 增加批注
new_comment = add_comment(target_paragraph, author="YourName", text="This is a new comment.")

# 保存文档
doc.save(r"G:\codes\python\pydev\win_pywin32\output_document.docx")
