from paddleocr import PaddleOCR, draw_ocr

# https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_ch/quickstart.md
# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
import datetime
import time

start = time.time()
ocr = PaddleOCR(use_angle_cls=False, lang="en", use_gpu=False, show_log=False,strategy="fast")  # need to run only once to download and load model into memory
# img_path = '/data/work/pydev/AI/unstructured/example-docs/layout-parser-paper-fast.jpg'
img_path = '/mnt/05C3B087-24FB-4c67-B398-EDF6DDC950FF.png'
f = open('test.txt', 'w')

result = ocr.ocr(img_path, cls=True)
# print(result)
for idx in range(len(result)):  # 从第3页显示
    res = result[idx]
    for line in res:
        print(line)
        print((line[1])[0])
        f.write((line[1])[0])
        f.write("\n")

f.close()
end = time.time()
print("完成时间: %f s" % (end - start))#