from service_win32.global_instance import word_Mix_parse
import os,shutil
from service.utils import replace_str,add_enter
from tools.utils import *



def docfilename_to_txtfilename(file_path, base_dir):
    file_name = os.path.basename(file_path)  # Gets the file name with extension
    file_name_list = os.path.splitext(file_name)  # Gets the file extension
    file_ext = file_name_list[1]
    file_name_real = file_name_list[0]
    out_file = os.path.join(base_dir, file_name_real + ".txt")
    delete_file_if_exists(out_file)
    return out_file


def rebuild_page_word_comments_write_with_dict(diff_doc_path, text_dict):
    comments_dict = {}
    text_dict_rebuild ={}
    for key, value in text_dict.items():
        risk_effect = ""
        risk_effect = f"大模型分析:{add_enter(value['effect'])}"
        if 'risk' in value:
            if value['risk'] is not None :
                risk_effect = f"风险提示:{add_enter(value['risk'])}\n大模型分析:{add_enter(value['effect'])}"


        comments_dict.setdefault(replace_str(key), risk_effect)
        text_dict_rebuild.setdefault(replace_str(key),value)
    text_dict_rebuild1=word_Mix_parse.rebuild_page_and_add_comments_with_dict(doc_path=diff_doc_path, comments_dict=comments_dict,text_dict=text_dict_rebuild)

    return text_dict_rebuild1


def word_deny_filename_build(path, base_path, save_path_prefix):
    file = os.path.basename(path)
    deny_file=os.path.join(base_path, save_path_prefix + file)
    delete_file_if_exists(deny_file)
    return deny_file

def deny_word_revision(path, save_path):
    try:
        return word_Mix_parse.revision_stat(path, save_path, False)
    except Exception as e:
        raise e


def word2txt(docpath, txtpath):
    try:
        return word_Mix_parse.custom_doc_to_txt(path=docpath, txt_path=txtpath, force_close=True)
    except Exception as e:
        raise e

def word_table_output(docpath):
    try:
        return word_Mix_parse.table_output_list(docpath)
    except Exception as e:
        raise e


def create_revisions_docx(src_doc, dest_doc, out_doc):
    try:
        delete_file_if_exists(out_doc)
        word_Mix_parse.create_revisions_docx(src_doc, dest_doc, out_doc)
    except Exception as e:
        raise e
