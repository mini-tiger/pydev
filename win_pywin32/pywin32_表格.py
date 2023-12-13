import sys

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
doc_path = r"G:\codes\python\neolink-dataset\contract-sentinel\diff_docx\diff1.docx"
doc = word_app.Documents.Open(doc_path)
# 打开文档

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


# 关闭Word文档和应用程序对象
doc.Close()
word_app.Quit()
# for key,value in source_dict.items():
#     print(key,value)
