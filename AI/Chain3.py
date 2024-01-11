
# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')
'''欢迎来到LangChain实战课
https://time.geekbang.org/column/intro/100617601
作者 黄佳'''
# 设置环境变量和API密钥
import os
os.environ["OPENAI_API_KEY"] = 'EMPTY'

# 创建聊天模型
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature=0,openai_api_base="http://120.133.83.145:9116/v1")

# 设定 AI 的角色和目标
# role_template = "你是一个为花店电商公司工作的AI助手, 你的目标是帮助客户根据他们的喜好做出明智的决定"

#CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
cot_time_template = """
你是一个时间字符提取工具 ，擅长解答关于时间字符串提取的问题。
仅输出关于时间的字符串

示例 1:
  人类：上海外高桥数据中心2022-10-01的上架率?
  2022-10-01

示例 2:
  人类：上海荷丹数据中心2022-10-02的上架率?
  2022-10-02
"""
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
# system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_cot = SystemMessagePromptTemplate.from_template(cot_time_template)

# 用户的询问
human_template = "{human_input}"
human_prompt = HumanMessagePromptTemplate.from_template(human_template)

# 将以上所有信息结合为一个聊天提示
chat_prompt = ChatPromptTemplate.from_messages([ system_prompt_cot, human_prompt])

prompt = chat_prompt.format_prompt(human_input="上海外高桥数据中心2023-12-01的上架率").to_messages()

# 接收用户的询问，返回回答结果
response = llm(prompt,stream=True)
print(response.content)

###
# CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
cot_datacenter_template = """
You are a data center name extraction expert who specializes in answering questions about data center name extraction.
仅输出关于数据中心名称的字符串

example 1:
  Human：上海外高桥数据中心2022-10-01的上架率?
  AI: 上海外高桥数据中心

example 2:
  Human：上海荷丹数据中心的情况?
  AI: 上海静安数据中心
  
"""
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
# system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_cot = SystemMessagePromptTemplate.from_template(cot_datacenter_template)

# 用户的询问
human_template = "{human_input}"
human_prompt = HumanMessagePromptTemplate.from_template(human_template)

# 将以上所有信息结合为一个聊天提示
chat_prompt = ChatPromptTemplate.from_messages([ system_prompt_cot, human_prompt])

prompt = chat_prompt.format_prompt(human_input="上海荷丹数据中心的概述?").to_messages()

# 接收用户的询问，返回回答结果
response = llm(prompt,stream=False)
print(response.content)