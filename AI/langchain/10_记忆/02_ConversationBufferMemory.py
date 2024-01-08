'''欢迎来到LangChain实战课
https://time.geekbang.org/column/intro/100617601
作者 黄佳'''
# 设置OpenAI API密钥
import os
os.environ["OPENAI_API_KEY"] = 'Your Key'

# 导入所需的库
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory

import os
os.environ["OPENAI_API_KEY"] = 'EMPTY'

# 创建聊天模型
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature=0,openai_api_base="http://120.133.83.145:7860/v1")

memory=ConversationBufferMemory(memory_key="history",return_messages=False)
# 初始化对话链
conversation = ConversationChain(
    llm=llm,
    memory=memory
)
memory.clear()

# 第一天的对话
# 回合1
conversation("我姐姐明天要过生日，我需要一束生日花束。")
print("第一次对话后的记忆:", conversation.memory.buffer)
print(memory.to_json())
# 回合2
conversation("她喜欢粉色玫瑰，颜色是粉色的。")
print("第二次对话后的记忆:", conversation.memory.buffer)

# 回合3 （第二天的对话）
conversation("我又来了，还记得我昨天为什么要来买花吗？")
print("/n第三次对话后时提示:/n",conversation.prompt.template)
print("/n第三次对话后的记忆:/n", conversation.memory.buffer)
print(memory.to_json())
memory.clear()


conversation("我姐姐明天要过生日，我需要一束生日花束。")
print("第一一次对话后的记忆:", conversation.memory.buffer)

# 回合2
conversation("她喜欢粉色玫瑰，颜色是粉色的。")
print("第二二次对话后的记忆:", conversation.memory.buffer)

# 回合3 （第二天的对话）
conversation("我又来了，还记得我昨天为什么要来买花吗？")
print("/n第三三次对话后时提示:/n",conversation.prompt.template)
print("/n第三三次对话后的记忆:/n", conversation.memory.buffer)