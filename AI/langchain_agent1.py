import requests
from langchain.tools import BaseTool, DuckDuckGoSearchRun
import re,json
from langchain.globals import set_debug,set_verbose

set_debug(True)
set_verbose(True)

import logging
import sys
# 创建日志器logger并将其日志级别设置为DEBUG
logger = logging.getLogger("python_config_logger")
logger.setLevel(logging.DEBUG)
# 创建一个流处理器handler并将其日志级别设置为DEBUG
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
# 创建一个格式化器formatter并将其添加到处理器handler中
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
# 为日志器logger添加上面创建好的处理器handler
logger.addHandler(handler)
# 将日志打印在控制台
logger.debug('打印日志级别：debug')

# 搜索工具
class SearchTool(BaseTool):
    name = "Search"
    description = "当问电影相关问题时候，使用这个工具"
    return_direct = False  # 直接返回结果

    def _run(self, query: str) -> str:
        print("\n正在调用搜索引擎执行查询: " + query)
        search = DuckDuckGoSearchRun()
        return search.run(query)

# 计算工具
class CalculatorTool(BaseTool):
    name = "Calculator"
    description = "如果问数学相关问题时，使用这个工具"
    return_direct = False  # 直接返回结果

    def _run(self, query: str) -> str:
        return eval(query)


# 计算工具
class Extract_DataCenter(BaseTool):
    name = "Extract_Datacenter"
    description = "如果问上架率相关问题时，使用这个工具"
    return_direct = True  # 直接返回结果

    def _run(self, input: str) -> str:
        # 使用正则表达式提取目标部分
        match = re.search(r'(.+?)数据中心', input)
        logger.debug(input)
        if match:
            extracted_part = match.group(1)
            # print("提取的部分:", extracted_part + "数据中心")

            r=requests.get(f"http://172.22.50.25:31857/dc/usage?dc_area={extracted_part}")

            return  f"截止到{r.json()['start_date']}日,{r.json()['datacenter_name']}上架率:{r.json()['usage_rate']}"
        return ""

from typing import Dict, Union, Any, List

from langchain.output_parsers.json import parse_json_markdown
from langchain.agents.conversational_chat.prompt import FORMAT_INSTRUCTIONS
from langchain.agents import AgentExecutor, AgentOutputParser
from langchain.schema import AgentAction, AgentFinish


# 自定义解析类
class CustomOutputParser(AgentOutputParser):

    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        print(text)
        cleaned_output = text.strip()
        # 定义匹配正则
        action_pattern = r'"action":\s*"([^"]*)"'
        action_input_pattern = r'"action_input":\s*"([^"]*)"'
        # 提取出匹配到的action值
        action = re.search(action_pattern, cleaned_output)
        action_input = re.search(action_input_pattern, cleaned_output)
        if action:
            action_value = action.group(1)
        if action_input:
            action_input_value = action_input.group(1)

        # 如果遇到'Final Answer'，则判断为本次提问的最终答案了
        if action_value and action_input_value:
            if action_value == "Final Answer":
                return AgentFinish({"output": action_input_value}, text)
            else:
                return AgentAction(action_value, action_input_value, text)

        # 如果声明的正则未匹配到，则用json格式进行匹配
        response = parse_json_markdown(text)

        action_value = response["action"]
        action_input_value = response["action_input"]
        if action_value == "Final Answer":
            return AgentFinish({"output": action_input_value}, text)
        else:
            return AgentAction(action_value, action_input_value, text)


output_parser = CustomOutputParser()
from langchain.memory import ConversationBufferMemory
from langchain.agents.conversational_chat.base import ConversationalChatAgent
from langchain.agents import AgentExecutor, AgentOutputParser

SYSTEM_MESSAGE_PREFIX = """尽可能用中文回答以下问题。您可以使用以下工具"""

# 初始化大模型实例，可以是本地部署的，也可是是ChatGPT
# llm = ChatGLM(endpoint_url="http://你本地的实例地址")
import os

os.environ["OPENAI_API_KEY"] = 'EMPTY'
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0, openai_api_base="http://120.133.83.145:8000/v1")
# 初始化工具
tools = [ Extract_DataCenter(),CalculatorTool(),SearchTool()]
# tools = [Extract_DataCenter()]
# 初始化对话存储，保存上下文

from langchain.memory import ConversationBufferWindowMemory

# 创建一个对话缓存的窗口（k=1）
memory = ConversationBufferWindowMemory(k=5,memory_key="chat_history", return_messages=True)

# 连续两次添加对话内容
memory.save_context({"input": "数据中心有哪些"},
                    {"output": "上海外高桥数据中心,上海荷丹数据中心"})

# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 配置agent
chat_agent = ConversationalChatAgent.from_llm_and_tools(
    system_message=SYSTEM_MESSAGE_PREFIX, # 指定提示词前缀
    llm=llm, tools=tools,
    memory=memory,
    verbose=True, # 是否打印调试日志，方便查看每个环节执行情况
    output_parser=output_parser #
)
agent = AgentExecutor.from_agent_and_tools(
    agent=chat_agent, tools=tools, memory=memory, verbose=True,
    max_iterations=3 # 设置大模型循环最大次数，防止无限循环
)

# agent.run("奥本海默的导演是谁")
agent.run("上海外高桥数据中心的上架率")
agent.run("55 乘以 55 是多少")

