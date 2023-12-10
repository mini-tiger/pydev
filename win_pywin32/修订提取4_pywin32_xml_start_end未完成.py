import win32com.client

# 创建Word应用程序对象
word_app = win32com.client.Dispatch("Word.Application")

# 打开Word文档
doc_path = r"G:\codes\python\pydev\win_pywin32\output_document.docx"
doc = word_app.Documents.Open(doc_path)

# 获取文档的所有段落
paragraphs = doc.Paragraphs

original_string1=""
# 遍历每个段落并提取修订内容
for paragraph in paragraphs:
    # 获取段落的XML
    xml = paragraph.Range.XML
    original_string = paragraph.Range.Text
    if original_string1 == "":
        original_string1 = original_string
    else:
        original_string1 = original_string1 + original_string
    # 获取段落的修订信息
    revisions = paragraph.Range.Revisions
    comments= paragraph.Range.Comments

    print(list(original_string))

    # 如果段落有修订，打印修订信息
    if revisions.Count > 0:
        for revision in revisions:
            print(f"Revision Type: {revision.Type}")
            # print(f"Author: {revision.Author}")
            # print(f"Date: {revision.Date}")
            # print(f"Range XML: {revision.Range.XML}")
            # print(f"Content: {paragraph.Range.Text.strip()}")
            # print(revision.Range.Start,revision.Range.End)
            start = revision.Range.Start
            end = revision.Range.End
            print(start,end)
            if revision.Type==1: # ins
                original_string1 = original_string1[:start] + original_string1[end:]
            # if revision.Type==2:
            #     original_string = original_string[:start] + original_string[end:]
        print(original_string1)
        print("\n---\n")

    # else:
    #     print(f"Paragraph without revisions:\n{xml}")

    for c in comments:
        print(c.Range.Text)

# 关闭Word文档和应用程序对象
doc.Close()
word_app.Quit()
