'''欢迎来到LangChain实战课
https://time.geekbang.org/column/intro/100617601
作者 黄佳'''

import os

# 1.Load 导入Document Loaders
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
import os
from tools.minio_tool import minio_process
from tools.utils import mkdir, removedir

current_directory = os.path.dirname(__file__)
src_dir = os.path.join(current_directory, "tmp_langchain")
removedir(src_dir)
mkdir(src_dir)

m = minio_process(minio_server="172.22.50.25:31088",  # MinIO服务器的URL
                  access_key="hlEPG0SuaiBys2Hd",  # 您的访问密钥
                  secret_key="OiQdBT8XI1O68F6Z3QQbUJl4LzkYR3dw")  # 您的秘密密钥)

# 2
m.download_folder(local_path=src_dir, prefix="IDC文本",
                  bucket_name="test")

# 加载Documents
base_dir = src_dir
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



#
if __name__ == "__main__":
    query="外高桥数据中心的地址？"
    docs = retriever_from_llm.get_relevant_documents(query)


    prompts = []
    for doc in docs:
        prompts.append(doc.dict())
    print(111,prompts)
    prompts.append({"question": query})
    print(333,prompts)
    print(222,qa_chain.run({"query": query}))
#     app.run(host='0.0.0.0',debug=True,port=5000)
