# unstructured==0.13.2
# unstructured-client==0.18.0
import copy
import logging
from unstructured.partition.docx import partition_docx
from unstructured.partition.doc import partition_doc
import nltk
import re
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
# nltk.set_proxy('http://127.0.0.1:1081')
# nltk.download("punkt")
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
import os, json
from string import Template
import shutil
import tempfile
import os
# 执行命令
import subprocess

os.environ["OPENAI_API_KEY"] = 'EMPTY'
# 创建日志格式
# 创建一个格式化器
formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')

# 获取一个名为__name__的logger
logger = logging.getLogger(__name__)
# 设置logger的级别为INFO
logger.setLevel(logging.INFO)

# 创建一个控制台处理器，并设置级别为INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# 将处理器添加到logger
logger.addHandler(console_handler)

# 创建聊天模型
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0, openai_api_base="http://120.133.63.166:9027/v1", model_name="Baichuan2-13B-Chat",
                 request_timeout=300, max_tokens=4096)

ex_data_obj = {"data": [{"question": "中国的首都是哪里?", "answer": "北京"},
                        {"question": "中国的全称是什么?", "answer": "中华人民共和国"}
                        ]}
ex_data = json.dumps(ex_data_obj, ensure_ascii=False)


def replace_str(original_string):
    tstr = original_string.replace(' ', '').replace('\t', ''). \
        replace('【', '[').replace('】', ']').replace('“', ''). \
        replace('：', ':').replace("（", "(").replace("）", ")")
    new_str1 = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', "", tstr)
    new_str = re.sub(r'[\n\r]', ' ', new_str1)

    pattern = r"第.*?条"
    # 替换字符串中所有匹配的部分为一个空字符串
    result = re.sub(pattern, "", new_str)
    pattern1 = r"第.*?章"
    # 替换字符串中所有匹配的部分为一个空字符串
    result1 = re.sub(pattern1, "", result)
    return result1
    # return new_str


def valid_str(text):
    # if len(text) < 15:
    #     return False
    if text == "中国国际工程咨询有限公司":
        return False
    if '修订' in text and '月' in text and '年' in text and len(text) < 15:
        return False
    if '实施细则' in text and len(text) < 20:
        return False
    if ('盖章' in text or '签字' in text) and ('单位' in text or '理由' in text):
        return False
    return True


def is_valid_list(text):
    """
    检查字符串是否为有效的JSON格式。

    参数:
    text (str): 需要检查的字符串。

    返回:
    bool: 如果字符串是有效的JSON格式，则返回 True，否则返回 False。
    """
    try:
        # 尝试使用json.loads()解析字符串
        # result = json.loads(text)

        # print(text)
        json.loads(text)
        return None
    except json.JSONDecodeError:
        return "给定字符串不是有效的JSON格式列表。"
    except Exception as e:
        # 捕获其他异常，例如传入非字符串类型
        return str(e)


def contains_chinese(text):
    """
    检查字符串是否包含中文字符。

    参数:
    text (str): 需要检查的字符串。

    返回:
    bool: 如果字符串包含至少一个中文字符，则返回 True，否则返回 False。
    """
    # 中文字符的Unicode范围是从U+4E00到U+9FFF
    pattern = re.compile('[\u4e00-\u9fff]')

    # 使用search查找匹配的部分
    return bool(pattern.search(text))


