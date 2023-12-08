
from langchain.agents import Tool
from langchain.tools import BaseTool
from math import pi
from typing import Union
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chains import LLMMathChain
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel,Field
llm = ChatOpenAI(
    openai_api_base="http://120.133.83.145:8000/v1", # http://120.133.83.145:8000/v1/chat/completions
    openai_api_key="EMPTY",
    # openai_proxy=current_app.config["OPENAI_PROXY"],
    temperature=0,
)
from langchain.agents import load_tools
from langchain.agents import Tool
from langchain.tools import BaseTool
from math import pi
from typing import Union
from langchain.agents import initialize_agent
from langchain.agents import AgentType
import os
from langchain.chat_models import ChatOpenAI



class CustomTool(BaseTool):
    name = "Temperature Detector"
    description = "This is a custom tool for my temperature detection use case"

    def _run(self, input: str) -> str:
        # Your logic here
        return "temperature is not bad,huh,20 celceius"

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")


class Robotic_Control(BaseTool):
    name = "Robotic Arm Control"
    description = "This is a custom tool for my Robotic Arm Control"

    def _run(self, input: str) -> str:
        # Your logic here
        return "Working "

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")


tools = [CustomTool(), Robotic_Control()]

# agent = initialize_agent(tools, agent=AgentType.DEFAULT)
agent = initialize_agent(tools,
                         llm,
                         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                         verbose=True)

agent("How's the temperature and Robotic Arm Control")

