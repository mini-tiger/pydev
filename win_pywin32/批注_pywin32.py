from win32com.client import Dispatch
word = Dispatch('Word.Application')
word.Visible = 0
path = r'G:\codes\python\pydev\win_pywin32\output_document.docx'
doc = word.Documents.Open(FileName=path, Encoding='gbk')
# 主要关键的是这一句

# first_paragraph = doc.Paragraphs.Item(1)
# doc.Comments.Add(Range=first_paragraph.Range, Text='测试')
# insert
for index,paragraph in enumerate(doc.Paragraphs):
    # 获取段落文本
    paragraph_text = paragraph.Range.Text.strip()
    print(paragraph_text)
    if "煽动颠覆国家政权" in paragraph_text:
        current_paragraph = doc.Paragraphs.Item(index+1)
        doc.Comments.Add(Range=current_paragraph.Range, Text='测试')
# 关闭Word文档
doc.Save()

# 关闭Word应用程序
word.Quit()
# read
for paragraph in doc.Paragraphs:
    comments= paragraph.Range.Comments
    for c in comments:
        print(c.Range.Text)