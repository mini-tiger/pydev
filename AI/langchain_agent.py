from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents.agent_types import AgentType

# initialize LLM (we use ChatOpenAI because we'll later define a `chat` agent)
import os

os.environ["OPENAI_API_KEY"] = 'EMPTY'
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0, openai_api_base="http://120.133.63.166:8000/v1")

# initialize conversational memory
conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True
)

from langchain.tools import BaseTool
from math import pi
from typing import Union


class CircumferenceTool(BaseTool):
    name = "Circumference calculator"
    description = "use this tool when you need to calculate a circumference using the radius of a circle"


    def _run(self, radius: Union[int, float,str]):

        if isinstance(radius,str):
            radius=float(radius.replace("\n",""))
        return f"{radius * 2.0 * pi}"


    def _arun(self, radius: int):
        raise NotImplementedError("This tool does not support async")

from langchain.agents import initialize_agent

tools = [CircumferenceTool()]

# initialize agent with tools
agent = initialize_agent(
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=conversational_memory
)
agent("can you calculate the circumference of a circle that has a radius of 7.81mm")


from langchain_core.messages import AIMessage, HumanMessage
from langchain import hub
from langchain.agents import AgentExecutor, create_json_chat_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
# Create an agent executor by passing in the agent and tools
from langchain.memory import ConversationBufferMemory,ConversationBufferWindowMemory,Conver
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)
agent_executor.invoke(
    {
        "input": "what's my name?",
        "chat_history": [
            HumanMessage(content="hi! my name is bob"),
            AIMessage(content="Hello Bob! How can I assist you today?"),
        ],
    }
)