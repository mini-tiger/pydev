'''欢迎来到LangChain实战课
https://time.geekbang.org/column/intro/100617601
作者 黄佳'''

import os

# 1.Load 导入Document Loaders
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader

# 加载Documents
from langchain_core.prompts import PromptTemplate

base_dir = './OneFlower'  # 文档的存放目录
documents = []
for file in os.listdir(base_dir):
    # 构建完整的文件路径
    file_path = os.path.join(base_dir, file)
    if file.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())
    elif file.endswith('.docx') or file.endswith('.doc'):
        loader = Docx2txtLoader(file_path)
        documents.extend(loader.load())
    elif file.endswith('.txt'):
        loader = TextLoader(file_path)
        documents.extend(loader.load())

# 2.Split 将Documents切分成块以便后续进行嵌入和向量存储
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=10)
chunked_documents = text_splitter.split_documents(documents)

# 3.Store 将分割嵌入并存储在矢量数据库Qdrant中
from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings,HuggingFaceEmbeddings


hm=HuggingFaceEmbeddings(model_name='/root/.cache/torch/exp_finetune/')

vectorstore = Qdrant.from_documents(
    documents=chunked_documents,  # 以分块的文档
    embedding=hm,  # 用OpenAI的Embedding Model做嵌入
    location=":memory:",  # in-memory 存储
    collection_name="my_documents", )  # 指定collection_name

# 4. Retrieval 准备模型和Retrieval链
import logging  # 导入Logging工具
from langchain.chat_models import ChatOpenAI  # ChatOpenAI模型
from langchain.retrievers.multi_query import MultiQueryRetriever  # MultiQueryRetriever工具
from langchain.chains import RetrievalQA  # RetrievalQA链

# 设置Logging
logging.basicConfig()
logging.getLogger('langchain.retrievers.multi_query').setLevel(logging.INFO)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", default="EMPTY")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", default="http://120.133.83.145:8000/v1")
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
    # callbacks=[self.cb],
)
# 实例化一个MultiQueryRetriever
retriever_from_llm = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(), llm=llm)





# 实例化一个RetrievalQA链
qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever_from_llm)



# # 5. Output 问答系统的UI实现
# from flask import Flask, request, render_template
# app = Flask(__name__) # Flask APP
#
# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#
#         # 接收用户输入作为问题
#         question = request.form.get('question')
#
#         # RetrievalQA链 - 读入问题，生成答案
#         result = qa_chain({"query": question})
#
#         # 把大模型的回答结果返回网页进行渲染
#         return render_template('index.html', result=result)
#
#     return render_template('index.html')
#
if __name__ == "__main__":
    query="易速鲜花网站是什么"
    docs = retriever_from_llm.get_relevant_documents(query)

    prompt_template = """请基于```内的内容回答问题。"

        ```

        {context}

        ```

        我的问题是：{question}。

    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    kc = RetrievalQA.from_llm(llm=llm, retriever=vectorstore.as_retriever(), prompt=prompt)
    print(kc.retriever.get_relevant_documents(query))


    prompts = []
    for doc in docs:
        prompts.append(doc.dict())
    print(111,prompts)
    prompts.append({"question": query})
    print(333,prompts)
    print(222,qa_chain.run({"query": query}))
#     app.run(host='0.0.0.0',debug=True,port=5000)
