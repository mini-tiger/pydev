# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import sys
import json
import xmltodict
import os, shutil
import utils
import prompt_ex
import mysql_conn
import ocr as ocr
from loguru import logger
from neo4j_conn import New_conn_neo4j, uri, username, password
# 创建日志目录（如果不存在）
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 日志文件路径
log_file_path = os.path.join(log_dir, "app.log")

# 配置 logger
logger.remove()  # 移除默认配置
logger.add(sys.stdout, level="DEBUG", format="{time} {level} {file}:{line} - {message}")
logger.add(log_file_path, level="DEBUG", format="{time} {level} {file}:{line} - {message}", rotation="10 MB")
# sys.stdout.reconfigure(encoding='utf-8')
'''欢迎来到LangChain实战课
https://time.geekbang.org/column/intro/100617601
作者 黄佳'''
# 设置环境变量和API密钥
import os
import config

os.environ["OPENAI_API_KEY"] = 'EMPTY'

# 创建聊天模型
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0.1, openai_api_base=config.BaseConfig.openai_base, model="Qwen1.5-72B-Chat",max_tokens=4096)


def invoke_llm(pdf_txt, cot, human_tpl):
    try:
        # CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
        cot_time_template = cot

        from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

        system_prompt_cot = SystemMessagePromptTemplate.from_template(cot_time_template)

        # 用户的询问
        # 将以上所有信息结合为一个聊天提示
        human_template = "{human_input}"
        human_prompt = HumanMessagePromptTemplate.from_template(human_template)

        # 将以上所有信息结合为一个聊天提示
        # chat_prompt = ChatPromptTemplate.from_messages([system_prompt_cot, human_prompt])
        chat_prompt = ChatPromptTemplate.from_messages([human_prompt])
        human_input = human_tpl.format(pdf_txt=pdf_txt)
        human_input = cot + human_input
        print(human_input)
        prompt = chat_prompt.format_prompt(human_input=human_input).to_messages()
        logger.debug(prompt)
        # 接收用户的询问，返回回答结果
        response = llm(prompt, stream=False)
        logger.debug(response.content)
    except Exception as e:
        logger.error(e)
        return None
    return response.content


def mix_llm(cot, human):
    # CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
    cot_time_template = cot

    from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

    system_prompt_cot = SystemMessagePromptTemplate.from_template(cot_time_template)

    # 用户的询问
    # 将以上所有信息结合为一个聊天提示
    human_template = "{human_input}"
    human_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # 将以上所有信息结合为一个聊天提示
    chat_prompt = ChatPromptTemplate.from_messages([system_prompt_cot, human_prompt])

    prompt = chat_prompt.format_prompt(human_input=human).to_messages()

    # 接收用户的询问，返回回答结果
    response = llm(prompt, stream=False)
    return response.content


def wr_xml_file(output_file_path, xml_str):
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(xml_str)


