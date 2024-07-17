from langchain.prompts import PromptTemplate
from loguru import logger
from langchain_core.globals import set_verbose, set_debug

# Disable verbose logging
set_verbose(True)
# Disable debug logging
set_debug(False)

from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
import pandas as pd
import os
import config
from neo4j_conn import New_conn_neo4j

os.environ["OPENAI_API_KEY"] = 'EMPTY'
# 初始化 OpenAI 语言模型
llm = ChatOpenAI(temperature=0, openai_api_base=config.BaseConfig.openai_base, model="Qwen1.5-72B-Chat")

# 定义数据库结构信息
database_schema = """
Node labels and properties:
1. Personnel
   - name: string
   - title: string
2. Report
   - year: int 
   - report_number: string
   - project_name: string
   - project_field: string
   - investment_amount: float
   - investment_amount_unit: string
   - region: string

Relationship types:
1. WORKS_ON: (Personnel)-[WORKS_ON]->(Report)

"""

# 创建一个包含数据库结构的提示模板
template = """
你是一个专门生成 Neo4j Cypher 查询的 AI 助手。
根据以下问题和给定的数据库结构，生成一个适当的 Cypher 查询语句,注意事项:
1. 必须使用模糊查询
2. Relationship: Personnel works_on Report
只返回 Cypher 查询语句，不要包含任何其他解释或上下文。

数据库结构：
{schema}

问题: {question}

Cypher 查询:
"""

prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template=template
)


# 创建 LLMChain
# chain = LLMChain(llm=llm, prompt=prompt)
# 函数：根据问题和数据库结构生成 Cypher 查询
# def generate_cypher_query(question):
#     return chain.run(schema=database_schema, question=question)

def generate_cypher_query(question):
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"schema": database_schema, "question": question})


def exec_cypher_query(cypher_query):
    neo4j_conn = New_conn_neo4j()
    return neo4j_conn.run_query(cypher_query)


def is_valid_for_echarts(data):
    if not isinstance(data, dict):
        print("Data is not a dictionary.")
        return False

    # 获取所有列名
    keys = list(data.keys())

    # 检查所有值是否为列表
    for key in keys:
        if not isinstance(data[key], list):
            print(f"Value for key '{key}' is not a list.")
            return False

    # 检查所有列表的长度是否相同
    lengths = [len(data[key]) for key in keys]
    if len(set(lengths)) != 1:
        print("Not all lists have the same length.")
        return False

    # 初始化标志位，检查是否至少有一项是数字类型
    has_numeric = False

    # 检查每个列表的内容类型是否适合可视化
    for key in keys:
        for item in data[key]:
            if isinstance(item, (int, float)):
                has_numeric = True
            elif isinstance(item, str):
                try:
                    # 尝试将字符串转换为浮点数
                    float(item)  # 尝试转换成浮点数
                    has_numeric = True
                except ValueError:
                    # print(f"List for key '{key}' contains invalid data types: {item}")
                    continue
            else:
                # print(f"List for key '{key}' contains invalid data types: {item}")
                continue

    if not has_numeric:
        print("Data does not contain any numeric values.")
        return False

    # 如果所有检查都通过，数据格式有效
    return True


def convert_to_pd(result):
    # 获取列名（假设所有记录都有相同的字段）
    data_dict = {}
    if result:
        columns = result[0].keys()
        # 获取所有记录的值
        records = [record.values() for record in result]
        # 将结果转换为DataFrame
        df = pd.DataFrame(records, columns=columns)

        # 转换为字典格式
        data_dict = df.to_dict(orient='list')
        # print(data_dict)
        return data_dict, is_valid_for_echarts(data_dict)
    else:
        # print("No data returned from query.")
        return data_dict, False


# 模糊查询职级或人名，并返回相应的统计信息
# def generate_fuzzy_query(keyword):
#     query = f"""
#     MATCH (p:Personnel)-[:WORKS_ON]->(r:Report)
#     WHERE p.name Contains  '{keyword}' or p.title Contains '{keyword}'
#     RETURN p.name AS name, COUNT(r) AS report_count
#     """
#     return query
def generate_fuzzy_query(keyword):
    query = f"""
    MATCH (p:Personnel)-[:WORKS_ON]->(r:Report)
    WHERE p.name CONTAINS '{keyword}' OR p.title CONTAINS '{keyword}'
    WITH
        CASE
            WHEN p.name CONTAINS '{keyword}' THEN p.name
            ELSE p.title
        END AS entity,
        COUNT(r) AS report_count
    RETURN entity, report_count
    """
    return query


def process_question(question):
    step = 1
    process_valid = True
    # 生成cql
    cypher_query = generate_cypher_query(question)
    # check and exec cql
    cql_valid, result = exec_cypher_query(cypher_query)
    # print(cql_valid,result)
    # 备用cql
    if cql_valid is False:
        # if len(question) < 7:
        #     step = 2
        #     logger.info(f"[begin use backup CQL] ， question: {question}")
        #     cypher_query = generate_fuzzy_query(question)
        #     cql_valid, result = exec_cypher_query(cypher_query)
        # else:
            step = 3
            process_valid = False
            return cypher_query, None, None, process_valid,step
    # check data match echats
    data_dict, data_valid = convert_to_pd(result)

    return cypher_query, data_valid, data_dict, process_valid,step


if __name__ == "__main__":
    r = process_question("查询2022,2023分别有多少报告")
    print(r)
    # r = process_question("工程")
    # print(r)
    # r = process_question("abc")
    # print(r)
    # r = process_question("查询侯宇编写过哪些报告")
    # print(r)
