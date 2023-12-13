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

def func2():
    # 创建Word应用程序对象
    word_app = win32com.client.Dispatch("Word.Application")

    # 打开Word文档
    current_directory = os.path.dirname(__file__)
    doc_path = os.path.join(current_directory, "diff.docx")
    doc_path = r"G:\codes\python\neolink-dataset\contract-sentinel\diff_docx\diff.docx"
    doc = word_app.Documents.Open(doc_path)
    # 打开文档
    # 获取文档的所有段落
    paragraphs = doc.Paragraphs
    for paragraph in paragraphs:
        revisions = paragraph.Range.Revisions

        # 如果段落有修订，打印修订前后的信息
        if revisions.Count > 0:
            original_string = copy.deepcopy(paragraph.Range.Text)
            for revision in revisions:
                if revision.Type == 1:
                    text = revision.Range.Text
                    print(text)
                    original_string = original_string.replace(text, "")
            revisions.AcceptAll()
            print(f"修订前:{original_string}")
            print(f"修订后:{paragraph.Range.Text}")
    doc.Close(False)  # xxx 不保存
    word_app.Quit()

def func1():
    # 创建Word应用程序对象
    word_app = win32com.client.Dispatch("Word.Application")

    # 打开Word文档
    current_directory = os.path.dirname(__file__)
    doc_path = os.path.join(current_directory, "diff.docx")
    doc_path = r"G:\codes\python\neolink-dataset\contract-sentinel\diff_docx\diff.docx"
    doc = word_app.Documents.Open(doc_path)
    # 打开文档
    # 获取文档的所有段落
    paragraphs = doc.Paragraphs

    source_dict = {}
    # 遍历每个段落并提取修订内容
    for paragraph in paragraphs:

        # 获取段落的修订信息
        revisions = paragraph.Range.Revisions
        original_string = paragraph.Range.Text

        source_line = copy.deepcopy(original_string)
        # 如果段落有修订，打印修订前后的信息
        if revisions.Count > 0:

            for revision in revisions:
                # print(dir(revision))

                # print(paragraph.Range.Start,paragraph.Range.End)
                # print(revision.Range.Start,revision.Range.End)
                start = revision.Range.Start-paragraph.Range.Start
                end =  start+(revision.Range.End-revision.Range.Start)
                # start = revision.Range.Start
                # end = revision.Range.End
                print(original_string)
                print(start, end, revision.Range.Start,revision.Range.End)
                print(revision.Type, revision.Range.Text)
                # abc = copy.deepcopy(source_line)
                # print(text)
                # print(abc[start:end])
                if revision.Type == 2:  # Check if the revision is rejected (Type 2 represents a deleted revision)
                    # Extract and print the text of the rejected revision

                    original_string = original_string[:start] + original_string[end:]
                # if revision.Type == 1:
                #     text = revision.Range.Text
                #     original_string = original_string[:start] + text + original_string[end:]

            print("修订前1: %s" % original_string)
            print(f'修订后1: {source_line}')
        # else:
        #     print(f"Paragraph without revisions:\n{xml}")

    # 关闭Word文档和应用程序对象
    doc.Close(False)  # xxx 不保存
    word_app.Quit()
if __name__ == "__main__":
    #方法1  有bug
    func1()

    # func2() #修订后 准