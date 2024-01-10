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
doc_path = r'E:\codes\pydev\neolink-dataset\contract-sentinel\diff_docx\diff.docx'
# doc_path = r"G:\codes\python\neolink-dataset\contract-sentinel\diff_docx\diff1.docx"
doc = word_app.Documents.Open(doc_path)
# 打开文档
# 获取文档的所有段落
paragraphs = doc.Paragraphs



source_dict={}
# 遍历每个段落并提取修订内容
for paragraph in paragraphs:
    heading_level = paragraph.Style.ParagraphFormat.OutlineLevel

    listformat=paragraph.Range.ListFormat
    # # 获取章节序号
    section_number = paragraph.Range.ListFormat.ListString
    start_page_number =  paragraph.Range.Information(win32com.client.constants.wdActiveEndPageNumber)
    # # 获取段落的样式
    paragraph_style = paragraph.Range.ParagraphFormat.Style.NameLocal
    text=copy.deepcopy(paragraph.Range.Text)
    if "适用情形" in text:
        print(paragraph)
    print(f"===========================================")
    print(f"Heading Level {heading_level}")
    print(f"当前段落级别:{listformat.ListLevelNumber}")
    print(listformat.ListValue,listformat.ListString,listformat.ListType)
    print(f"当前文本:{replace_str(text)}")
    print(f"当前段落序号:{section_number}")
    print(f"当前页码:{start_page_number}")
    source_dict[replace_str(text)]={"page":replace_str(f"{start_page_number}"),"part":replace_str(section_number)}
    print(f"段落样式:{paragraph_style}")
    # print(paragraph.Range.Tables.Count)
    # if start_page_number == 8:
    #     print(f"88888 {paragraph.Range.Tables.Count}")
    #     print(paragraph)
    # 获取段落的修订信息
    # revisions = paragraph.Range.Revisions

    # else:
    #     print(f"Paragraph without revisions:\n{xml}")

# 关闭Word文档和应用程序对象
doc.Close(False) # xxx 不保存
word_app.Quit()
# for key,value in source_dict.items():
#     print(key,value)
