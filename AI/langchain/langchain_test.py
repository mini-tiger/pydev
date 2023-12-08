from langchain.chat_models import ChatOpenAI
from langchain.agents import tool
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.agents import AgentExecutor
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, ConversationKGMemory
import os
from langchain.chains import LLMChain
import openai
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory

from langchain.callbacks.base import BaseCallbackHandler
from typing import Dict, Any, Optional, List

# os.environ["OPENAI_API_KEY"] = 'your_openai_key'
# os.environ['OPENAI_API_BASE'] = ''

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", default="EMPTY")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", default="http://120.133.83.145:8000/v1")
OPENAI_PROXY = os.environ.get("OPENAI_PROXY", default="")

os.environ.setdefault("OPENAI_API_KEY", OPENAI_API_KEY)
os.environ.setdefault("OPENAI_API_BASE", OPENAI_API_BASE)

from langchain.document_loaders import UnstructuredFileLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI


def summery():
    llm = ChatOpenAI(
        openai_api_base=OPENAI_API_BASE,
        openai_api_key=OPENAI_API_KEY,
        openai_proxy=OPENAI_PROXY,
        temperature=0,
        # callbacks=[self.cb],
    )
    # 导入文本
    loader = UnstructuredFileLoader("data/lg_test.txt")
    # 将文本转成 Document 对象
    document = loader.load()
    print(f'documents:{len(document)}')

    # 初始化文本分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=0
    )

    # 切分文本
    split_documents = text_splitter.split_documents(document)
    print(f'documents:{len(split_documents)}')

    # 创建总结链
    chain = load_summarize_chain(llm, chain_type="refine", verbose=True)

    # 执行总结链，（为了快速演示，只总结前5段）
    chain.run(split_documents[:5])


from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

from langchain.prompts import ChatPromptTemplate
from langchain.chains.openai_functions import create_structured_output_chain


def json_output():
    llm = OpenAI(model_name="text-davinci-003")
    # 告诉他我们生成的内容需要哪些字段，每个字段类型式啥
    response_schemas = [
        ResponseSchema(name="bad_string", description="This a poorly formatted user input string"),
        ResponseSchema(name="good_string", description="This is your response, a reformatted response")
    ]

    # 初始化解析器
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    # 生成的格式提示符
    # {
    #	"bad_string": string  // This a poorly formatted user input string
    #	"good_string": string  // This is your response, a reformatted response
    # }
    format_instructions = output_parser.get_format_instructions()

    template = """
    You will be given a poorly formatted string from a user.
    Reformat it and make sure all the words are spelled correctly

    {format_instructions}

    % USER INPUT:
    {user_input}

    YOUR RESPONSE:
    """

    # 将我们的格式描述嵌入到 prompt 中去，告诉 llm 我们需要他输出什么样格式的内容
    prompt = PromptTemplate(
        input_variables=["user_input"],
        partial_variables={"format_instructions": format_instructions},
        template=template
    )

    promptValue = prompt.format(user_input="welcom to califonya!")

    llm_output = llm(promptValue)

    # 使用解析器进行解析生成的内容
    output_parser.parse(llm_output)
    print(llm_output)


from langchain.prompts.few_shot import FewShotPromptTemplate


def custom_tpl():
    prompt_template = """
    使用 [{new_str}] 替换下文中全部[{old_str}],输出替换后的文本
    -------------------
    {context}
    """
    # qa_chain_prompt = PromptTemplate.from_template(template=prompt_template)
    llm = ChatOpenAI(
        openai_api_base=OPENAI_API_BASE,
        openai_api_key=OPENAI_API_KEY,
        openai_proxy=OPENAI_PROXY,
        temperature=0,
        # callbacks=[self.cb],
    )
    # PROMPT = PromptTemplate(
    #     template=prompt_template, input_variables=["context", "old_str","new_str"]
    # )

#     memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
#
#     chain = RetrievalQA.from_chain_type(
#                 llm=llm,
#                 memory=memory,
#                 chain_type='stuff',
#                 retriever=retriever,
#                 verbose=True,
#                 chain_type_kwargs={
#                     "verbose": True,
#                     "prompt": PROMPT,
#                     "memory": ConversationBufferMemory(
#                         memory_key="history",
#                         input_key="question"),
#                 }
# )
#
#     result = chain.run(context="abcbcda", old_str="a", new_str="1")
#     print(result)

    from langchain.chains import LLMChain
    multiple_input_prompt = PromptTemplate(
        input_variables=["context", "old_str","new_str"],
        template=prompt_template
    )
    # multiple_input_prompt.format(personA="小张", thingsB="故事")
    chain = LLMChain(llm=llm, prompt=multiple_input_prompt)
    print(chain.run(context="abcbcda", old_str="a", new_str="1111"))

    #######
    template = """Tell me a {adjective} joke about {subject}."""
    prompt = PromptTemplate(
        template=template, input_variables=["adjective", "subject"]
    )
    # llm = OpenAI(temperature=0)
    memory = ConversationKGMemory(llm=llm, input_key="adjective")
    llm_chain = LLMChain(prompt=prompt, llm=OpenAI(temperature=0), memory=memory)

    print(llm_chain.predict(adjective="sad", subject="ducks"))
    print(memory)

def using_memory():
    from langchain.memory import ConversationKGMemory
    from langchain.llms import OpenAI
    llm = ChatOpenAI(
        openai_api_base=OPENAI_API_BASE,
        openai_api_key=OPENAI_API_KEY,
        openai_proxy=OPENAI_PROXY,
        temperature=0,
        # callbacks=[self.cb],
    )
    # memory = ConversationKGMemory(llm=llm, return_messages=True)
    # memory.save_context({"input": "say hi to sam"}, {"output": "who is sam"})
    # memory.save_context({"input": "sam is a friend"}, {"output": "okay"})
    # print(memory.load_memory_variables({"input": "who is sam"}))
    # print(memory.load_memory_variables({"input": "who is sam"}))
    # print(memory.get_current_entities("what's Sams favorite color?"))
    # print(memory.get_knowledge_triplets("her favorite color is red"))
    from langchain.chains import ConversationChain
    from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
    # 初始化对话链
    conversation = ConversationChain(
        llm=llm,
        memory=ConversationSummaryBufferMemory(
            llm=llm,
            max_token_limit=300
        )
    )

    # 第一天的对话
    # 回合1
    result = conversation("我姐姐明天要过生日，我需要一束生日花束。")
    print(result)
    # 回合2
    result = conversation("她喜欢粉色玫瑰，颜色是粉色的。")
    # print("\n第二次对话后的记忆:\n", conversation.memory.buffer)
    print(result)

    # 第二天的对话
    # 回合3
    result = conversation("我又来了，还记得我昨天为什么要来买花吗？")
    print(result)




if __name__ == "__main__":
    # json_output()
    # custom_tpl()
    using_memory()

