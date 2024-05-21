from langchain.llms import Ollama
import os
from crewai import Agent, Task, Crew, Process
os.environ["OPENAI_API_KEY"] = 'EMPTY'
from langchain.chat_models import ChatOpenAI
# 谷歌搜索的Key
os.environ["SERPAPI_API_KEY"] = '310730e8cccf5e088ae50243cd37fdde7a769f80e46041abf0debb2cbcd5f5c4'
from langchain.tools import Tool
llm = ChatOpenAI(temperature=0, openai_api_base="http://120.133.83.145:8000/v1")

ollama_openhermes = Ollama(model="agent")
# Pass Ollama Model to Agents: When creating your agents within the CrewAI framework, you can pass the Ollama model as an argument to the Agent constructor. For instance:
from langchain import OpenAI, PromptTemplate, LLMChain, SerpAPIWrapper, LLMMathChain
search = SerpAPIWrapper()

local_expert = Agent(
  role='Local Expert at this city',
  goal='Provide the BEST insights about the selected city',
  backstory="""A knowledgeable local guide with extensive information
  about the city, it's attractions and customs""",
  tools=[
    search,

  ],
  llm=ollama_openhermes, # Ollama model passed here
  verbose=True
)

print(local_expert.json())