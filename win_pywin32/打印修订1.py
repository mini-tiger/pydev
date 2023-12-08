import win32com.client

def print_revisions_before_after(doc):
    # 备份文档
    doc_backup = doc.Range().Duplicate

    # 获取文档中的所有修订
    revisions = doc.Revisions

    # 遍历修订
    for revision in revisions:
        # 获取修订的类型
        revision_type = revision.Type

        # 获取修订的文本范围
        revision_range = revision.Range

        # 保存修订前的文档版本
        doc_backup.Copy()

        # 粘贴修订前的文档版本到新的Range对象
        previous_range = doc.Range()

        # 如果是插入操作
        if revision_type == 1:
            print("Insert:")
            print(f"Author: {revision.Author}")
            print(f"Date: {revision.Date}")
            print(f"Before Content: {previous_range.Text.strip()}")
            print(f"After Content: {revision_range.Text.strip()}")
            print("----")

        # 如果是删除操作
        elif revision_type == 2:
            print("Delete:")
            print(f"Author: {revision.Author}")
            print(f"Date: {revision.Date}")
            print(f"Deleted Content: {revision_range.Text.strip()}")
            print("----")

def main():
    # 替换为你的Word文档路径
    doc_path = r'G:\codes\python\pydev\win_pywin32\a.docx'

    # 创建Word应用程序对象
    word_app = win32com.client.Dispatch('Word.Application')

    # 打开文档
    doc = word_app.Documents.Open(doc_path)

    # 打印文档中的所有修订及修订前后的内容
    print_revisions_before_after(doc)

    # 关闭文档
    doc.Close()

    # 退出Word应用程序
    word_app.Quit()

if __name__ == "__main__":
    main()
