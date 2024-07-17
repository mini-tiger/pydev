from unstructured.partition.pdf import partition_pdf
import os
os.environ['HTTP_PROXY']='http://localhost:1081'
os.environ['HTTPS_PROXY']='http://localhost:1081'
from huggingface_hub import hf_hub_download
hf_hub_download('unstructuredio/yolo_x_layout', 'yolox_l0.05.onnx')
# Returns a List[Element] present in the pages of the parsed pdf document
# elements = partition_pdf('/mnt/m6.pdf')

# Applies the English and Swedish language pack for ocr. OCR is only applied
# if the text is not available in the PDF.

elements = partition_pdf('/mnt/191/业务发文报告/高技18中国国际工程咨询有限公司关于印送彩虹（合肥）液晶玻璃有限公司高分辨率显示用玻璃基板生产线项目专家组验收意见的函.pdf',
                         ocr_languages="chi",max_partition=None)

# for el in elements:
#     print(el.to_dict())

f = open('test.txt', 'w')
for el in elements:
    # if el.metadata.page_number == 3:
        print(el.to_dict())
        f.write(el.to_dict().get("text"))
        f.write("\n")

f.close()
