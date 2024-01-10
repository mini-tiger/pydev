import win32com.client

def add_comment_to_word_document(file_path, comment_text, range_start, range_end):
    # 创建 Word 应用程序的 COM 对象
    word_app = win32com.client.Dispatch("Word.Application")

    # 设置为可见，以便查看 Word 操作的过程
    word_app.Visible = True

    # 打开 Word 文档
    doc = word_app.Documents.Open(file_path)

    paragraphs = doc.Paragraphs

    first_start = 0
    first_end = 0
    second_start = 0
    second_end = 0
    # 遍历每个段落并提取修订内容
    for paragraph in paragraphs:
        print(paragraph.Range.Start,paragraph.Range.End,paragraph.Range.Text)
        if "煽动颠覆国家政权" in paragraph.Range.Text:
            first_start = paragraph.Range.Start
        if "宣扬恐怖主义" in paragraph.Range.Text:
            first_end = paragraph.Range.End
        if "传播虚假信息扰乱经济秩序和社会秩序的" in paragraph.Range.Text:
            second_start = paragraph.Range.Start
        if "进入计算机信息网络或者使用计算机信息网络资源的" in paragraph.Range.Text:
            second_end = paragraph.Range.End

    # 获取文档的指定范围
    # range_to_comment = doc.Range(doc.Range().Start + range_start, doc.Range().Start + range_end)
    range_to_comment1 = doc.Range(doc.Range().Start + first_start, doc.Range().Start + first_end)
    # 在指定范围添加批注
    comment = range_to_comment1.Comments.Add(range_to_comment1, "first")

    range_to_comment2 = doc.Range(doc.Range().Start + second_start, doc.Range().Start + second_end)
    comment = range_to_comment2.Comments.Add(range_to_comment2, "second")
    # 关闭文档时保存更改
    doc.Save()
    doc.Close()

    # 退出 Word 应用程序
    word_app.Quit()


if __name__ == "__main__":
    # 替换为你的 Word 文档路径
    word_file_path = r'E:\codes\pydev\win_pywin32\diff.docx'

    # 替换为你的批注文本
    comment_text = "这是一个批注示例。"

    # 替换为你的范围开始和结束位置
    range_start = 10
    range_end = 20

    add_comment_to_word_document(word_file_path, comment_text, range_start, range_end)
