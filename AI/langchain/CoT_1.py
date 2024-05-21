
# -*- coding: utf-8 -*-

'''欢迎来到LangChain实战课
https://time.geekbang.org/column/intro/100617601
作者 黄佳'''
# 设置环境变量和API密钥
import os,json
os.environ["OPENAI_API_KEY"] = 'EMPTY'

# 创建聊天模型
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature=0,openai_api_base="http://120.133.83.145:8000/v1")

# 设定 AI 的角色和目标
# role_template = "你是一个为花店电商公司工作的AI助手, 你的目标是帮助客户根据他们的喜好做出明智的决定"

# CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
from string import Template
cot_template = """
示例 1:
  人类：参考合同中的条款，是否损害了甲方的利益,返回xml格式,例如$ex
  -----------------------
  模板条款: 服务方保证电力的连通性达到99.9%，带宽连通性达到99.9%，DCSS/MPLS VPN/SD-WAN可用性达到99.9%。
  当前条款: 服务方保证电力的连通性达到99.99%，带宽连通性达到99.99%，DCSS/MPLS VPN/SD-WAN可用性达到99.99%。
  ----------------------- 
  AI：$AI
"""
d={"ex":"<harm>True</harm><detail>''</detail>","AI":"<harm>True</harm><detail>该条款对服务方设定了非常高的服务标准，承诺了近乎完美的连通性和可用性。如果服务方无法达到这些承诺，可能会面临严重的违约责任，包括退款、赔偿等。在现实运营中，达到这样的水平可能非常困难，尤其是考虑到自然灾害、技术故障和外部网络影响等不可控因素。因此，这样的条款可能对服务方构成潜在的经济损失和运营压力。服务方应考虑在合同中包含合理的除外条款或降低服务保证水平，以平衡风险。</detail>"}
tt=Template(cot_template)
cot=tt.substitute(d)
print(cot)

from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
# system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_cot = SystemMessagePromptTemplate.from_template(cot)

# 用户的询问
human_template = "{human_input}"
human_prompt = HumanMessagePromptTemplate.from_template(human_template)

# 将以上所有信息结合为一个聊天提示
chat_prompt = ChatPromptTemplate.from_messages([  human_prompt])
human_input = """请根据下面文本返回2组question,answer对，格式例如[{"question":"who are you?","answer":"I am a human who"},{"question":"how old are you?","answer":"I am 12 years old"}]
-----------------------
到出差目的地有多种交通工具可选择时，出差人员在不影响公务、确保安全的前提下，应当首选经济便捷的交通工具。
_______________________
"""

tt1=Template(human_input)
human=tt1.substitute(d)
print(human)

prompt = chat_prompt.format_prompt(human_input=human).to_messages()

# 接收用户的询问，返回回答结果
response = llm(prompt,stream=True)
# print(response)
result_json=response.json()

result_json=json.loads(result_json)
# print(result_json)
result=result_json['content']
print(result)
# print(json.loads(result))