def xml_to_json(xml_file, json_file):
    try:
        with open(xml_file, 'r', encoding='utf-8') as file:
            xml_content = file.read()
        # 将XML转换为字典
        data_dict = xmltodict.parse(xml_content)
        # 将字典转换为JSON
        json_data = json.dumps(data_dict, indent=4, ensure_ascii=False)

        # 将JSON保存到文件
        with open(json_file, 'w', encoding='utf-8') as json_file:
            json_file.write(json_data)

        logger.info(f"XML has been successfully converted to JSON and saved to {json_file.name}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e


def clean_xml(text):
 # 检查并提取匹配字符后的内容
    if '：' in text:
        result = text.split('：', 1)[1]  # 按 '：' 分割并取第二部分
    elif ':' in text:
        result = text.split(':', 1)[1]  # 按 ':' 分割并取第二部分
    else:
        result = text  # 如果不包含指定字符，则返回空字符串
    
    return result

    return cleaned_text
def validate_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        logger.info(f"XML file is valid Root element: {root.tag}")
        return True
    except ET.ParseError as e:
        logger.error(f"!!!!! XML file is not valid. Error: {e}")
        return False


def process_xml_insert_db(filename, output_directory, total_pages, pdf_rule, prefix, retry=0,error=None):
    if retry > 1:
        return None,None,None,error
    try:
        cot = pdf_rule["cot"]
        human_tpl = pdf_rule["human_tpl"]

        pdf_path = os.path.join(ocr.input_directory, filename)

        output_text_file = os.path.join(output_directory, prefix + os.path.basename(pdf_path).replace('.pdf', '.txt'))
        os.remove(output_text_file) if os.path.exists(output_text_file) else None

        output_xml_file = os.path.join(output_directory, prefix + os.path.basename(pdf_path).replace('.pdf', '.xml'))

        os.remove(output_xml_file) if os.path.exists(output_xml_file) else None
        output_json_file = os.path.join(output_directory, prefix + os.path.basename(pdf_path).replace('.pdf', '.json'))
        os.remove(output_json_file) if os.path.exists(output_json_file) else None

        # pdf_txt = ocr.process_pdf_file(pdf_path, output_directory, output_text_file, ocr.save_images, pdf_rule)
        pdf_txt = ocr.process_pdf_file(pdf_path=pdf_path, output_directory=output_directory, total_pages=total_pages,
                                       pdf_rule=pdf_rule)
        if len(pdf_txt) <= 2:
            raise Exception(f"{pdf_rule['pdf_page']}.txt,content len lte 2")
        
        pdf_txt = pdf_txt.lstrip('\n ')
        resp_context = invoke_llm(pdf_txt=pdf_txt, cot=cot, human_tpl=human_tpl)
        if resp_context is None:
            raise Exception("llm error")

        # llm GLM3 split
        resp_context = clean_xml(resp_context)
        logger.debug(resp_context)

        wr_xml_file(output_xml_file, xml_str=resp_context)
        xml_to_json(xml_file=output_xml_file, json_file=output_json_file)

        if validate_xml(output_xml_file):
            parsed_xml = xmltodict.parse(resp_context)
            return parsed_xml,output_xml_file,output_json_file,error
        else:
            raise Exception("XML validation failed.")
    except BaseException as e:
        logger.error(f"{e},retry: {retry}")
        error=str(e)
        return process_xml_insert_db(filename, output_directory, total_pages, pdf_rule, prefix, retry=retry + 1,error=error)


def process_xml_data(filename, output_directory, xmbh,total_pages,retry=0,err_detail=None):
    if retry > 1:
        logger.error(f"retry:{retry},err_detail:{err_detail},move {filename} to {config.BaseConfig.err_pdf_files_dir}")
        return retry, err_detail

    # clear data
    mysql_conn.delete_records_by_filename(filename=filename)
    # New_conn_neo4j().delete_records_by_filename(filename)


    if mysql_conn.is_filename_exist(mysql_conn.Personnel,filename) is not None:
        # Personnel
        parsed_xml_personnel,personnel_output_xml_file,personnel_output_json_file,error = process_xml_insert_db(filename=filename,
                                                                                                          output_directory=output_directory,
                                                     total_pages=total_pages, pdf_rule=prompt_ex.Personnel_rule,
                                                     prefix="personnel", retry=0)
        # xml fail 直接返回
        if error is not None:
            err_detail = error
            retry = 2
            logger.error(f"err:{err_detail},filename:{filename},current retry num:{retry}")
            return retry,err_detail

        err_detail = mysql_conn.insert_personnel(mysql_conn.session, filename=filename,
                                                 parsed_xml=parsed_xml_personnel,xmbh=xmbh)
        if err_detail is None:
            logger.info(f"Successfully inserted Personnel DB with {filename}")
        else:
            #retry
            logger.error(f"err:{err_detail},filename:{filename},current retry num:{retry}")
            return process_xml_data(filename=filename, output_directory=output_directory, total_pages=total_pages,
                                    retry=retry+1,err_detail=err_detail,xmbh=xmbh)
    else:
        logger.debug(f"filename: {filename} Personnel record exist")

    # Project
    # if mysql_conn.is_filename_exist(mysql_conn.Report,filename) is not None:
    #     #有专家  在项目信息中 不考虑 error
    #     _,project_output_xml_file,project_output_json_file,_ = process_xml_insert_db(filename, output_directory=output_directory, total_pages=total_pages,
    #                                                pdf_rule=prompt_ex.Project_rule, prefix="project", retry=0)
    #
    #
    #     #xxx 总投资额 merge to project
    #     investment, unit = ocr.extraction_investment_amount_with_textfile(os.path.join(output_directory, "all.txt"))
    #
    #     utils.add_dict_to_xml(project_output_xml_file,data_dict={"investment_amount":investment,"investment_amount_unit":"万元"})
    #     parsed_xml_project = utils.read_xml_to_dict(project_output_xml_file)
    #
    #
    #     # 印发时间
    #     report_time=ocr.extraction_report_time(os.path.join(output_directory, "all.txt"))
    #     if report_time is not None:
    #         utils.add_dict_to_xml(project_output_xml_file,
    #                               data_dict={"report_time": report_time})
    #         parsed_xml_project = utils.read_xml_to_dict(project_output_xml_file)
    #         logger.info(parsed_xml_project)
    #
    #     xml_to_json(xml_file=project_output_xml_file, json_file=project_output_json_file)
    #
    #     err_detail = mysql_conn.insert_project(mysql_conn.session, filename=filename, parsed_xml=parsed_xml_project,xmbh=xmbh)
    #
    #     if err_detail is None:
    #         logger.info(f"Successfully inserted Project DB with {filename}")
    #     else:
    #         #retry
    #         logger.error(f"err:{err_detail},filename:{filename}")
    #         return process_xml_data(filename=filename, output_directory=output_directory,
    #                                 total_pages=total_pages,retry=retry+1,err_detail=err_detail,xmbh=xmbh)

    mysql_conn.session.close()
    return retry, err_detail


    # # # check filename duplicate
    # if New_conn_neo4j().check_report_exists(filename) and config.BaseConfig.NEO4J_USE:
    #     logger.warning(f"Report with filename {filename} already exists. Skipping creation.")
    #     return None,None
    #
    #     # Personnel Project
    #
    #     # 合并数据
    #     merged_data = {**parsed_xml_personnel, **parsed_xml_project}
    #     output_json_file = os.path.join(output_directory, os.path.basename(filename).replace('.pdf', '.json'))
    #     json_data = json.dumps(merged_data, ensure_ascii=False, indent=2)
    #     # 将JSON保存到文件
    #     with open(output_json_file, 'w', encoding='utf-8') as json_file:
    #         json_file.write(json_data)
    #
    #     # 插入报告和人员数据
    #     err=New_conn_neo4j().create_nodes_and_relationships(filename, merged_data)
    #     if err is not None:
    #         # retry
    #         logger.error(f"err:{err},filename:{filename}")
    #         process_xml_data(filename=filename, output_directory=output_directory, total_pages=total_pages, retry=retry + 1)



def query_db_agg():
    from langchain_community.utilities.sql_database import SQLDatabase
    from langchain_experimental.sql import SQLDatabaseChain

    db = SQLDatabase.from_uri(mysql_conn.db_uri)
    from langchain_community.agent_toolkits import create_sql_agent
    from langchain_openai import ChatOpenAI

    db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
    questions = "有多少个工程师及以上职称"
    res = db_chain.run(questions)
    print("问题：", questions, "解答：", res)
    # agent_executor = create_sql_agent(llm, db=db, agent_type="tool-calling", verbose=True)
    # abc = agent_executor.invoke(
    #     "how much people"
    # )
    # print(abc)


def llm_resp_rule(res):
    if utils.contains_any(res['result'], ["无法", "对不起", "抱歉"]):
        result_string = utils.list_of_dicts_to_string(res["intermediate_steps"][-1]["context"])
        cot = f"Personnel 表中字段信息{utils.generate_class_info(mysql_conn.Personnel)}\nReport表中字段信息{utils.generate_class_info(mysql_conn.Report)}"
        human = f"根据字段信息，结合已查到的相关数据与问题返回精简答案，忽略缺少的信息,数据:{result_string},问题:查询侯宇编写过哪些报告"
        resp = mix_llm(cot=cot, human=human)
        return resp
    return None


def query_neo4j():
    from langchain.chains import GraphCypherQAChain
    from langchain_community.graphs import Neo4jGraph
    from langchain_openai import ChatOpenAI

    graph = Neo4jGraph(url=uri, username=username, password=password)

    chain = GraphCypherQAChain.from_llm(llm=llm, graph=graph, verbose=True, return_intermediate_steps=True)  # 确保返回中间步骤)

    res = chain({"query": "查询侯宇编写过的2023年报告的数量"})
    print(res['result'])
    print(res["intermediate_steps"][-1])

    res = chain({"query": "查询侯宇编写过哪些报告"})
    print(res['result'])
    print(res["intermediate_steps"][-1])
    resp = llm_resp_rule(res)
    if resp is not None:
        print(resp)

    res = chain({"query": "查询2022,2023分别有多少报告"})
    print(res['result'])
    print(res["intermediate_steps"][-1])



def success_record(pdf_path,log_file_path,filename, content):
    utils.move_file_to_directory(pdf_path, config.BaseConfig.success_pdf_files_dir)
    append_to_file(log_file_path,filename,content)

def error_record(pdf_path,log_file_path,filename, content):
    utils.move_file_to_directory(pdf_path, config.BaseConfig.err_pdf_files_dir)
    append_to_file(log_file_path,filename,content)

def append_to_file(file_path,filename, content):
    """
    Append content to the specified file using UTF-8 encoding. If the file does not exist, it will be created.

    :param file_path: Path to the file
    :param content: Content to append
    """
    content=f"time:{utils.get_current_time()}   filename: {filename} -> content: {content}"
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(content + '\n')

if __name__ == '__main__':

    output_directory = config.BaseConfig.output_dir_base
    # print(output_directory)
    # 删除 重新创建目录
    shutil.rmtree(output_directory) if os.path.exists(output_directory) else os.makedirs(output_directory, exist_ok=True)

    # 处理目录中的所有 PDF 文件

    for filename in os.listdir(ocr.input_directory):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(ocr.input_directory, filename)
            file_size=utils.get_file_size(pdf_path)
            if file_size < 1024 *2: # 2kB
                logger.error(f"{filename},file size let 2k,Skip,Record ")
                error_record(pdf_path=pdf_path,
                             log_file_path=config.BaseConfig.download_fail_record_file,
                             filename=filename,content="file size let 2k")
                continue
            # xmbh
            xmbh = mysql_conn.get_xmbh_by_filename(filename)
            if xmbh is not None:
                logger.info(f"The xmbh :{xmbh} for {filename} ")
            else:
                logger.error(f"No xmbh found for {filename},Skip,Record ")
                error_record(pdf_path=pdf_path,
                             log_file_path=config.BaseConfig.download_fail_record_file,
                             filename=filename,content="mysql no exist xmbh")
                continue

            # all pages
            output_directory_new, total_pages = ocr.process_pdf_all_pages(pdf_path, output_directory)

            retry,err_detail= process_xml_data(filename=filename,output_directory=output_directory_new,
                                               total_pages=total_pages,err_detail=None,xmbh=xmbh)

            if retry > 1 and err_detail is not None:
                error_record(pdf_path=pdf_path,
                             log_file_path=config.BaseConfig.download_fail_record_file,
                             filename=filename,content=err_detail)
            else:
                success_record(pdf_path=pdf_path,
                             log_file_path=config.BaseConfig.download_success_record_file,
                             filename=filename,content='ok')




    # query_db_agg()
    # query_neo4j()
