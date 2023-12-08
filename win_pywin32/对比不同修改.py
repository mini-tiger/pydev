import copy
import time

import win32com.client
import win32com.client as win32



def track_doc(path_file_name,stat=False):
    word = win32.gencache.EnsureDispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(path_file_name)
        doc.Activate()
        word.ActiveDocument.TrackRevisions = True  #关闭默认修订模式 Maybe not need this (not really but why not)

        # Accept all revisions
        if stat:
            # Accept all revisions
            word.ActiveDocument.Revisions.AcceptAll()
        else:
            word.ActiveDocument.Revisions.RejectAll()
        # Delete all comments
        if word.ActiveDocument.Comments.Count >= 1:
            word.ActiveDocument.DeleteAllComments()

        word.ActiveDocument.Save()
        doc.Close(False)
    except Exception as e:
        print(111,e)
    finally:
        word.Application.Quit()

def add_comment_at_range(range, comment_text):
    # Add a comment to the specified range in the document
    range.Comments.Add(range, Text=comment_text)


def compare_and_track_changes(doc_path1, doc_path2, output_path):
    # Create the Application word
    word = win32.gencache.EnsureDispatch("Word.Application")
    # word.Visible = False

    try:

        # Compare documents
        word.CompareDocuments(word.Documents.Open(doc_path1),
                                     word.Documents.Open(doc_path2),CompareWhitespace=False,IgnoreAllComparisonWarnings=True)

        word.ActiveDocument.ActiveWindow.View.Type = 3
        #
        for revision in word.ActiveDocument.Revisions:
            if revision.Type == 2:  # Type 2 corresponds to wdRevisionInsert
                add_comment_at_range(revision.Range, "Inserted: " + revision.Range.Text)
            if revision.Type == 3:  # Type 3 corresponds to wdRevisionDelete
                add_comment_at_range(revision.Range, "Deleted: " + revision.Range.Text)


        # Save the comparison document as "Comparison.docx"
        word.ActiveDocument.SaveAs(FileName=output_path)

    # Don't forget to quit your Application
    except Exception as e:
        print(2222,e)
    finally:

        word.Application.Quit()




#

if __name__ == "__main__":

    # 示例用法
    document1_path = "e:\\source_docx\\unlock_undyx_unstatic_带宽罚则 非锁定版(非标准合同)_IDC主协议_北京世纪互联宽带数据中心托管服务协议(2023年版)-（非预留机柜）.docx"
    document2_path = "e:\\source_docx_modify\\蓝芯算力&世纪互联主合同-JH cmts-Vlegal1109_modify.docx"

    # track_doc(document1_path)
    # time.sleep(1)
    # track_doc(document2_path)
    output_document_path = "e:\\source_docx_modify\\output_document.docx"
    time.sleep(1)

    compare_and_track_changes(document1_path, document2_path, output_document_path)
