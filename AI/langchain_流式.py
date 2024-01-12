from langchain.llms import OpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
os.environ["OPENAI_API_KEY"] = 'EMPTY'
# llm = OpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0,openai_api_base="http://120.133.83.145:8000/v1/chat/completions")

from langchain.schema import AIMessage, HumanMessage, SystemMessage


from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(streaming=True,temperature=0, callbacks=[StreamingStdOutCallbackHandler()], openai_api_base="http://120.133.83.145:8000/v1")
messages = [
    # SystemMessage(
    #     content="You are a helpful assistant that translates English to French."
    # ),
    HumanMessage(
        content="模仿李白的风格写一首唐诗"
    ),
]
resp = llm(messages)
print(resp.content)