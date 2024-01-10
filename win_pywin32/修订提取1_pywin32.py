import win32com.client

def print_revisions_with_line(doc):
    # 获取文档中的所有修订
    revisions = doc.Revisions

    # 遍历修订
    for revision in revisions:
        # 获取修订的文本范围
        revision_range = revision.Range

        # 获取修订所在的段落范围
        paragraph_range = revision_range.Paragraphs(1).Range

        # 打印修订所在行的内容
        # print(f"Author: {revision.Author}")
        # print(f"Date: {revision.Date}")
        print(f"Content: {paragraph_range.Text.strip()}")
        print("----")

def print_revisions_with_line1(doc):
    for index, paragraph in enumerate(doc.Paragraphs):
        revisions = paragraph.Range.Revisions
        if revisions.Count > 0:
            revisions.AcceptAll()
            print(paragraph.Range.Text)




# 替换为你的Word文档路径
doc_path = r'E:\codes\pydev\neolink-dataset\contract-sentinel\diff_docx\diff.docx'

# 创建Word应用程序对象
word_app = win32com.client.Dispatch('Word.Application')

# 打开文档
doc = word_app.Documents.Open(doc_path)

# 打印文档中的所有修订及所在行的内容
print_revisions_with_line1(doc)

# 关闭文档
doc.Close(False)

# 退出Word应用程序
word_app.Quit()

