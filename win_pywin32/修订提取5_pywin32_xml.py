import win32com.client
import copy,os

# 创建Word应用程序对象
word_app = win32com.client.Dispatch("Word.Application")

# 打开Word文档
current_directory = os.path.dirname(__file__)
doc_path = os.path.join(current_directory,  "output_document.docx")
doc = word_app.Documents.Open(doc_path)

# 获取文档的所有段落
paragraphs = doc.Paragraphs

original_string1 = ""
# 遍历每个段落并提取修订内容
for paragraph in paragraphs:
    # 获取章节序号
    section_number = paragraph.Range.ListFormat.ListString
    start_page_number =  paragraph.Range.Information(win32com.client.constants.wdActiveEndPageNumber)
    print(f"当前文本:{paragraph.Range.Text}")
    print(f"当前段落序号:{section_number}")
    print(f"当前页码:{start_page_number}")
    # 获取段落的修订信息
    revisions = paragraph.Range.Revisions

    # 如果段落有修订，打印修订前后的信息
    if revisions.Count > 0:
        original_string = paragraph.Range.Text
        source_line = copy.deepcopy(original_string)
        for revision in revisions:
            text = revision.Range.Text
            # print(paragraph.Range.Start,paragraph.Range.End)
            # print(revision.Range.Start,revision.Range.End)
            start = revision.Range.Start-paragraph.Range.Start
            end =  start+(revision.Range.End-revision.Range.Start)
            # print(start, end, revision.Type)

            if revision.Type == 2:  # Check if the revision is rejected (Type 2 represents a deleted revision)
                # Extract and print the text of the rejected revision
                # print(text)
                source_line  = source_line.replace(text, "")
                # source_line = copy.deepcopy(original_string)
                # new_string = new_line[:start] + text + new_line[end:]
                # print("修订前1: %s" % source_line)
                # print(f'修订后1: {new_line}')
                # 在指定位置插入字符串

            if revision.Type == 1:
                # source_line = copy.deepcopy(original_string).replace(text, "")
                # new_line = copy.deepcopy(original_string)
                # print(f"修订前2: {source_line}")
                # print(list(source_line))
                original_string = original_string[:start]  + original_string[end:]
                # print(f"修订后2: {new_line}")
                # print("\n---\n")

        print("修订前1: %s" % original_string)
        print(f'修订后1: {source_line}')
    # else:
    #     print(f"Paragraph without revisions:\n{xml}")

# 关闭Word文档和应用程序对象
doc.Close()
word_app.Quit()
