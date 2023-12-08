from unstructured.partition.msg import partition_msg
from unstructured.partition.auto import partition
from PIL import ImageFile, Image
ImageFile.LOAD_TRUNCATED_IMAGES = True
def printele(elements):
    # print(elements)
    for i in elements:
        print(i)
    print("-" * 100)


filename = "/mnt/AI_Json/email/答复  关于摩根合同网络线路部分转签至摩根士丹利北京分公司合同.msg"
elements = partition_msg(filename=filename, attachment_partitioner=partition)
printele(elements)