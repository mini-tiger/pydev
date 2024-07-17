import time
from collections.abc import Iterable
from paddleocr import PaddleOCR
import fitz  # PyMuPDF
import os
import re
from loguru import logger
from prompt_ex import Personnel_rule
import config
from datetime import datetime
# Configuration
save_images = False  # 是否保存生成的 PNG 图像
input_directory = config.BaseConfig.pdf_files_dir  # 输入 PDF 文件目录
output_dir = config.BaseConfig.current_directory
import config
import utils

cpu_count_os = os.cpu_count()
# Initialize PaddleOCR
ocr = PaddleOCR(
    use_angle_cls=True,
    lang="ch",
    use_gpu=False,
    use_npu=True,
    show_log=True,
    ocr_version="PP-OCRv4",

    rec_model_dir=config.BaseConfig.rec_model_dir,
    det_model_dir=config.BaseConfig.det_model_dir
)


# Function to process each page
# 处理每个页面的函数
def process_page(page_num, page, save_images, output_directory):
    # 将 PDF 页面转换为图像
    pix = page.get_pixmap()
    img_path = f"{output_directory}/page_{page_num}.png"

    if save_images:
        pix.save(img_path)

    # 对图像进行 OCR
    result = ocr.ocr(pix.tobytes(), cls=True)
    # 输出OCR结果
    # for line in result:
    #     print(line)

    # 返回 OCR 结果及页面尺寸
    return result, pix.width, pix.height


# Function to extract text after keywords
def extract_text_after_keywords(text, keywords):
    if len(keywords) == 0 or keywords is None:
        return text
    lines = text.splitlines()
    for i, line in enumerate(lines):
        for keyword in keywords:
            # Check if line exactly matches the keyword and is not preceded by other characters
            if re.fullmatch(keyword, line.strip()):
                return "\n".join(lines[i:])
    return ""


# 检测是否为页码的函数
def is_page_number(text, bbox, page_width, page_height, margin=75):
    # 打印 bbox 信息用于调试
    # print(f"检测文本: {text}, bbox: {bbox},right_down: {bbox[2][1]},page_margin: {page_height - margin} 页宽: {page_width}, 页高: {page_height}")

    # 简单检查行是否为纯数字
    if re.match(r'^\d+$', text.strip()):
        # 提取左上角和右下角的 y 坐标
        y1 = bbox[2][1]
        # 如果文本位于页面底部边缘，则视为页码
        if y1 > page_height - margin:
            return True
    return False


def process_pdf_all_pages(pdf_path, output_dir):
    pdf_real_name = os.path.basename(pdf_path)
    output_directory: str = os.path.join(output_dir, utils.generate_timestamped_filename(pdf_real_name))
    utils.recreate_directory(output_directory)

    pdf_document = fitz.open(pdf_path)
    total_pages = len(pdf_document)
    logger.info(f"OCR PDF file  {pdf_path}")
    collected_text = ""

    output_text_all_file = os.path.join(output_directory, "all.txt")
    for page_num in range(0, total_pages):
        output_text_file = os.path.join(output_directory, f"{page_num}.txt")
        page = pdf_document.load_page(page_num)
        page_result, page_width, page_height = process_page(page_num, page, save_images, output_directory)

        page_text = ""
        for res in page_result:
            if isinstance(res, Iterable):  # 检查 res 是否为可迭代对象
                for line in res:
                    text, confidence, bbox = line[1][0], line[1][1], line[0]
                    '''
    [161.0, 109.0]: 左上角的坐标 (x0, y0)
    [186.0, 109.0]: 右上角的坐标 (x1, y0)
    [186.0, 125.0]: 右下角的坐标 (x1, y1)
    [161.0, 125.0]: 左下角的坐标 (x0, y1)
                    '''
                    text.replace('院干','院士')
                    # print(text, bbox, page_width, page_height)
                    if not is_page_number(text, bbox, page_width, page_height):
                        page_text += f"{text}\n"
            else:
                logger.warning(f"Warning: res is not iterable (type: {type(res)}), skipping this result. Value: {res}")
        with open(output_text_file, "w", encoding="utf-8") as f:
            f.write(page_text)
        collected_text += page_text + "\n"

        logger.info(f"OCR results saved to {output_text_file}")

    with open(output_text_all_file, "w", encoding="utf-8") as f:
        f.write(collected_text)

    return output_directory, total_pages


