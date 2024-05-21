
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
llm = ChatOpenAI(temperature=0,openai_api_base="http://120.133.63.166:8007/v1")

# 设定 AI 的角色和目标
# role_template = "你是一个为花店电商公司工作的AI助手, 你的目标是帮助客户根据他们的喜好做出明智的决定"

# CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
cot_template = """
example:
  Human：You are an identity reviewer, please help me,Extract the Chinese name and ID number from the following text
-------------------------
Hi @cc@neolink.com
下周一，我司有服务商人员上门更换设备硬盘操作，请帮忙授权,谢谢。

时间：2024.03.18 周一
姓名：翁宝喆 
身份证：440103199809021832
姓名：张三 
身份证：440103199809021833
-------------------------
Return to fixed format: username: \n id number:
  AI：username:翁宝喆\nid number:440103199809021832

"""
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
# system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_cot = SystemMessagePromptTemplate.from_template(cot_template)

prompt_prefix='''You are an information extraction expert, adept at extracting information from content. The extracted information includes: initiator, initiation date, access instructions, computer room name, start date, end date, name of the reservation person, ID number of the reservation person, and mobile phone number. The content is as follows'''
human_test_input=prompt_prefix+'''-------------------------
尊敬的用户
         您好！您申请1位工作人员进入广州科学城连云数据中心，进机房日期3/18，预约已成功。机房地址：广州市黄埔区连云路388号广州科学城连云数据中心，请进机房人员携带好有效身份证件前往！温馨提示：机房重地，严禁吸烟！如有异议，请询4006519966，祝您愉快！
顺颂商祺
Hi @cc@neolink.com
  下周一，我司有服务商人员上门更换设备硬盘操作，请帮忙授权,谢谢。

时间：2024.03.18 周一
姓名：翁宝喆 
身份证：440103199809021832

故障设备位置：405机房-AC01-09号机柜 13-14U位置
-------------------------
Return to fixed format json{ "initiator": "@cc@neolink.com",\n  "initiation_date": "N/A","computer_room_name": "广州科学城连云数据中心",\n  "start_date": "2024.03.18",\n  "end_date": "2024.03.18",\n   "name": "翁宝喆",\n    "identification": "440103199809021832",\n     "additional_info": "机房地址：广州市黄埔区连云路388号\\n温馨提示：机房重地，严禁吸烟！如有异议，请询4006519966"\n}
'''

# 用户的询问
human_template = "{human_input}"
human_prompt = HumanMessagePromptTemplate.from_template(human_template)

# 将以上所有信息结合为一个聊天提示
chat_prompt = ChatPromptTemplate.from_messages([  human_prompt])

prompt = chat_prompt.format_prompt(human_input=human_test_input).to_messages()

# 接收用户的询问，返回回答结果
response = llm(prompt,stream=False)
print(response)