def Generate_QA_with_txt(data, max_retry):
    max_retry = max_retry - 1
    error = None
    result = []

    # 用户的询问
    human_template = "{human_input}"
    human_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # 将以上所有信息结合为一个聊天提示
    chat_prompt = ChatPromptTemplate.from_messages([human_prompt])
    human_input = """根据下面文档内容生成$num组question,answer对,输出格式示例$ex
    -----------------------
    $data
    _______________________
    """
    num = len(data) // 25
    if num == 0:
        num = 1
    if num > 15:
        num = 15
    tt1 = Template(human_input)
    human = tt1.substitute({"num": num, "data": data,
                            "ex": ex_data})
    logger.info(f"txt human:{human}")

    prompt = chat_prompt.format_prompt(human_input=human).to_messages()
    try:
        # 接收用户的询问，返回回答结果
        response = llm(prompt, stream=False)
        # print(response)
        result_json = response.json()
        result_json = json.loads(result_json)
        # print(result_json)
        result_list_str = result_json['content']
        result_list_str = re.sub(r',\s*(}|\])', r'\1', result_list_str)
        valid_result = is_valid_list(result_list_str)
        if valid_result is not None:
            result, error = retry_generate_QA(result_list_str)
            if error is not None:
                logger.error(valid_result)
                raise ValueError(f"error:{valid_result} invalid list : {result}")
            logger.info(f"success len:{len(result)}")
            return result, None

        result = json.loads(result_list_str)['data']
        logger.info(f"success len:{len(result)}")
        return result, error
    except Exception as e:
        error = str(e)
        logger.error(f"restart Generate_QA_with_html,{error},max_retry:{max_retry}")
        if max_retry > 0:
            return Generate_QA_with_txt(data, max_retry)
        else:
            logger.error(f"final error:{error}")
    return result, error


def retry_generate_QA(data):
    error = None
    result = []

    # 用户的询问
    human_template = "{human_input}"
    human_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # 将以上所有信息结合为一个聊天提示
    chat_prompt = ChatPromptTemplate.from_messages([human_prompt])
    human_input = """根据下面文档内容生成question,answer对,输出格式示例$ex
    -----------------------
    $data
    _______________________
    """

    tt1 = Template(human_input)
    human = tt1.substitute({"data": data, "ex": ex_data})
    logger.info(f"retry human:{human}")

    prompt = chat_prompt.format_prompt(human_input=human).to_messages()
    try:
        # 接收用户的询问，返回回答结果
        response = llm(prompt, stream=False)
        # print(response)
        result_json = response.json()
        result_json = json.loads(result_json)
        # print(result_json)
        result_list_str = result_json['content']
        result_list_str = re.sub(r',\s*(}|\])', r'\1', result_list_str)

        valid_result = is_valid_list(result_list_str)
        if valid_result is not None:
            # logger.error(valid_result)
            raise ValueError(f"error:{valid_result}invalid list : {result_list_str}")

        # print(json.loads(result))
        result = json.loads(result_list_str)['data']
        return result, error
    except Exception as e:
        error = str(e)

    return result, error


