import win32com.client
import copy,os,re
def replace_str(original_string):
    tstr= original_string.replace(' ', '').replace('\t', '').\
        replace('【', '[').replace('】', ']').replace('\n','').replace('\r','').\
        replace('：', ':').replace("（", "(").replace("）", ")").replace('\r\n','')


    new_str1=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]',"", tstr)
    new_str = re.sub(r'[\n\r]', ' ',new_str1 )
    return new_str
# 创建Word应用程序对象
word_app = win32com.client.Dispatch("Word.Application")

# 打开Word文档
current_directory = os.path.dirname(__file__)
doc_path = os.path.join(current_directory,  "diff.docx")
doc_path = r"E:\codes\pydev\neolink-dataset\contract-sentinel\diff_docx\diff.docx"
doc = word_app.Documents.Open(doc_path)

# 获取文档的所有段落
paragraphs = doc.Paragraphs
# 遍历每个段落并显示内容，包括表格
# 遍历每个段落并显示内容，包括表格
run_table=True
for paragraph in paragraphs:
    # 判断段落是否为表格
    if paragraph.Range.Tables.Count > 0 and run_table:
        run_table=False
        # 如果是表格，遍历表格并显示内容
        for table in paragraph.Range.Tables:
            for row_index in range(1, table.Rows.Count+1 ):
                row = table.Rows(row_index)
                row_content = []
                if row_index < 5:
                    for col_index in range(1, table.Columns.Count + 1):
                        cell = row.Cells(col_index)

                        # 获取单元格文本内容
                        cell_text = cell.Range.Text.strip()

                        row_content.append(replace_str(cell_text))
                        # print(row_index,col_index,cell.Range.Cells.Count)
                else:
                    # 获取合并单元格的信息
                    # 检查单元格是否为合并单元格
                    cell = row.Cells(1)
                    merged_cell_text = cell.Range.Text.strip()
                    row_content.append(replace_str(merged_cell_text))
                    cell = row.Cells(2)
                    merged_cell_text = cell.Range.Text.strip()
                    row_content.append(replace_str(merged_cell_text))

                # 将单元格内容用 "|" 分割显示
                row_str = " | ".join(row_content)



source_dict={}
# 遍历每个段落并提取修订内容
for paragraph in paragraphs:
    # # 获取章节序号
    # section_number = paragraph.Range.ListFormat.ListString
    # start_page_number =  paragraph.Range.Information(win32com.client.constants.wdActiveEndPageNumber)
    # # 获取段落的样式
    # paragraph_style = paragraph.Range.ParagraphFormat.Style.NameLocal
    # text=copy.deepcopy(paragraph.Range.Text)
    # print(f"当前文本:{replace_str(text)}")
    # print(f"当前段落序号:{section_number}")
    # print(f"当前页码:{start_page_number}")
    # source_dict[replace_str(text)]={"page":replace_str(f"{start_page_number}"),"part":replace_str(section_number)}
    # print(f"段落样式:{paragraph_style}")
    # print(paragraph.Range.Tables.Count)
    # if start_page_number == 8:
    #     print(f"88888 {paragraph.Range.Tables.Count}")
    #     print(paragraph)
    # 获取段落的修订信息
    revisions = paragraph.Range.Revisions
    original_string = paragraph.Range.Text

    source_line = copy.deepcopy(original_string)
    # 如果段落有修订，打印修订前后的信息
    if revisions.Count > 0:
        # print(dir(revisions))
        print("bcd",original_string)
        revisions.AcceptAll()
        print("abc",paragraph.Range.Text)
        revisions.RejectAll()
        print("ccc",paragraph.Range.Text)
        for revision in revisions:
            # print(dir(revision))
            text = revision.Range.Text
            # print(paragraph.Range.Start,paragraph.Range.End)
            # print(revision.Range.Start,revision.Range.End)
            start = revision.Range.Start-paragraph.Range.Start
            end =  start+(revision.Range.End-revision.Range.Start)
            print(start, end, revision.Type)
            print(source_line)
            abc=copy.deepcopy(source_line)
            print(text)
            print(abc[start:end])
            if revision.Type == 2:  # Check if the revision is rejected (Type 2 represents a deleted revision)
                # Extract and print the text of the rejected revision
                # print(text)
                source_line  = source_line.replace(text, "")
                # source_line = copy.deepcopy(original_string)
                # new_string = new_line[:start] + text + new_line[end:]
                # print("修订前1: %s" % source_line)
                # print(f'修订后1: {new_line}')
                # 在指定位置插入字符串
                # original_str[:index] + insert_str + original_str[index:]

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
# for key,value in source_dict.items():
#     print(key,value)
