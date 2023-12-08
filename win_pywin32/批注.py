from win32com.client import Dispatch
word = Dispatch('Word.Application')
word.Visible = 0
path = r'G:\codes\python\pydev\win_pywin32\a.docx'
doc = word.Documents.Open(FileName=path, Encoding='gbk')
# 主要关键的是这一句
for index,paragraph in enumerate(doc.Paragraphs):
    # 获取段落文本
    paragraph_text = paragraph.Range.Text.strip()
    print(paragraph_text)
    if "煽动颠覆国家政权" in paragraph_text:

        doc.Comments.Add(Range=doc.paragraphs[index+1].Range, Text='测试')