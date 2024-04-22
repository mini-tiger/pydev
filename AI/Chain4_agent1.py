import os

from langchain import OpenAI, PromptTemplate, LLMChain, SerpAPIWrapper, LLMMathChain
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.tools import Tool
import re,requests

import os

os.environ["OPENAI_API_KEY"] = 'EMPTY'
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0, openai_api_base="http://120.133.63.166:8003/v1")
# 谷歌搜索的Key
os.environ["SERPAPI_API_KEY"] = '310730e8cccf5e088ae50243cd37fdde7a769f80e46041abf0debb2cbcd5f5c4'




def three():
    """
    agents版：动态代理，实现自动选择计算工具
    :return:
    """
    # SerpApi是一个付费提供搜索结果API的第三方服务提供商。它允许用户通过简单的API调用访问各种搜索引擎的搜索结果，包括Google、Bing、Yahoo、Yandex等。
    # llm-math是langchain里面的能做数学计算的模块
    # tools = load_tools(["serpapi", "llm-math"], llm=llm)

    search = SerpAPIWrapper()
    llm_math_chain = LLMMathChain(llm=llm, verbose=True)

    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events"
        ),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="数学计算器"
        )
    ]

    # 初始化tools，models 和使用的agent
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,handle_parsing_errors=True)
    # 输出结果
    result = agent.run("你是人工智能吗?海湾战争距离现在多少年了? 这个数字的三次方是多少?")
    print(result)



if __name__ == '__main__':
    three()
    # four()