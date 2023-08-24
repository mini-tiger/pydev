from paddleocr import PaddleOCR, draw_ocr
# deploy
# https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_ch/quickstart.md
# model download
# https://github.com/PaddlePaddle/PaddleOCR/blob/static/doc/doc_ch/quickstart.md

# server delpy
# https://zhuanlan.zhihu.com/p/513377092
# https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_ch/models_list.md

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`

import time

start = time.time()
ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False, show_log=False,strategy="fast")  # need to run only once to download and load model into memory
img_path = '/mnt/m6.pdf'

f = open('test.txt', 'w')

result = ocr.ocr(img_path, cls=True)
for idx in list(range(len(result)))[2:]:  # 从第3页显示
    res = result[idx]
    for line in res:
        print((line[1])[0])
        f.write((line[1])[0])
        f.write("\n")

f.close()
end = time.time()
print("完成时间: %f s" % (end - start))#