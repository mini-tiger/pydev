
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,AIMessage
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import gradio as gr
from langchain.chat_models import ChatOpenAI

import os

os.environ["OPENAI_API_KEY"] = 'EMPTY'
llm = ChatOpenAI(temperature=0,openai_api_base="http://120.133.83.145:8000/v1")

#  os.envrion["OPENAI_API_KEY"] = ""  # Replace with your key

def predict(message, history):
    history_langchain_format = []
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=message))
    # gpt_response = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0,openai_api_key="...")
    gpt_response = llm
    resp = gpt_response(history_langchain_format)
    return resp.content

gr.ChatInterface(predict).launch(server_name="0.0.0.0", share=False)
