
doc = word_app.Documents.Open(doc_path)
# 打开文档

for index, paragraph in enumerate(doc.Paragraphs):
    # 获取段落的修订信息
    if index == 2:
        current_paragraph = doc.Paragraphs.Item(index )
        doc.Comments.Add(Range=current_paragraph.Range, Text="abc11")

# # 保存文档
# doc.save(r"G:\codes\python\pydev\win_pywin32\output_document.docx")

# 关闭Word文档和应用程序对象
doc.Close(False) ## xxx
word_app.Quit()