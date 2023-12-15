from win32com.client import Dispatch
word = Dispatch('Word.Application')
word.Visible = 0
path = r'E:\codes\pydev\win_pywin32\diff.docx'
doc = word.Documents.Open(FileName=path, Encoding='gbk')
# 主要关键的是这一句

# first_paragraph = doc.Paragraphs.Item(1)
# doc.Comments.Add(Range=first_paragraph.Range, Text='测试')
# insert
parag = doc.Paragraphs(1)
parag_2 = doc.Paragraphs(70)

parag_range = parag.Range
selected_range = parag_2.Range
print(selected_range.Text) # 选中行文本
selected_range.SetRange(Start=selected_range.Start+10,End=selected_range.End)
print(parag.Range.Text)#第一段整段文字
print(selected_range.Text)#第2段中位置从第10个到最后的字符


# 关闭Word文档
doc.Save()

# 关闭Word应用程序
word.Quit()
