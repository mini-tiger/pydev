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

llm = ChatOpenAI(temperature=0, openai_api_base="http://120.133.63.166:8007/v1")

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
    base_dir = '.'  # 文档的存放目录
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
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=10,
                                                   # separators=["\n\n", "\n", "。", ".", ""]
                                                   separators=["\n", '\n\n', "。"],
                                                   is_separator_regex=True
                                                   )
    chunked_documents = text_splitter.split_documents(documents)
    print(chunked_documents)
    print(len(chunked_documents))
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

    query="乙方负责按本合同和个别合同规定的条件提供相关服务或设施，供甲方放置设备及使用；乙方提供的机房及相关设施产权仍归乙方所有。"
    # query= "5.	如果乙方提供的发票不符合甲方要求，甲方有权拒绝支付，并从个别合同的服务费用中扣减相应费用。 "
    docs = retriever_from_llm.get_relevant_documents(query)
    prompts = []
    for doc in docs:
        prompts.append(doc.dict()['page_content'])
    # print("==============prompts append 向量匹配结果================")
    # print(''.join(prompts))

    # 创建聊天模型
    from langchain.chat_models import ChatOpenAI



    # 设定 AI 的角色和目标
    # role_template = "你是一个为花店电商公司工作的AI助手, 你的目标是帮助客户根据他们的喜好做出明智的决定"

    # CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
    from string import Template


    from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate


    # 用户的询问
    human_template = "{human_input}"
    human_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # 将以上所有信息结合为一个聊天提示
    chat_prompt = ChatPromptTemplate.from_messages([human_prompt])  #
    human_input = '''服务方为出租方，对比模板条款和现有条款，推理现有条款对服务方(乙方)是否产生了风险,只返回xml格式,例如$ex
-----------------------
模板条款:
$muban
-----------------------
现有条款:
$now'''
    d = {"ex": "<harm>True</harm><detail>''</detail>",
         "muban":''.join(prompts),"now":query}

    tt1 = Template(human_input)
    human = tt1.substitute(d)
    print(human)

    prompt = chat_prompt.format_prompt(human_input=human).to_messages()

    # 接收用户的询问，返回回答结果
    response = llm(prompt, stream=True)
    print(response)

