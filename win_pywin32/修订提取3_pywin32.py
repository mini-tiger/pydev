import win32com.client

def has_revisions(para):
    # 检查段落的修订集合是否为空
    return para.Range.Revisions.Count > 0

def check_revisions_in_document(doc):
    # 获取文档中的所有段落
    paragraphs = doc.Paragraphs

    # 遍历每个段落
    for para in paragraphs:
        if has_revisions(para):
            revisions = para.Range.Revisions
            revisions.AcceptAll()
            print(f"Paragraph with revisions found: {para.Range.Text.strip()}")
            # 这里可以添加具体的处理逻辑

def main():
    # 替换为你的Word文档路径
    doc_path = r'E:\codes\pydev\neolink-dataset\contract-sentinel\diff_docx\diff.docx'

    # 创建Word应用程序对象
    word_app = win32com.client.Dispatch('Word.Application')

    # 打开文档
    doc = word_app.Documents.Open(doc_path)
    doc.Activate()
    # 检查文档中的所有段落是否有修订
    check_revisions_in_document(doc)

    # 关闭文档
    doc.Close(False)

    # 退出Word应用程序
    word_app.Quit()

if __name__ == "__main__":
    main()
