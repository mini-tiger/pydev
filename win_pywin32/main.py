import win32com.client
from win32com.client import Dispatch

def add_revision( doc, text_to_insert):
    # Create a new Word application
    word_app = Dispatch('Word.Application')
    # Access the ActiveDocument
    word_doc = word_app.Documents.Open(doc)

    # Enable tracking changes
    word_app.ActiveDocument.TrackRevisions = True

    # Insert the text with revision
    word_app.ActiveDocument.Range().InsertBefore(text_to_insert)

    # Save the changes
    word_doc.Save()

    # Close the document
    word_doc.Close()



# Specify the document path
doc_path = r"Z:\\AI_Json\\source_docx_modify\\a.docx"

# Open the Word documen

# Call the function to add a revision
revision_text = "This is a new revision."
add_revision( doc_path, revision_text)


