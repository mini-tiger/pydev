import os,re
from win32com.client import Dispatch
def replace_str(original_string):
    tstr= original_string.replace(' ', '').replace('\t', '').\
        replace('【', '[').replace('】', ']').replace('\n','').replace('\r','').\
        replace('：', ':').replace("（", "(").replace("）", ")").replace('\r\n','')


    new_str1=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]',"", tstr)
    new_str = re.sub(r'[\n\r]', ' ',new_str1 )
    return new_str
def convert_word_to_txt(word_file, txt_file):
    # Create a new Word application
    word_app = Dispatch('Word.Application')

    # Open the Word document
    doc = word_app.Documents.Open(word_file)

    # Extract text from the document
    text_content = doc.Content.Text

    # Close the Word document
    doc.Close()

    # Quit the Word application
    word_app.Quit()

    # Write the extracted text to a text file
    with open(txt_file, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text_content)

def convert_word_to_txt1(word_file, txt_file):
    # Create a new Word application
    word_app = Dispatch('Word.Application')

    # Open the Word document
    doc = word_app.Documents.Open(word_file)

    # Extract text from the document
    # Extract text from the document
    # text_content = doc.Content.Text
    paragraphs = doc.Paragraphs
    with open(txt_file, 'w', encoding='utf-8') as txt_file:
        for paragraph in paragraphs:
            text = paragraph.Range.Text
            # print(f"当前文本:{replace_str(text)}")

            txt_file.write(replace_str(text))
            txt_file.write('\n')


    # Close the Word document
    doc.Close()

    # Quit the Word application
    word_app.Quit()



if __name__ == "__main__":
    # Replace 'your_word_file.docx' with the path to your Word document
    word_file_path = r'G:\codes\python\pydev\win_pywin32\unlock_unstd_unstatic_带宽罚则 非锁定版(非标准合同)_IDC主协议_北京世纪互联宽带数据中心托管服务协议(2023年版)-（非预留机柜）.docx'

    # Replace 'output.txt' with the desired name for the output text file
    txt_file_path = 'output.txt'
    txt_file_path1 = 'output1.txt'
    convert_word_to_txt(word_file_path, txt_file_path)
    convert_word_to_txt1(word_file_path, txt_file_path1)