def Generate_QA_with_html(data_struct, max_retry):
    max_retry = max_retry - 1
    error = None
    result = []
    data = ''
    if data_struct['category'] == "table":
        # data = data_struct['text']
        data = data_struct['text_as_html']

    # 用户的询问
    human_template = "{human_input}"
    human_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # 将以上所有信息结合为一个聊天提示
    chat_prompt = ChatPromptTemplate.from_messages([human_prompt])
    human_input = """下面html是描述$before_text,结合标题[$before_text]生成$num组question,answer对，格式例如$ex
    -----------------------
    $data
    _______________________
    """
    num = int(data.count("tr") // 2 - 1)
    if num <= 0:
        error = "table th is 0"
        return result, error

    if contains_chinese(data) is False:
        error = "table not contains chinese"
        # print(error)
        return result, error

    tt1 = Template(human_input)
    before_text = ""
    if len(data_struct['before_text']) < 15:
        before_text = data_struct['before_text']

    human = tt1.substitute({"num": num, "data": data,
                            'before_text': before_text,
                            "ex": ex_data})
    logger.info(f"html human:{human}")

    prompt = chat_prompt.format_prompt(human_input=human).to_messages()
    try:
        # 接收用户的询问，返回回答结果
        response = llm(prompt, stream=False)
        # print(response)
        result_json = response.json()
        result_json = json.loads(result_json)
        # print(result_json)
        result_list_str = result_json['content']

        valid_result = is_valid_list(result_list_str)
        # retry llm
        if valid_result is not None:
            result, error = retry_generate_QA(result_list_str)
            if error is not None:
                # logger.error(valid_result)
                raise ValueError(f"error:{valid_result}invalid list : {result}")
            logger.info(f"success len:{len(result)}")
            return result, None

        result = json.loads(result_list_str)['data']
        logger.info(f"success len:{len(result)}")
        return result, error
        # print(json.loads(result))
    except Exception as e:
        error = str(e)
        logger.error(f"restart Generate_QA_with_html,{error},max_retry:{max_retry}")
        if max_retry > 0:
            return Generate_QA_with_html(data_struct, max_retry)
        else:
            logger.error(f"final error:{error}")
    return result, error


class UnstrucedDocxLoader():
    def __init__(self, source_file):
        self.docx = None
        self.source_file = source_file
        self.source_file_name = os.path.basename(self.source_file)
        self.source_file_suffix = source_file.split(".")[1]
        # 创建一个临时目录
        self.temp_dir = tempfile.mkdtemp()
        self.txt_file = os.path.join("/data/work/pydev/AI/legal_demo", f'file.txt')
        # 构建目标文件的完整路径
        self.destination_file = os.path.join(self.temp_dir, f'copied_file.{self.source_file_suffix}')
        self.max_retry = 2
        # 打印出临时目录的路径，以便验证
        logger.info(f"临时目录路径：{self.temp_dir}")

    def copy_file_to_temp_dir(self):
        error = None

        try:
            # 复制文件到临时目录
            shutil.copy(self.source_file, self.destination_file)
            print(f"文件已成功复制到临时目录：{self.destination_file}")

        except IOError as e:
            print(f"无法复制文件。{e}")
            error = str(e)

        except Exception as e:
            print(f"发生了错误：{e}")
            error = str(e)

        return error

    def convert_doc2docx_to_temp_dir(self):
        error = None

        # libreoffice --headless --convert-to docx:"Office Open XML Text" /mnt/公司差旅费管理实施细则（咨财〔2019〕2583号，2019年修订）.doc --outdir ./
        # 设置文件名和输出目录
        # file_name = source_file
        # output_dir = os.path.dirname(destination_file)

        # 构建命令
        command = [
            'libreoffice', '--headless', '--convert-to', 'docx:"Office Open XML Text"',
            self.source_file, '--outdir', self.temp_dir
        ]

        pipe = subprocess.Popen(" ".join(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print('命令返回结果')
        stdout = pipe.stdout.read().decode()
        stderr = pipe.stderr.read().decode()

        if stderr == "":
            print(f"stdout:{stdout}")
        else:
            # print(stderr)
            error = stderr
        return error

    def Generate_QA_with_doc(self):

        # print("suffix: {}".format(suffix))
        if self.source_file_suffix == "doc":
            with open(self.source_file, "rb") as f:
                element = partition_doc(file=f)
        if self.source_file_suffix == "docx":
            with open(self.source_file, "rb") as f:
                element = partition_docx(file=f)
        unstruct_list = []

        before_text = ''
        for i in element:
            text = replace_str(i.text)

            if valid_str(text):
                if i.category.lower() == "table":
                    if valid_str(i.metadata.text_as_html):
                        unstruct_list.append(
                            {'before_text': before_text, 'text': text, 'category': i.category.lower(),
                             'text_as_html': i.metadata.text_as_html})
                else:
                    unstruct_list.append({'text': text, 'category': i.category.lower()})
            before_text = text
        return unstruct_list

    def Generate_QA_with_docx_for_langchain(self, txt):
        result_list = []
        error = None
        try:
            file = os.path.basename(txt)
            documents = []
            if file.endswith('.pdf'):
                loader = PyPDFLoader(txt)
                documents.extend(loader.load())
            elif file.endswith('.txt'):
                loader = TextLoader(txt)
                documents.extend(loader.load())

            # 2.Split 将Documents切分成块以便后续进行嵌入和向量存储
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=10,
                                                           # separators=["\n\n", "\n", "。", ".", ""]
                                                           separators=["\n", '\n\n', "。"],
                                                           is_separator_regex=True
                                                           )
            chunked_documents = text_splitter.split_documents(documents)
            # print(chunked_documents)
            # print(len(chunked_documents))

            for document in chunked_documents:
                result_list.append(document.page_content)
        except Exception as e:
            error = str(e)
        return result_list, error

    def write_to_txt(self, data):
        error = None
        # 打开文件进行写入，如果文件不存在则创建
        try:
            with open(self.txt_file, 'w') as file:
                file.write(data)
                print(f"数据已成功写入到文件 {self.txt_file}")
        except IOError as e:
            print(f"写入文件时发生错误：{e}")
        except Exception as e:
            print(f"发生了其他错误：{e}")
        return error

    def check_valid_item(self, item):
        r = False
        if isinstance(item, dict):
            if 'question' in item and "answer" in item:
                return True

        return r

    def format_clean_list(self, result_json_list):
        # 使用集合来存储已经见过的问题
        seen_questions = set()
        unique_data = []
        for ex in ex_data_obj['data']:
            seen_questions.add(ex["question"])

        for item in result_json_list:
            print(item, self.check_valid_item(item))
            if self.check_valid_item(item):
                if item['question'] not in seen_questions:
                    item1 = copy.deepcopy(item)
                    item1.setdefault('source', os.path.basename(self.source_file))
                    unique_data.append(item1)
                    seen_questions.add(item['question'])

        # 输出去重后的结果
        return unique_data

    def process(self):
        logger.info(f"current file begin process: {self.source_file_name}")
        if self.source_file_suffix not in ['doc', 'docx', "pdf", "txt"]:
            return f"not support {self.source_file_suffix}"
        result_json_list = []
        if self.source_file_suffix == "doc" or self.source_file_suffix == "docx":
            result_json_list.extend(self.process_word())
        if self.source_file_suffix == "pdf" or self.source_file_suffix == "txt":
            result_json_list.extend(self.process_txt_pdf())

        result_json_list = self.format_clean_list(result_json_list)

        logger.info(f"{len(result_json_list)},result_json_list:{result_json_list}")
        logger.info(f"current file finish process: {self.source_file_name}")
        return result_json_list

    def process_txt_pdf(self):
        result_json_list = []

        result, error = self.Generate_QA_with_docx_for_langchain(self.source_file)
        if error is None:
            for d in result:
                max_retry = copy.deepcopy(self.max_retry)
                txt_json, err = Generate_QA_with_txt(d, max_retry=max_retry)
                if err is None:
                    # print(type(txt_json))
                    result_json_list.extend(txt_json)
                logger.info(f"err:{err}, len:{len(txt_json)}, txt_json:{txt_json}")

        return result_json_list

    def process_word(self):
        error = self.copy_file_to_temp_dir()
        if error is not None:
            return error
        result_json_list = []
        # doc 转换docx
        # if self.source_file_suffix.endswith('.doc'):
        #     error=self.convert_doc2docx_to_temp_dir()
        data_list = self.Generate_QA_with_doc()

        txt_data = []
        for d in data_list:
            if d['category'] == 'table':
                max_retry = copy.deepcopy(self.max_retry)
                txt_json, error = Generate_QA_with_html(d, max_retry=max_retry)
                logger.info(f"txt_json:{txt_json}")
                if error is None:
                    result_json_list.extend(txt_json)
            else:
                txt_data.append(d['text'] + "\n")

        self.write_to_txt(''.join(txt_data))
        result, error = self.Generate_QA_with_docx_for_langchain(self.txt_file)
        if error is None:
            for d in result:
                max_retry = copy.deepcopy(self.max_retry)
                txt_json, err = Generate_QA_with_txt(d, max_retry=max_retry)
                logger.info(f"txt_json:{txt_json}")
                # print(type(txt_json))
                result_json_list.extend(txt_json)
        return result_json_list


if __name__ == "__main__":
    total_num=0
    # 读取目录 或多文件
    base_dir="/data/work/pydev/AI/legal_demo/doc_dir"
    for file in os.listdir(base_dir):
        ul = UnstrucedDocxLoader(
            source_file=os.path.join(base_dir,file))
        result_list = ul.process()
        total_num += len(result_list)
        logger.warning(f"len:{len(result_list)}")
    print(total_num)
    # 单文件
    # ul = UnstrucedDocxLoader(source_file="/data/work/pydev/AI/legal_demo/外聘专家出差标准-20240413.txt")
    # ul.process()
