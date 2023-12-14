from imessagefilter import CMessageFilter
import win32com.client as win32
import time, os


def close_word_window():
    os.system("taskkill /F /IM WINWORD.EXE")

class WordParse():
    def __init__(self):
        self.word=self.word_app_dispatch()

    def message_filter_register(self):
        CMessageFilter.register()

    def message_filter_revoke(self):
        CMessageFilter.revoke()


    def word_app_dispatch(self):
        self.word = win32.gencache.EnsureDispatch("Word.Application")
        self.word.Visible = False
        return self.word

    def word_app_quit(self):
        self.word.Application.Quit()

    def track_doc(self,path_file_name, stat=False):
        self.message_filter_register()
        try:
            doc = self.word.Documents.Open(path_file_name)
            doc.Activate()
            self.word.ActiveDocument.TrackRevisions = True  # 关闭默认修订模式 Maybe not need this (not really but why not)

            # Accept all revisions
            if stat:
                self.word.ActiveDocument.Revisions.AcceptAll()
            else:
                self.word.ActiveDocument.Revisions.RejectAll()
            # Delete all comments
            if self.word.ActiveDocument.Comments.Count >= 1:
                self.word.ActiveDocument.DeleteAllComments()
            doc.Close()
        except Exception as e:
            print(111, e)
        self.message_filter_revoke()


    def add_comment_at_range(self,range, comment_text):
        # Add a comment to the specified range in the document
        range.Comments.Add(range, Text=comment_text)


    def create_revisions_docx(self,doc_path1, doc_path2, output_path):
        self.message_filter_register()
        self.word.CompareDocuments(self.word.Documents.Open(doc_path1),
                                     self.word.Documents.Open(doc_path2), CompareWhitespace=False, IgnoreAllComparisonWarnings=True)

        # self.word.ActiveDocument.ActiveWindow.View.Type = 3

        # 引用常量模块
        word_constants = win32.constants
        # word.ActiveDocument.ActiveWindow.View.Type = 3
        # 设置文档为显示修订模式
        self.word.ActiveDocument.TrackRevisions = True
        # print(word_constants.__dicts__)

        # 显示所有修订标记
        self.word.ActiveWindow.View.RevisionsFilter.Markup = word_constants.wdRevisionsMarkupAll  # 1 表示显示所有标记

        # 显示所有标记，包括格式更改
        self.word.ActiveWindow.View.RevisionsFilter.View = word_constants.wdRevisionsViewFinal  #  表示显示所有标记，包括格式更改
        #
        self.word.ActiveDocument.SaveAs(FileName=output_path)

        self.message_filter_revoke()

    def add_revisions2comment_docx(self,doc_path):
        try:
            self.message_filter_register()
            word = win32.Dispatch("Word.Application")
            word.Visible = False
            doc = word.Documents.Open(doc_path)

            # Access the Revisions collection
            revisions = doc.Revisions

            # Iterate through the revisions and print details
            for revision in revisions:
                print(f"Type: {revision.Type}")
                print(f"Author: {revision.Author}")
                print(f"Date: {revision.Date}")
                print(f"Range Text: {revision.Range.Text}")
                print("---------------")
            doc.Close()

        except Exception as e:
            print(f"An error occurred: {e}")
        # for revision in word.ActiveDocument.Revisions:
        #
        #     if revision.Type == 2:  # Type 2 corresponds to wdRevisionInsert
        #         self.add_comment_at_range(revision.Range, "Inserted: " + revision.Range.Text)
        #
        #     elif revision.Type == 3:  # Type 3 corresponds to wdRevisionDelete
        #         self.add_comment_at_range(revision.Range, "Deleted: " + revision.Range.Text)

        self.message_filter_revoke()


if __name__ == "__main__":
    close_word_window()
    current_directory = os.path.dirname(__file__)
    document1_path = os.path.join(current_directory,"unlock_unstd_unstatic_带宽罚则 非锁定版(非标准合同)_IDC主协议_北京世纪互联宽带数据中心托管服务协议(2023年版)-（非预留机柜）.docx")
    document2_path = os.path.join(current_directory,"a.docx")

    word_parse=WordParse()
    word_parse.word_app_dispatch()
    word_parse.track_doc(document1_path)

    word_parse.track_doc(document2_path)
    time.sleep(1)

    output_document_path =os.path.join(current_directory,"output_document.docx")

    word_parse.word_app_dispatch()
    word_parse.create_revisions_docx(document1_path, document2_path, output_document_path)
    word_parse.word_app_quit()

    time.sleep(2)

    word_parse.add_revisions2comment_docx(output_document_path)
    time.sleep(2)

    close_word_window()