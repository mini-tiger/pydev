import os,re
os.environ["OPENAI_API_KEY"] = 'EMPTY'
os.environ['HTTP_PROXY']='http://localhost:1081'
os.environ['HTTPS_PROXY']='http://localhost:1081'
# from langchain.globals import set_debug,set_verbose
#
# set_debug(True)
# set_verbose(True)
def replace_str(original_string):
    tstr= original_string.replace(' ', '').replace('\t', '').\
        replace('【', '[').replace('】', ']').replace('\n','').replace('\r','').\
        replace('：', ':').replace("（", "(").replace("）", ")").replace('\r\n','')
    new_str1=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]',"", tstr)
    new_str = re.sub(r'[\n\r]', ' ',new_str1 )
    return new_str

from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0, openai_api_base="http://120.133.63.166:8001/v1")

# 1.Load 导入Document Loaders
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings,HuggingFaceEmbeddings
hm=HuggingFaceEmbeddings(model_name='moka-ai/m3e-base')

save_file="faiss_index"

if os.path.exists(save_file):
    vectorstore = FAISS.load_local(save_file, hm)
else:
    # 加载Documents
    base_dir = './langchain/02_文档QA系统/OneFlower'  # 文档的存放目录
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
    vectorstore = FAISS.from_documents(chunked_documents, hm)
    vectorstore.save_local(save_file)


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
    # delete function
    # https://blog.csdn.net/weixin_57028107/article/details/132214687
    # init_delete_vector=vectorstore.as_retriever(search_kwargs={"filter": {"source": "./langchain/02_文档QA系统/OneFlower/易速鲜花运营指南.docx"}})
    #
    # del_doc=init_delete_vector.get_relevant_documents('')
    # print(del_doc)
    # 实例化一个MultiQueryRetriever
    retriever_from_llm = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(), llm=llm)
    # vectorstore.delete()
    # 实例化一个RetrievalQA链
    qa_chain = RetrievalQA.from_chain_type(llm, return_source_documents=True,retriever=retriever_from_llm)

    query="易速鲜花网站是什么"
    docs = retriever_from_llm.get_relevant_documents(query)
    prompts = []
    for doc in docs:
        prompts.append(doc.dict())
    print("==============prompts append 向量匹配结果================")
    # print(prompts)



    qa_result = qa_chain(query)
    source_list = []
    context_list = []
    result = qa_result['result']
    print(result)
    for i in qa_result['source_documents']:
        # print(i.metadata['source'])
        source_list.append(i.metadata['source'])
        # print(i.page_content)
        context_list.append(i.page_content)
    print(source_list)
    print(context_list)
    # prompts.append({"question": query})
    # print("answer",qa_chain.run({"query": query}))
    # print("answer1",qa_chain.run({"query":"网站项目的实施分为四大阶段?"}))

