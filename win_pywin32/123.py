import win32com.client as win32

def read_revisions_from_word_document(doc_path):
    # Create the Application word
    word = win32.gencache.EnsureDispatch("Word.Application")
    word.Visible = False

    try:
        # Open the document
        doc = word.Documents.Open(doc_path)

        # Access the Revisions collection
        revisions = doc.Revisions

        # Iterate through the revisions and print details
        for revision in revisions:
            # revision_attributes = dir(revision)
            #
            # # Print the list of methods and properties
            # for attribute in revision_attributes:
            #     print(attribute)
            print(f"Type: {revision.Type}")
            print(f"Author: {revision.Author}")
            print(f"Date: {revision.Date}")
            # Collapse the range to the start of the revision
            revision_range = revision.Range
            revision_range.Collapse(0)  # 0 corresponds to wdCollapseStart

            # Duplicate the range to create a copy
            original_range = revision_range.Duplicate

            # Move the duplicated range to the previous story range
            original_range.MoveStart()

            # Get the text before the revision
            original_text = original_range.Text
            print(f"Original Text before Revision: {original_text}")

            # Print modified text after the revision
            modified_text = revision.Range.Text
            print(f"Modified Text after Revision: {modified_text}")

            print("---------------")
        doc.Close()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the document and quit Word application

        word.Application.Quit()

# Example usage
document_path = "e:\\source_docx_modify\\output_document.docx"
read_revisions_from_word_document(document_path)
