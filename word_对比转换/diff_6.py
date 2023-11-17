from difflibparser.difflibparser import *
import os
from unstructured.partition.docx import partition_docx

def word2txt(docpath,txtpath):
    elements = partition_docx(filename=docpath)
    with open(txtpath, "w") as f:
        for i in elements:
            f.write(i.text)
            f.write("\n")

def convert_docx_to_txt(directory,dest_dir):
    # 遍历目录中的所有文件
    txt_dict ={}
    txt_list =[]
    for filename in os.listdir(directory):
        if filename.endswith(".docx"):
            # 构建完整的文件路径
            full_path = os.path.join(directory, filename)

            # 构建新的文件名，将扩展名修改为.txt
            new_filename = os.path.splitext(filename)[0] + ".txt"
            new_full_path_txt = os.path.join(dest_dir, new_filename)
            word2txt(docpath=full_path,txtpath=new_full_path_txt)
            txt_dict.setdefault(full_path,new_full_path_txt)
            txt_list.append(new_full_path_txt)
    return txt_dict,txt_list

txt_dict,txt_list=convert_docx_to_txt(directory="/data/work/pydev/word_对比转换/source_docx",dest_dir="/data/work/pydev/word_对比转换/source_txt")


