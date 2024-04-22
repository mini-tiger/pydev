import os

from langchain import OpenAI, PromptTemplate, LLMChain, SerpAPIWrapper, LLMMathChain
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.tools import Tool
import re,requests

import os

os.environ["OPENAI_API_KEY"] = 'EMPTY'
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0, openai_api_base="http://120.133.63.166:8000/v1")
# 谷歌搜索的Key
os.environ["SERPAPI_API_KEY"] = '310730e8cccf5e088ae50243cd37fdde7a769f80e46041abf0debb2cbcd5f5c4'

def one():
    """
    基础版：输入整个语义
    :return:
    """
    text = "对于一家生产彩色袜子的公司来说，什么是好的公司名称？"
    result = llm(text)
    print(result)


def two():
    """
    prompt版本：提前定义好语义，输入关键词即可
    :return:
    """
    prompt = PromptTemplate(input_variables=["product"],
                            template="对于一家生产{product}的公司来说，什么是好的公司名称？")

    chain = LLMChain(llm=llm, prompt=prompt)

    # 这样我们只需要输入产品名称即可
    result = chain.run("杨梅")
    print(result)


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
            name="username",
            func=search.run,
            description="Name extraction tool"
        ),
        # Tool(
        #     name="Calculator",
        #     func=llm_math_chain.run,
        #     description="useful for when you need to answer questions about math"
        # )
    ]

    # 初始化tools，models 和使用的agent
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    # 输出结果
    result = agent.run("你是人工智能吗？海湾战争距离现在多少年了? 这个数字的三次方是多少?")
    print(result)

from langchain.tools import BaseTool, DuckDuckGoSearchRun
# 计算工具
class CalculatorTool(BaseTool):
    name = "Calculator"
    description = "如果问数学相关问题时，使用这个工具"
    return_direct = False  # 直接返回结果

    def _run(self, query: str) -> str:
        return eval(query)

class Extract_DataCenter(BaseTool):
    name = "Extract_Datacenter"
    description = "如果问上架率相关问题时，使用这个工具"
    return_direct = True  # 直接返回结果

    def _run(self, input: str) -> str:
        # 使用正则表达式提取目标部分
        match = re.search(r'(.+?)数据中心', input)
        # logger.debug(input)
        if match:
            extracted_part = match.group(1)
            # print("提取的部分:", extracted_part + "数据中心")

            r=requests.get(f"http://172.22.50.25:31857/dc/usage?dc_area={extracted_part}")

            return  f"截止到{r.json()['start_date']}日,{r.json()['datacenter_name']}上架率:{r.json()['usage_rate']}"
        return ""
def four():
    """
    agents版：动态代理，实现自动选择计算工具
    :return:
    """
    # SerpApi是一个付费提供搜索结果API的第三方服务提供商。它允许用户通过简单的API调用访问各种搜索引擎的搜索结果，包括Google、Bing、Yahoo、Yandex等。
    # llm-math是langchain里面的能做数学计算的模块
    # tools = load_tools(["serpapi", "llm-math"], llm=llm)

    # search = SerpAPIWrapper()
    # llm_math_chain = LLMMathChain(llm=llm, verbose=True)

    tools = [
        Tool(
            name="Shelf rate",
            func=Extract_DataCenter.run,
            description="Useful when you need to answer questions about shelf rates"
        ),
        Tool(
            name="Calculator",
            func=CalculatorTool.run,
            description="useful for when you need to answer questions about math"
        )
    ]

    # 初始化tools，models 和使用的agent
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    # 输出结果
    result = agent.run("上海外高桥数据中心的上架率?")
    print(result)



if __name__ == '__main__':
    three()
    # four()