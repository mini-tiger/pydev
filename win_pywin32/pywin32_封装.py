from imessagefilter import CMessageFilter
import win32com.client as win32
import time, os, copy
from service.utils import replace_str
import subprocess


def close_word_window():
    # os.system("chcp 65001")
    # 执行命令，不显示输出和错误
    subprocess.run("chcp 65001", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run("taskkill /F /IM WINWORD.EXE", shell=True, text=True)


class WordMix():

    def message_filter_register(self):
        CMessageFilter.register()

    def message_filter_revoke(self):
        CMessageFilter.revoke()

    def word_app_dispatch(self):
        self.word = win32.gencache.EnsureDispatch("Word.Application")
        self.word.Visible = False
        return self.word

    def word_app_quit(self, word):
        word.Application.Quit()

    def request_word(self, force_close=False):
        if force_close:
            close_word_window()
        self.message_filter_register()
        word = self.word_app_dispatch()
        return word

    def release_word(self, word, doc, doc_save=True, force_close=False):
        if doc is not None:
            doc.Close(doc_save)
        # 关闭Word应用程序
        self.word_app_quit(word)
        self.message_filter_revoke()
        if force_close:
            close_word_window()

    def doc_parse(self, path_file_name):
        word = self.request_word(force_close=True)
        try:
            doc = word.Documents.Open(path_file_name)
            doc.Activate()

        except Exception as e:
            return None, None, e

        return word, doc, None

    # 保留特殊字符 to txt
    def doc_to_txt(self, path, txt_path, force_close=False):
        word, doc, e = self.doc_parse(path)
        try:
            if e is not None:
                raise e
            # Extract text from the document
            text_content = doc.Content.Text
            # Write the extracted text to a text file
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text_content)
        finally:
            self.release_word(word, doc, force_close=True)

    def custom_doc_to_txt(self, path, txt_path, force_close=False):
        word, doc, e = self.doc_parse(path)
        try:
            if e is not None:
                raise e
            text_dict = {}
            text_dict_map = {}
            # Extract text from the document
            paragraphs = doc.Paragraphs

            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                for paragraph in paragraphs:
                    text = copy.deepcopy(paragraph.Range.Text)
                    txt_file.write(replace_str(text))
                    txt_file.write('\n')

                    section_number = paragraph.Range.ListFormat.ListString
                    start_page_number = paragraph.Range.Information(win32.constants.wdActiveEndPageNumber)
                    # 获取段落的样式
                    # paragraph_style = paragraph.Range.ParagraphFormat.Style.NameLocal

                    # print(f"当前文本:{replace_str(text)}")
                    # print(f"当前段落序号:{section_number}")
                    # print(f"当前页码:{start_page_number}")
                    text_dict[replace_str(text)] = {"page": replace_str(f"{start_page_number}"),
                                                    "part": replace_str(section_number)}
                    text_dict_map[replace_str(text)] = text

        finally:
            self.release_word(word, doc, force_close=True)
        return text_dict, text_dict_map

    def create_revisions_docx(self, doc_path1, doc_path2, output_path):
        word = self.request_word()
        try:
            word.CompareDocuments(word.Documents.Open(doc_path1),
                                  word.Documents.Open(doc_path2), CompareWhitespace=False,CompareFormatting=False,
                                  IgnoreAllComparisonWarnings=True)
            word_constants = win32.constants
            # print(word_constants.__dict__)
            # 显示所有修订标记
            word.ActiveWindow.View.RevisionsFilter.Markup = word_constants.wdRevisionsMarkupAll  # 1 表示显示所有标记

            # 显示所有标记，包括格式更改
            word.ActiveWindow.View.RevisionsFilter.View = word_constants.wdRevisionsViewFinal
            # word.ActiveWindow.View.ShowFormatChanges = False
            # print(dir(word.ActiveWindow.View))
            # word.ActiveDocument.ActiveWindow.View.Type = 3
            # 设置文档为显示修订模式
            word.ActiveDocument.TrackRevisions = True

            #
            word.ActiveDocument.SaveAs(FileName=output_path)
        finally:
            self.release_word(word, None, force_close=True)

    def modify_doc_view(self, doc_path1):
        word, doc, e = self.doc_parse(doc_path1)
        try:

            # 引用常量模块
            word_constants = win32.constants
            # print(word_constants.__dict__)
            # 显示所有修订标记
            word.ActiveWindow.View.RevisionsFilter.Markup = word_constants.wdRevisionsMarkupAll  # 1 表示显示所有标记

            # 显示所有标记，包括格式更改
            word.ActiveWindow.View.RevisionsFilter.View = word_constants.wdRevisionsViewFinal
            # word.ActiveWindow.View.ShowFormatChanges = False
            # print(dir(word.ActiveWindow.View))
            # word.ActiveDocument.ActiveWindow.View.Type = 3
            # 设置文档为显示修订模式
            word.ActiveDocument.TrackRevisions = True
            word.ActiveDocument.TrackFormatting = False

            #
            # word.ActiveDocument.SaveAs(FileName=doc_path1)

        finally:
            self.release_word(word, doc, doc_save=True, force_close=True)


