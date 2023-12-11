import win32com.client
import difflib

def read_word_document(file_path):
    word_app = win32com.client.Dispatch("Word.Application")
    word_app.Visible = False  # 隐藏Word应用程序界面

    doc = word_app.Documents.Open(file_path)

    paragraphs = [paragraph.Range.Text.strip() for paragraph in doc.Paragraphs]

    # 关闭Word应用程序
    word_app.Quit()

    return paragraphs

def compare_documents(doc1, doc2):
    differ = difflib.Differ()
    diff = list(differ.compare(doc1, doc2))
    return '\n'.join(diff)

def save_diff_to_file(diff_result, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(diff_result)

# 示例用法
document1_path = "e:\\source_docx\\unlock_undyx_unstatic_带宽罚则 非锁定版(非标准合同)_IDC主协议_北京世纪互联宽带数据中心托管服务协议(2023年版)-（非预留机柜）.docx"
document2_path = "e:\\source_docx_modify\\a.docx"
output_diff_file = 'output_diff.txt'

doc1_content = read_word_document(document1_path)
print(doc1_content)
doc2_content = read_word_document(document2_path)

diff_result = compare_documents(doc1_content, doc2_content)

save_diff_to_file(diff_result, output_diff_file)
