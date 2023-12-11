
import win32com.client,re

def remove_invalid_characters(text):
    # 删除无效字符
    cleaned_text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')

    return cleaned_text
def replace_str(original_string):
    tstr= original_string.replace(' ', '').replace('\t', '').\
        replace('【', '[').replace('】', ']').replace('\n','').\
        replace('：', ':').replace("（", "(").replace("）", ")").replace('\r\n','').replace('\x1f','')
    new_str = re.sub(r'[\n\r]', ' ',tstr )
    return repr(remove_invalid_characters(new_str))

def insert_revision_at_text(doc_path, target_text, new_text):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False  # 如果你想可见Word应用程序，请设置为True

    doc = word.Documents.Open(doc_path)
    doc.TrackRevisions = True

    for paragraph in doc.Paragraphs:
        # 获取段落文本
        paragraph_text = paragraph.Range.Text.strip()
        # 在文本中查找目标文本
        paragraph_text1 =replace_str(paragraph_text)
        if target_text in paragraph_text1:
            # 在目标文本前插入新文本
            doc.InsertBefore(new_text)
            # 开启修订


    # 关闭Word文档
    doc.Close(SaveChanges=True)

    # 关闭Word应用程序
    word.Quit()

# 使用示例
insert_revision_at_text("Z:\\AI_Json\\source_docx_modify\\a.docx","我司对于所申请的北京世纪互联宽带数据中心有限公司", "NewText")
