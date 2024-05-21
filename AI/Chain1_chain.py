from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
import os
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", default="EMPTY")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", default="http://120.133.83.145:9116/v1")
OPENAI_PROXY = os.environ.get("OPENAI_PROXY", default="")

os.environ.setdefault("OPENAI_API_KEY", OPENAI_API_KEY)
os.environ.setdefault("OPENAI_API_BASE", OPENAI_API_BASE)

# 实例化一个大模型工具 - OpenAI的GPT-3.5
# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
llm = ChatOpenAI(
    openai_api_base=OPENAI_API_BASE,
    openai_api_key=OPENAI_API_KEY,
    openai_proxy=OPENAI_PROXY,
    temperature=0,
    max_tokens=2048
    # callbacks=[self.cb],
)


template = """
Step1 :

I have a problem related to {input}. Could you brainstorm three distinct solutions? Please consider a variety of factors such as {perfect_factors}
A:
"""

prompt = PromptTemplate(
    input_variables=["input", "perfect_factors"],
    template=template
)

chain1 = LLMChain(
    llm=llm,
    prompt=prompt,
    output_key="solutions"
)

template = """
Step 2:

For each of the three proposed solutions, evaluate their potential. Consider their pros and cons, initial effort needed, implementation difficulty, potential challenges, and the expected outcomes. Assign a probability of success and a confidence level to each option based on these factors

{solutions}

A:"""

prompt = PromptTemplate(
    input_variables=["solutions"],
    template=template
)

chain2 = LLMChain(
    llm=llm,
    prompt=prompt,
    output_key="review"
)

template = """
Step 3:

For each solution, deepen the thought process. Generate potential scenarios, strategies for implementation, any necessary partnerships or resources, and how potential obstacles might be overcome. Also, consider any potential unexpected outcomes and how they might be handled.

{review}
"""

prompt = PromptTemplate(
    input_variables=["review"],
    template=template
)

chain3 = LLMChain(
    llm=llm,
    prompt=prompt,
    output_key="deepen_thought_process"
)

template = """
Step 4:

Based on the evaluations and scenarios, rank the solutions in order of promise. Provide a justification for each ranking and offer any final thoughts or considerations for each solution
{deepen_thought_process}

A:"""

prompt = PromptTemplate(
    input_variables=["deepen_thought_process"],
    template=template
)

chain4 = LLMChain(
    llm=llm,
    prompt=prompt,
    output_key="ranked_solutions"
)

template = """
Step 5:
以下翻译成中文
——————————————
{ranked_solutions}

"""

prompt = PromptTemplate(
    input_variables=["ranked_solutions"],
    template=template
)

chain5 = LLMChain(
    llm=llm,
    prompt=prompt,
    output_key="chinese_transfer"
)

from langchain.chains import SequentialChain

overall_chain = SequentialChain(
    chains=[chain1, chain2, chain3, chain4,chain5],
    input_variables=["input", "perfect_factors"],
    output_variables=["chinese_transfer"],
    verbose=True
)

print(overall_chain({"input":"human colonization of Mars", "perfect_factors":"The distance between Earth and Mars is very large, making regular resupply difficult"}))