# Function to process each PDF file
def process_pdf_file(pdf_path, output_directory, total_pages, pdf_rule):
    start_page = 0
    if pdf_rule["pdf_page"] == "last_5":
        start_page = max(0, total_pages - 5)  # Only process the last 3 pages
    if pdf_rule["pdf_page"] == "head_1":
        start_page = 0
        total_pages = 1

    # logger.info(f"OCR PDF file  {pdf_path}")
    collected_text = ""

    for page_num in range(start_page, total_pages):
        page_text = ""
        with open(os.path.join(output_directory, f"{page_num}.txt"), 'r', encoding='utf-8') as file:
            page_text += file.read() + "\n"  # 每个文件内容之间添加换行符
        collected_text += page_text + "\n"

    filtered_text = extract_text_after_keywords(collected_text, pdf_rule["keywords"])
    # print(filtered_text)
    output_text_file = os.path.join(output_directory, f"{pdf_rule['pdf_page']}.txt")
    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write(filtered_text)

    logger.info(f"OCR results saved to {output_text_file}")
    return filtered_text


import re

# 定义正则表达式模式
# pattern = re.compile(r'([^\d]*?)((\d+\.\d+|\d+)(万?元|亿(?:里亚尔|元)?))[^\d]*')
# 定义正则表达式模式
pattern = re.compile(r'(?:总)?投资(?:为)?\s*(\d+\.\d+|\d+)\s*(万?元|亿(?:里亚尔|元)?)')


def convert_to_million_units(number, unit):
    if '亿' in unit:
        number *= 10000  # 将亿元转换为万元
    if '里亚尔' in unit:
        number *= 1.94  # 将亿里亚尔转换为万元
    return number


def extraction_investment_amount_with_textfile(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    number = 0
    unit = None
    # print(file_path)
    # 使用正则表达式匹配符合条件的句子
    matches = pattern.findall(text)
    if len(matches) == 0:
        return number, unit
    for match in matches[0:1]:
        number = float(match[0])
        unit = match[1]
        number = convert_to_million_units(number, unit)

    return number, unit


def extraction_report_time(file_path):
    # 提取日期的正则表达式
    date_pattern = r'(\d{4}年\d{1,2}月\d{1,2}日)\s*印发'

    # 从文件中读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 提取日期
    match = re.search(date_pattern, text)
    if match:
        date_str = match.group(1)
        logger.debug(f"提取的日期字符串:{date_str}")

        # 将日期字符串转换为 datetime 对象
        date_obj = datetime.strptime(date_str, '%Y年%m月%d日')

        # 将 datetime 对象格式化为 MySQL 时间列格式
        mysql_date_str = date_obj.strftime('%Y-%m-%d')
        logger.debug(f"转换后的 MySQL 日期格式:{mysql_date_str}")
        return mysql_date_str
    else:
        logger.debug("未找到日期字符串")
        return None

def scan_directory(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'all.txt':
                file_path = os.path.join(dirpath, filename)
                extraction_investment_amount_with_textfile(file_path)


if __name__ == '__main__':
    start_time = time.time()
    output_directory = os.path.join(output_dir, 'output')  # 指定输出目录
    os.makedirs(output_directory, exist_ok=True)
    # Process all PDF files in the directory

    pdf_path = os.path.join(config.BaseConfig.pdf_files_dir, "咨高技72 中国国际工程咨询有限公司关于中国科学院“十四五”科教基础设施—碳汇监测技术与国产装备研发能力提升项目（可行性研究报告）的咨询评估报告.pdf")
            # output_text_file = os.path.join(output_directory, os.path.basename(pdf_path).replace('.pdf', '.txt'))

    output_directory,total_pages = process_pdf_all_pages(pdf_path,output_directory)
    process_pdf_file(pdf_path=pdf_path, output_directory=output_directory, total_pages=total_pages, pdf_rule=Personnel_rule)
    print(time.time() - start_time)
    # scan_directory("/data/work/pydev/AI/ocr识别/output")
