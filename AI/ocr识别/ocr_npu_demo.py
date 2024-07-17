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
import config
config.BaseConfig.use_gpu=True
def pdf_to_txt(pdf_file, txt_file):
    start = time.time()
    ocr = PaddleOCR(use_angle_cls=True,
                    lang="ch",
                    use_gpu=True,
                    show_log=False,
                    ocr_version="PP-OCRv4",
                    enable_mkldnn=True,
                    rec_model_dir=config.BaseConfig.rec_model_dir if config.BaseConfig.use_gpu else None,
                    det_model_dir=config.BaseConfig.det_model_dir if config.BaseConfig.use_gpu else None
                    )  # need to run only once to download and load model into memory
    img_path = pdf_file

    f = open(txt_file, 'w', encoding='utf-8')

    result = ocr.ocr(img_path, cls=True)
    for idx in list(range(len(result)))[:]:
        res = result[idx]
        for line in res:
            print((line[1]))
            f.write((line[1])[0])
            f.write("\n")

    f.close()
    end = time.time()
    print("完成时间: %f s" % (end - start))  #


def to_word(txt, word_file):
    from docx import Document

    # 打开文本文件进行读取
    with open(txt, 'r', encoding='gbk') as file:
        text_content = file.read()

    # 创建一个新的 Word 文档
    doc = Document()

    # 添加文本内容到 Word 文档中
    doc.add_paragraph(text_content)

    # 保存 Word 文档
    doc.save(word_file)


if __name__ == "__main__":
    pdf_file = 'pdf_files/咨高技72 中国国际工程咨询有限公司关于中国科学院“十四五”科教基础设施—碳汇监测技术与国产装备研发能力提升项目（可行性研究报告）的咨询评估报告.pdf'
    txt_file = 'test.txt'
    word_file = 'test.docx'
    pdf_to_txt(pdf_file, txt_file)
    # to_word(txt_file, word_file)
