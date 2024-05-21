# -*- coding: utf-8 -*-
import json
import logging
from webapi.utils.tools import RunError
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
import re
# from webapi.db.vector import *
from webapi.log.setup import logger
from webapi.db.rag import *
import webapi.config as config
# start large model
'''
CUDA_VISIBLE_DEVICES=4,5 python src/api_demo.py   --model_name_or_path /media/llm/Qwen1.5-72B-Chat   --template qwen   --finetuning_type lora
'''
# 设置环境变量和API密钥
import os, langchain

os.environ["OPENAI_API_KEY"] = 'EMPTY'

# 创建聊天模型
from langchain.chat_models import ChatOpenAI





def generate_query(title, section, child_section):
    section_str = section
    child_section_str = child_section
    section_list = section.split(" ")
    child_section_list = child_section.split(" ")
    if len(section_list) == 2:
        section_str = section_list[1]
    if len(child_section_list) == 2:
        child_section_str = child_section_list[1]
    # return f"{title}的{child_section_str}"
    return f"我要写一份{title}，正在写{section_str}章节，请撰写{child_section_str}的内容，只输出内容，不要写根据文档信息。"


def vector_search(vectorstore, title, section, child_section, ip):
    txt = ''
    source = ''

    return txt, source


def large_model_return_section(vectorstore, ip, prompt, word_batch_size=50, word_batch_size_extend=60,
                               title="全球数据治理研究报告",
                               section="应收账款自动化软件行业界定和分类", child_section="行业定义、基本概念",**kwargs):
    llm = ChatOpenAI(model_name=config.BaseConfig.MODEL_NAME, temperature=0, openai_api_base=ip, max_tokens=3092, request_timeout=300)

    logger.info(f"{'==' * 15}-{title}---{section}--{child_section}-generate-{'==' * 15}")

    context_source = ""
    cleaned_text = ""
    vectorstore_search_result = ''
    err = None
    try:
        query_custom = generate_query(title, section, child_section)
        logger.info("query_custom: {}".format(query_custom))

        if int(config.BaseConfig.VECTOR_OPEN) == 1 and int(kwargs.get("query_vector_open")) == 1:

            vector_result = {}
            # gpuos 实现RAG
            if int(config.BaseConfig.GPUOS_PLATFORM) == 1:
                vector_result, err = vector_generator_with_gouos(query_custom)
            logger.info(f"RAG Result: {vector_result}")
            # if int(config.BaseConfig.LANGCHAIN_RAG) == 1:
            #     vector_result, err = vector_generator_with_langchain(vectorstore=vectorstore, query=query_custom,
            #                                                          url=ip)

                # human_template = "{human_input}"
                # human_prompt = HumanMessagePromptTemplate.from_template(human_template)
                #
                # # 将以上所有信息结合为一个聊天提示
                # chat_prompt = ChatPromptTemplate.from_messages([human_prompt])
                #
                # q = prompt.get('user').format(vector_text=vector_result['vectorstore_search_result'],
                #                               word_batch_size=word_batch_size,
                #                               word_batch_size_extend=word_batch_size_extend,
                #                               title=title, section=section, child_section=query_custom)
                # logger.info(f"!!!!prompt: {q}")
                # prompt = chat_prompt.format_prompt(human_input=q).to_messages()
                # # 接收用户的询问，返回回答结果
                # response = llm(prompt, stream=False)
                # cleaned_text = response.content
                #
                # context_source=vector_result['context_source']
                # return {"context_source": context_source, "context": cleaned_text,
                #         'vectorstore_search_result': vector_result['vectorstore_search_result']}, None

            if err is None:
                context_source = vector_result.get('context_source')
                cleaned_text = vector_result.get('context')
                vectorstore_search_result = vector_result.get('vectorstore_search_result')
        else:
            # CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
            # cot_template = prompt.get('cot')
            #
            # system_prompt_cot = SystemMessagePromptTemplate.from_template(cot_template)

            # 用户的询问
            human_template = "{human_input}"
            human_prompt = HumanMessagePromptTemplate.from_template(human_template)

            # 将以上所有信息结合为一个聊天提示
            chat_prompt = ChatPromptTemplate.from_messages([human_prompt])
            vectorstore_search_result, source_search_result = vector_search(vectorstore, title=title, section=section,
                                                                            child_section=child_section, ip=ip)

            q = prompt.get('user').format(vector_text=vectorstore_search_result,
                                          word_batch_size=word_batch_size,
                                          word_batch_size_extend=word_batch_size_extend,
                                          title=title, section=section, child_section=child_section)
            logger.info(f"!!!!prompt: {q}")
            prompt = chat_prompt.format_prompt(human_input=q).to_messages()
            # 接收用户的询问，返回回答结果
            response = llm(prompt, stream=False)
            cleaned_text = response.content
            # 使用正则表达式进行匹配
            # 去除换行符和空格
            # cleaned_text = text.replace(" ", "")
            # print(cleaned_text)
            logger.info(f"large model return: {cleaned_text}")

            # 提取内容来源
            context_source = source_search_result

            source_index = cleaned_text.find("内容来源:")  # 查找 "内容来源:" 的位置
            source_index_context = cleaned_text.find("小节编写内容:")  # 查找 "内容来源:" 的位置

            if source_index != -1 and source_index_context != -1:  # 如果找到了 "内容来源:"
                source_text = cleaned_text[source_index + len("内容来源:"):source_index_context]  # 从 "内容来源:" 的位置之后开始截取
                # print(source_text.strip())  # 输出截取的内容，使用 strip() 方法去除可能存在的空格和换行符
                context_source = source_text.strip()

            # 提取小节内容
            text_list = cleaned_text.split('小节编写内容:')

            if len(text_list) <= 1:
                logger.error(f"!!!subject: {title}, section:{section}, 小节名称:{child_section},source_text:{cleaned_text},err: section prompt result err: text_list neq 2")
                raise RunError("section prompt result err: text_list neq 2")
                # return None, RunError("section prompt result err: text_list neq 2")
            cleaned_text = text_list[1]
            # 检查第一个字符是否是回车
            if cleaned_text.startswith('\n'):
                # 替换第一个回车字符
                cleaned_text = cleaned_text.replace('\n', '', 1)

            # print("large model text:",cleaned_text)

            if len(cleaned_text) == 0:
                return {"context_source": context_source, "context": cleaned_text,
                        'vectorstore_search_result': vectorstore_search_result}, RunError(
                    "section prompt result err: is null")
    except Exception as e:
        logger.error(f"section prompt result err:{e.__str__()}")
        return {"context_source": context_source, "context": cleaned_text,
                'vectorstore_search_result': vectorstore_search_result}, RunError(
            f"section prompt result err:{e.__str__()}")
    finally:
        # logger.info( f"child_section:{child_section},source_search_result:{context_source},vector search result: {vectorstore_search_result}")
        if err is not None:
            logger.error(f"{title}-{section}--{child_section}--section prompt result err:{err}")
        logger.info(
            f"!!!小节名称:{child_section}\n,内容来源:{context_source}\n,内容:{cleaned_text}\n,vector search result: {vectorstore_search_result}")
        logger.info(f"{'==' * 15}--{title}--{section}-{child_section}-finish-{'==' * 15}")
    return {"context_source": context_source, "context": cleaned_text,
            'vectorstore_search_result': vectorstore_search_result}, None


if __name__ == "__main__":
    # title_result, err = return_title_with_question(ip="http://120.133.63.166:8001/v1",
    #                                                question="请生成单片机行业研究报告")
    # if err != None:
    #     print(err)
    #     exit(0)
    # print(title_result)
    from webapi.service.large_model_prompt import prompt_dict_tpl

    # vectorstore = generate_vector_obj(base_dir=config.BaseConfig.PDF_DIR,
    #                                   vector_index_file=config.BaseConfig.VECTOR_INDEX_FILE)

    r, err = large_model_return_section(vectorstore=object, ip="http://120.133.75.252:28006/v1/",
                                      prompt=prompt_dict_tpl.get('yi_rag'), word_batch_size=150,
                                      word_batch_size_extend=160,
                                      title="全球数据治理研究报告",
                                      section="全球数字治理焦点议题进展",
                                      child_section="结论",query_vector_open=1)
    print(err)
    print(r)
