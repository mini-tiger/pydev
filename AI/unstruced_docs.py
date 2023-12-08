import docx
import nltk

nltk.set_proxy('http://127.0.0.1:1081')
nltk.download("punkt")

from unstructured.partition.docx import partition_docx
# elements = partition_docx(filename="my.docx")

with open("/mnt/AI_Json/source_docx_modify/a.docx", "rb") as f:
    element = partition_docx(file=f)

unstruct_dict={}

for i in element:
    # print(i.metadata)
    # print(i.to_dict())
    # if i.category == "Table":
    #     print(i.to_dict())
    unstruct_dict[i.text]=i.metadata

# print(unstruct_dict)
for key,value in unstruct_dict.items():
    print(key,value)