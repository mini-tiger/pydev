
import os,copy
from unstructured.partition.docx import partition_docx

def word2txt(docpath, txtpath="1.txt"):
    elements = partition_docx(filename=docpath)
    copy_ele = copy.deepcopy(elements)
    ele_list = [i for i in copy_ele]
    with open(txtpath, "w") as f:
        for index,value in enumerate(ele_list):
            if (value.category).lower() == 'pagebreak':
                print(index)
                print(ele_list[index+1].text,ele_list[index+1].category)

word2txt(docpath="/data/work/pydev/neolink-dataset/contract-sentinel/source_docx/unlock_sjhl_unreserved_非锁定版(非标准合同)_IDC主协议_北京世纪互联宽带数据中心托管服务协议(2023年版)-（非预留机柜）.docx")