def extract_page_part(self, doc_path):
    word, doc, e = self.doc_parse(doc_path)
    try:
        if e is not None:
            raise e


    finally:

        self.release_word(word, doc, force_close=True)


def revision_stat(self, path_file_name, save_file, accept=False):
    word, doc, e = self.doc_parse(path_file_name)
    try:
        self.word.ActiveDocument.TrackRevisions = True  # 关闭默认修订模式 Maybe not need this (not really but why not)

        # Accept all revisions
        if accept:
            self.word.ActiveDocument.Revisions.AcceptAll()
        else:
            self.word.ActiveDocument.Revisions.RejectAll()
        # Delete all comments
        if self.word.ActiveDocument.Comments.Count >= 1:
            self.word.ActiveDocument.DeleteAllComments()

        word.ActiveDocument.SaveAs(FileName=save_file)
    finally:

        self.release_word(word, doc, force_close=True)


def revisions_index_extract(self, doc_path, text_dict):
    word, doc, e = self.doc_parse(doc_path)
    revision_index = {}
    try:
        for index, paragraph in enumerate(doc.Paragraphs):
            revisions = paragraph.Range.Revisions
            if revisions.Count > 0:
                revisions.AcceptAll()
                if replace_str(paragraph.Range.Text) in text_dict:
                    revision_index.setdefault(index, text_dict[replace_str(paragraph.Range.Text)])
    finally:
        self.release_word(word, doc, doc_save=False, force_close=True)
    return revision_index


def add_comments_with_dict(self, doc_path, text_dict):
    if len(text_dict) == 0:
        return
    # 1. 记录diff.docx 有修订的index,
    revision_index = self.revisions_index_extract(doc_path=doc_path, text_dict=text_dict)
    # 2. Accept diff.docx,将这些index 的行内容提取从 accept_diff.docx出来
    # 3.  在与text_dict key 比对

    word, doc, e = self.doc_parse(doc_path)
    print(12323, text_dict)
    print(323, revision_index)
    try:
        for index, paragraph in enumerate(doc.Paragraphs):
            # 获取段落的修订信息
            if index in revision_index.keys():
                # print("inhint",revision_index[index])
                current_paragraph = doc.Paragraphs.Item(index + 1)
                doc.Comments.Add(Range=current_paragraph.Range, Text=revision_index[index])
    finally:

        self.release_word(word, doc, force_close=True)


if __name__ == "__main__":
    current_directory = os.path.dirname(__file__)
    document1_path = os.path.join(current_directory,
                                  "unlock_unstd_unstatic_带宽罚则 非锁定版(非标准合同)_IDC主协议_北京世纪互联宽带数据中心托管服务协议(2023年版)-（非预留机柜）.docx")
    document2_path = os.path.join(current_directory,
                                  "北京世纪互联宽带数据中心托管服务协议-商予科技2023.11.8-Vlegal1109.docx")
    output_document_path = os.path.join(current_directory, "output_document.docx")
    # document2_path = os.path.join(current_directory,"蓝芯算力&世纪互联主合同-JH cmts-Vlegal1109_modify.docx")
    close_word_window()
    wm = WordMix()
    wm.create_revisions_docx(doc_path1=document1_path, doc_path2=document2_path, output_path=output_document_path)
    wm.modify_doc_view(output_document_path)