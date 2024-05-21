import os
os.environ["OPENAI_API_KEY"] = 'EMPTY'

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
from langchain.vectorstores import Qdrant
from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings import OpenAIEmbeddings,HuggingFaceEmbeddings
hm=HuggingFaceEmbeddings(model_name='/root/.cache/torch/exp_finetune/')


CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get("PGVECTOR_HOST", "172.22.50.25"),
    port=int(os.environ.get("PGVECTOR_PORT", "31867")),
    database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
    user=os.environ.get("PGVECTOR_USER", "test"),
    password=os.environ.get("PGVECTOR_PASSWORD", "test123"),
)

vectorstore = PGVector.from_documents(
    embedding=hm,
    documents=chunked_documents,
    collection_name="test_pgvector",
    connection_string=CONNECTION_STRING,
)


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

# 实例化一个MultiQueryRetriever
retriever_from_llm = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(), llm=llm)

# 实例化一个RetrievalQA链
qa_chain = RetrievalQA.from_chain_type(llm,retriever=retriever_from_llm)


if __name__ == "__main__":
    query="易速鲜花网站是什么"
    docs = retriever_from_llm.get_relevant_documents(query)


    prompts = []
    for doc in docs:
        prompts.append(doc.dict())
    print(111,prompts)
    prompts.append({"question": query})
    print(333,prompts)
    print(222,qa_chain.run({"query": query}))

    docs_with_score = vectorstore.similarity_search_with_score(query)
    for doc, score in docs_with_score:
        print("-" * 80)
        print("Score: ", score)
        print(doc.page_content)
        print("-" * 80)