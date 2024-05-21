import os
os.environ["OPENAI_API_KEY"] = 'EMPTY'
from langchain.globals import set_debug,set_verbose

set_debug(True)
set_verbose(True)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0, openai_api_base="http://120.133.83.145:8000/v1")

# 1.Load 导入Document Loaders
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader

# 加载Documents
base_dir = './OneFlower'  # 文档的存放目录
documents = []
for file in os.listdir(base_dir): 
    # 构建完整的文件路径
    file_path = os.path.join(base_dir, file)
    if file.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())
    elif file.endswith('.docx'):
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
from langchain.vectorstores import Qdrant,pgvector
from langchain.embeddings import OpenAIEmbeddings,HuggingFaceEmbeddings
hm=HuggingFaceEmbeddings(model_name='/root/.cache/torch/exp_finetune/')
vectorstore = Qdrant.from_documents(
    documents=chunked_documents, # 以分块的文档
    # embedding=OpenAIEmbeddings(), # 用OpenAI的Embedding Model做嵌入
    embedding=hm,
    location=":memory:",  # in-memory 存储
    collection_name="my_documents",) # 指定collection_name

# 4. Retrieval 准备模型和Retrieval链
import logging # 导入Logging工具
from langchain.chat_models import ChatOpenAI # ChatOpenAI模型
from langchain.retrievers.multi_query import MultiQueryRetriever # MultiQueryRetriever工具
from langchain.chains import RetrievalQA # RetrievalQA链

# 设置Logging
logging.basicConfig()
logging.getLogger('langchain.retrievers.multi_query').setLevel(logging.INFO)

# 实例化一个大模型工具 - OpenAI的GPT-3.5
# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)




if __name__ == "__main__":
    # 实例化一个MultiQueryRetriever
    retriever_from_llm = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(), llm=llm)

    # 实例化一个RetrievalQA链
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever_from_llm)

    query="易速鲜花网站是什么"
    docs = retriever_from_llm.get_relevant_documents(query)
    prompts = []
    for doc in docs:
        prompts.append(doc.dict())
    print("==============prompts append 向量匹配结果================")
    # print(prompts)
    # print(prompts)
    for p in prompts:
        print(f"{p['page_content']}")
        # print(p)

    prompts.append({"question": query})
    print(222,qa_chain.run({"query": query}))
