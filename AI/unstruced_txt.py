import docx
import nltk



from unstructured.partition.text import partition_text
elements = partition_text(filename="/data/work/pydev/file_对比转换/lock2023-1.docx.txt")

for i in elements:
    print(i)


