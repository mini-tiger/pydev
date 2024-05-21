import copy
import os

from service_win32.utils import word2txt
from service_win32.file_struct_define import *

def ele2lines(elements):
    lines = []
    for i in elements:
        text = i.text
        if not text.endswith('\n'):
            text += '\n'
        lines.append(text)

    return lines


from service.utils import replace_str


def ele2txt(elements, txtpath, source_record_cls):
    copy_ele = copy.deepcopy(elements)
    ele_list = [i for i in copy_ele]
    with open(txtpath, "w") as f:
        for index, value in enumerate(ele_list):
            real_txt = replace_str(value.text)
            if len(real_txt) == 0:
                continue

            f.write(replace_str(value.text))
            if source_record_cls is not None:
                if index in source_record_cls.skip_enter_index:
                    continue
            f.write("\n")
            # if len(real_txt) > 0 and f.tell() > 0:
            #     if len(ele_list[index-1].text) > 0:
            #         f.write("\n")


from service_win32.utils import create_directory_if_not_exists




def convert_docx_to_txt(src_doc_dir, txt_dir):
    # 遍历目录中的所有文件
    txt_dict = {}
    txt_list = []
    create_directory_if_not_exists(src_doc_dir)
    create_directory_if_not_exists(txt_dir)
    for filename in os.listdir(src_doc_dir):
        if filename.endswith(".docx") and "~" not in filename:
            # 构建完整的文件路径
            full_path = os.path.join(src_doc_dir, filename)

            # 构建新的文件名，将扩展名修改为.txt
            new_filename = os.path.splitext(filename)[0] + ".txt"
            new_full_path_txt = os.path.join(txt_dir, new_filename)

            word2txt(docpath=full_path, txtpath=new_full_path_txt)

            txt_dict.setdefault(full_path, new_full_path_txt)
            txt_list.append(new_full_path_txt)
    return txt_dict, txt_list



def zhongzi_valid_search(txt):
    f = open(txt,"r",encoding='utf-8')
    file_content = f.readlines()
    f.close()
    if base_valid(file_content, str="采购合同书"):
        return "硬件采购合同_source.docx",True,"hard"

    if base_valid(file_content,str="软件开发服务合同书"):
        return "软件开发服务合同_source.docx",True,"soft"
    return "",False,""

def version_valid_search(txt):
    f = open(txt,"r",encoding='utf-8')
    file_content = f.readlines()
    f.close()

    record_cls=None
    valid=False
    if dyx_valid(file_content=file_content):
        if preset_valid(file_content=file_content):
            valid=True
            record_cls = dyx_unstd_reserved()
        else:
            valid=True
            record_cls = dyx_unstd_unreserved()

    # 必须满足
    if sjhl_valid(file_content) and base_valid(file_content, str="互联网信息安全责任书"):
        if preset_valid(file_content=file_content):
            valid=True
            record_cls = undyx_unstd_reserved()
        else:
            valid=True
            record_cls = undyx_unstd_unreserved()

    return record_cls,valid


def list_filter(q1, q2, file_list):
    tlist = [file for file in file_list if q1 in file and q2 in file and "~" not in file]


    return [file for file in tlist ]



def find_src_version_filename(search_path, dyx=False, reserved=False):
    file_list = os.listdir(search_path)
    if dyx and reserved:
        # 筛选同时包含'abc'和'789'的文件
        return list_filter(q1="dyx", q2="reserved", file_list=file_list)

    if dyx and reserved == False:
        return list_filter(q1="dyx", q2="unreserved", file_list=file_list)

    if dyx == False and reserved:
        return list_filter(q1="sjhl", q2="reserved", file_list=file_list)

    if dyx == False and reserved == False:
        return list_filter(q1="世纪互联", q2="非预留", file_list=file_list)


def dyx_valid(file_content):
    for line in file_content[0:10]:
        if "深圳" in line:
            return True
    return False


def sjhl_valid(file_content):
    for line in file_content[0:10]:
        if "北京世纪互联宽带数据中心" in line:
            return True
    return False


def base_valid(file_content, str):
    for line in file_content[0:100]:
        if str in line:
            return True
    return False


def preset_valid(file_content):
    for line in file_content[50:100]:
        if "预留机柜启用通知函" in line:
            return True
    return False

# if __name__ == "__main__":
#     txt_dict, txt_list = convert_docx_to_txt(directory="/data/work/pydev/word_对比转换/source_docx")
#
#     print(txt_dict.keys())
#
#     file1_content = txt_list[0]
#     file2_content = txt_list[1]
#
#     differ = DifflibParser(file1_content, file2_content)
#
#     if dyx_valid(file_content=file1_content):
#         print("1111")
#
#     if preset_valid(file_content=file2_content):
#         print("2222")
#
#     if preset_valid(file_content=file1_content):
#         print("3333")
#
#     if dyx_valid(file_content=file2_content):
#         if preset_valid(file_content=file2_content):
#             source_txt = "unlock_dyx_static"
#         else:
#             source_txt = "unlock_dyx_nostatic"
#
#     else:
#         if preset_valid(file_content=file1_content):
#             source_txt = "lock_std_static"
#         else:
#             source_txt = "unlock_unstd_unstatic"
#
#     for line in differ:
#         if line['code'] > 0:
#             print(line)
