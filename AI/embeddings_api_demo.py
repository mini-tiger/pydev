from langchain_openai import OpenAIEmbeddings
import os
os.environ["OPENAI_API_KEY"] = 'EMPTY'
embeddings_model = OpenAIEmbeddings(openai_api_base="http://120.133.63.166:9027/v1",model="bge-base-zh-v1.5")

embeddings = embeddings_model.embed_documents(
    [
        "Hi there!",
        "Oh, hello!",
        "What's your name?",
        "My friends call me World",
        "Hello World!"
    ]
)
# 打印向量数量和第一个文本向量的长度
print(len(embeddings), len(embeddings[0]))
embedded_query = embeddings_model.embed_query("What was the name mentioned in the conversation?")
print(embedded_query)