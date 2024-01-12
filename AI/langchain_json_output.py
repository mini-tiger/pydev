
# -*- coding: utf-8 -*-
import json
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

# CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
cot_template = """
You are a helpful assistant. Extract data center name and time, Your response should be in JSON format.
example 1:
    human:上海外高桥数据中心2023-10-01的上架率?
    AI: name:上海外高桥数据中心,date:2023-10-01
example 2:
    human: 2023-10-02北京大兴数据中心的上架率?
    AI: name:北京大兴数据中心,date:2023-10-02
example 3:
    human:北京星光数据中心的上架率?
    AI: name:上海外高桥数据中心,date:null
"""
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
# system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_cot = SystemMessagePromptTemplate.from_template(cot_template)

# 用户的询问
human_template = "{human_input}"
human_prompt = HumanMessagePromptTemplate.from_template(human_template)

# 将以上所有信息结合为一个聊天提示
chat_prompt = ChatPromptTemplate.from_messages([ system_prompt_cot, human_prompt])

prompt = chat_prompt.format_prompt(human_input="2023年10月02日北京大兴数据中心的上架率?").to_messages()

# 接收用户的询问，返回回答结果
response = llm(prompt,stream=False)
print(response.content)
print(json.loads(response.content))