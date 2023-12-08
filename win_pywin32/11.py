import os
from win32com.client import Dispatch

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

if __name__ == "__main__":
    # Replace 'your_word_file.docx' with the path to your Word document
    word_file_path = 'Z:\\AI_Json\\source_docx\\unlock_sjhl_unreserved_非锁定版(非标准合同)_IDC主协议_北京世纪互联宽带数据中心托管服务协议(2023年版)-（非预留机柜）.docx'

    # Replace 'output.txt' with the desired name for the output text file
    txt_file_path = 'output.txt'

    convert_word_to_txt(word_file_path, txt_file_path)
