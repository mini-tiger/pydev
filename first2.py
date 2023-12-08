# 设置环境变量和API密钥
import os
os.environ["OPENAI_API_KEY"] = '你的OpenAI API Key'
# pip install langchain
# pip install openai
# 创建聊天模型
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    openai_api_base="http://120.133.83.145:8000/v1", # http://120.133.83.145:8000/v1/chat/completions
    openai_api_key="EMPTY",
    # openai_proxy=current_app.config["OPENAI_PROXY"],
    temperature=0,
)

# 设定 AI 的角色和目标
role_template = "你是一名律师，根据你的专业知识，概括的分析客户方在模板合同文本中增加内容对服务方有什么影响，100字内"

# CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
cot_template = """
"你是一名律师，根据你的专业知识，概括的分析客户方在模板合同文本中删减内容对服务方有什么影响，100字内"

示例1:
  人类："服务方中断惩罚一节中，增加文本: 服务年度内第三次及后续不达标 减免用户方电力保障未达标机柜当月服务费30%或提供等额服务； 减免用户方带宽保障未达标带宽产品当月服务费30%或提供合同到期后顺延一个月的服务； 按照该服务中断时间的3倍赔偿，赔偿执行方式为在服务期满后，免费顺延。
  AI：增加后的模板合同文本对服务方的影响主要包括以下几点：
  1. 服务不达标时，服务方需要减免用户方电力保障未达标机柜当月服务费30%或提供等额服务；
  2. 服务方还需减免用户方带宽保障未达标带宽产品当月服务费30%或提供合同到期后顺延一个月的服务；
  3. 服务方需要按照服务中断时间的3倍赔偿用户方。这些修改可能会对服务方的收入和经营造成一定影响，但同时也强调了服务方的责任。"

"""
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
system_prompt_role = SystemMessagePromptTemplate.from_template(role_template)
system_prompt_cot = SystemMessagePromptTemplate.from_template(cot_template)

human_input = """
在合同 设备的交接、合理使用及保管 一节中 增加文本:若用户方自行提供设备的，在用户方设备到达服务方指定地点时，服务方应当有专人在场进行签收
"""
# 用户的询问
human_template = "{human_input}"
human_prompt = HumanMessagePromptTemplate.from_template(human_template)

# 将以上所有信息结合为一个聊天提示
chat_prompt = ChatPromptTemplate.from_messages([system_prompt_role, system_prompt_cot, human_prompt])

prompt = chat_prompt.format_prompt(human_input=human_input).to_messages()

# 接收用户的询问，返回回答结果
response = llm(prompt)
print(response.content)