
import os
from unstructured.partition.docx import partition_docx


def ele2lines(elements):
    lines = []
    for i in elements:
        text = i.text
        if not text.endswith('\n'):
            text += '\n'
        lines.append(text)

    return lines


def word2txt(docpath, txtpath):
    elements = partition_docx(filename=docpath)
    with open(txtpath, "w") as f:
        for i in elements:
            f.write(i.text)
            f.write("\n")


def convert_docx_to_txt(src_doc_dir, txt_dir):
    # 遍历目录中的所有文件
    txt_dict = {}
    txt_list = []
    for filename in os.listdir(src_doc_dir):
        if filename.endswith(".docx"):
            # 构建完整的文件路径
            full_path = os.path.join(src_doc_dir, filename)

            # 构建新的文件名，将扩展名修改为.txt
            new_filename = os.path.splitext(filename)[0] + ".txt"
            new_full_path_txt = os.path.join(txt_dir, new_filename)
            word2txt(docpath=full_path, txtpath=new_full_path_txt)
            txt_dict.setdefault(full_path, new_full_path_txt)
            txt_list.append(new_full_path_txt)
    return txt_dict, txt_list


def list_filter(q1, q2, file_list):
    return [file for file in file_list if q1 in file and q2 in file]


def find_src_version_filename(source_txt_path, dyx=False, reserved=False):
    file_list = os.listdir(source_txt_path)
    if dyx and reserved:
        # 筛选同时包含'abc'和'789'的文件
        return list_filter(q1="dyx", q2="static", file_list=file_list)

    if dyx and reserved == False:
        return list_filter(q1="dyx", q2="free", file_list=file_list)

    if dyx == False and reserved:
        return list_filter(q1="sjhl", q2="static", file_list=file_list)

    if dyx == False and reserved == False:
        return list_filter(q1="sjhl", q2="free", file_list=file_list)


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

def base_valid(file_content,str):
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
