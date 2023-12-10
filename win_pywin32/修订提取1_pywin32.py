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
        print(f"Author: {revision.Author}")
        print(f"Date: {revision.Date}")
        print(f"Content: {paragraph_range.Text.strip()}")
        print("----")

def main():
    # 替换为你的Word文档路径
    doc_path = r'G:\codes\python\pydev\win_pywin32\output_document.docx'

    # 创建Word应用程序对象
    word_app = win32com.client.Dispatch('Word.Application')

    # 打开文档
    doc = word_app.Documents.Open(doc_path)

    # 打印文档中的所有修订及所在行的内容
    print_revisions_with_line(doc)

    # 关闭文档
    doc.Close()

    # 退出Word应用程序
    word_app.Quit()

if __name__ == "__main__":
    main()
