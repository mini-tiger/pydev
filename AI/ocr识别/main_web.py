from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional

from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from Chain3_prompt import llm, llm_resp_rule
from neo4j_conn import uri, username, password
from neo4j_query import process_question
from loguru import logger

# 初始化LangChain中的Neo4j图对象和QA链


# 初始化FastAPI应用
app = FastAPI()


class QueryRequest(BaseModel):
    question: str

'''
程亮参与的项目投资总和
统计侯宇2022，2023年分别参与的项目投资数额
分别统计2022，2023年项目投资数额
'''
@app.api_route("/query", methods=["GET", "POST"])
async def query_neo4j(request: QueryRequest):
    print(request.question)

    # cypher_query, data_valid, data_dict, process_valid ,step = process_question(question=request.question)
    # logger.info(f"EXEC CQL process_valid: {process_valid},data_valid: {data_valid},data_dict: {data_dict},")
    process_valid=False
    data_valid= False
    if process_valid == False or data_valid == False:
        step = 4
        graph = Neo4jGraph(url=uri, username=username, password=password,
                           driver_config={"max_connection_lifetime": 500})
        chain = GraphCypherQAChain.from_llm(llm=llm, graph=graph, verbose=True,
                                            return_intermediate_steps=True)  # 确保返回中间步骤)
        # res = chain.run(request.question)
        res = chain({"query": request.question})
        resp = llm_resp_rule(res) # 重新llm
        print(res['intermediate_steps'])
        if resp is not None:
            res = resp
            return {"step": {"cql": res['intermediate_steps'][0]["query"], "process_valid": process_valid,"step":step},"result": res}
        return {"step": {"cql": res['intermediate_steps'][0]["query"], "process_valid": process_valid,"step":step},"result": res['intermediate_steps'][-1]['context']}
    else:
        return {"step": {"cql": cypher_query, "process_valid": process_valid,"step":step}, "result": data_dict}


# 运行FastAPI应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8006)
