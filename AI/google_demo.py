
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMRequestsChain, LLMChain
from langchain.chat_models import ChatOpenAI

import os
os.environ["http_proxy"] = "http://127.0.0.1:1081"
os.environ["https_proxy"] = "http://127.0.0.1:1081"
os.environ["OPENAI_API_KEY"] = 'EMPTY'
llm = ChatOpenAI(temperature=0,openai_api_base="http://120.133.83.145:8000/v1")

template = """在 >>> 和 > 之间 {requests_result} """
PROMPT=PromptTemplate.from_template(template)
chain = LLMRequestsChain(llm_chain=LLMChain(llm=llm, prompt=PROMPT))
question = "什么是三个最大的国家，以及它们各自的面积？"
inputs = {
    "query": question,
    "url": "https://www.google.com/search?q=" + question.replace(" ", "+"),
}
print(chain(inputs))
