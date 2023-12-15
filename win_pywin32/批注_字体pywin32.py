from win32com.client import Dispatch
word = Dispatch('Word.Application')
word.Visible = 0
path = r'E:\codes\pydev\win_pywin32\diff.docx'
doc = word.Documents.Open(FileName=path, Encoding='gbk')
# 主要关键的是这一句

# first_paragraph = doc.Paragraphs.Item(1)
# doc.Comments.Add(Range=first_paragraph.Range, Text='测试')
# insert
for index,paragraph in enumerate(doc.Paragraphs):
    # 获取段落文本
    # paragraph_text = paragraph.Range.Text.strip()
    # print(paragraph_text)
    if "煽动颠覆国家政权" in paragraph.Range.Text.strip():
        parag_2 = doc.Paragraphs(index)
        comment_text='测12345678试'
        bold_text='1'
        start_bold=comment_text.find(bold_text)
        end_bold=start_bold+len(bold_text)

        comment = doc.Comments.Add(Range=parag_2.Range, Text=comment_text)
        # print(comment.Range.Text)
        select_cr=comment.Range
        select_cr.SetRange(Start=select_cr.Start +start_bold,End=select_cr.Start+end_bold)
        print(select_cr.Text)
        select_cr.Font.Bold = True
# 关闭Word文档
doc.Save()

# 关闭Word应用程序
word.Quit()
