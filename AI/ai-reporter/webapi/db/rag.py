# from webapi.db.vector import get_documents
import json, requests
import webapi.config as config
# from webapi.db.vector import *
from webapi.log.setup import logger
from webapi.utils.tools import RunError
# def vector_generator_with_langchain(vectorstore, query, url):
#     # txt_list, _ = get_documents(vectorstore, query=query, limit=3)
#     # txt_str_list = [i.get('page_content') for i in txt_list]
#     # txt = '\n'.join(txt_str_list)
#     # source_str_list = [i.get('metadata').get('source') for i in txt_list]
#     # source = ','.join(set(source_str_list))
#     # print("txt:",txt)
#     # print("source:",source)
#     result, err = retrievalQA_with_langchain(vectorstore, query, url)
#     if err is not None:
#         raise err
#     return result, None
#

def vector_generator_with_gouos(query):
    url = config.BaseConfig.GPUOS_PLATFORM_URL

    payload = json.dumps({
        "assistant_id": "4df33138f1524b91837a324ebf3b2633",
        "chat_id": "test001",
        "stream": False,
        "detail": True,
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, timeout=300)
        logger.warning(f"RAG response.status_code:{response.status_code}")
    except Exception as e:
        logger.error(f"request RAG query: {query} err:{str(e)}")
        return {"context_source": '', "context": '',
            'vectorstore_search_result': ''}, e

    if response.status_code == 200:
        data = response.json()

        if 'choices' in data and data['choices']:
            content = data['choices'][0]['message']['content']
            # 提取quoteList中的q和sourceName
            q_list = [item['q'] for item in data['responseData'][0]['quoteList']]
            source_name_list = [item['sourceName'] for item in data['responseData'][0]['quoteList']
                                if item['score'][0]['value'] > float(config.BaseConfig.SCORE)]
            logger.warning(f"quotoList:{data['responseData'][0]['quoteList']}")
        else:
            logger.error(f"request RAG query : {query} , error: GPUOS 未找到有效的返回内容")
            raise RunError( "GPUOS 未找到有效的返回内容")
    else:
        logger.error(f"request RAG query : {query} , error: GPUOS 请求错误，状态码：{response.status_code}")
        raise RunError(f"GPUOS 请求错误，状态码：{response.status_code}")

    return {"context_source": ','.join(set(source_name_list)), "context": content,
            'vectorstore_search_result': '\n'.join(q_list)}, None
