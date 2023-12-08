import win32com.client
from win32com.client import Dispatch

def add_revision( doc, text_to_insert):
    # Create a new Word application
    word_app = Dispatch('Word.Application')

    # Access the ActiveDocument
    word_doc = word_app.Documents.Open(doc)

    # Enable tracking changes
    word_app.ActiveDocument.TrackRevisions = True
    # 将文本插入到文档中
    selection = word_app.Selection
    # print(dir(selection))
    selection.TypeText(text_to_insert)
    # Insert the text with revision

    # word_app.ActiveDocument.Range().InsertBefore(text_to_insert)

    # Save the changes
    word_doc.Save()

    # Close the document
    word_doc.Close()



# Specify the document path
doc_path = r"G:\codes\python\pydev\win_pywin32\a.docx"

# Open the Word documen

# Call the function to add a revision
revision_text = "不得利用世纪互联提供的互联网接入服务或相关业务平台从事"
add_revision( doc_path, revision_text)


