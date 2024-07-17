import traceback

from neo4j import GraphDatabase
from loguru import logger
import config

# 配置Neo4j数据库连接

uri = config.BaseConfig.neo4j_uri
username = config.BaseConfig.neo4j_username
password = config.BaseConfig.neo4j_password


class Neo4jHandler:

    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password), max_connection_lifetime=300)

    def close(self):
        self.driver.close()

    def clear_database(self):
        with self.driver.session() as session:
            session.write_transaction(self._clear_db)

    def run_query(self, query, parameters=None):
        data = []
        logger.info(f"EXEC CQL:{query}")
        with self.driver.session() as session:
            try:
                result = session.run(query, parameters)
                return True, [record for record in result]
            except Exception as e:
                logger.error(f"Invalid Cypher query: {e}")
                # print(e)
                return False, data
    def create_nodes_and_relationships(self, filename, data):
        with self.driver.session() as session:
            session.write_transaction(self._create_nodes_and_relationships, filename, data)

    def count_reports_by_author_and_year(self, author_name, year):
        with self.driver.session() as session:
            result = session.read_transaction(self._count_reports_by_author_and_year, author_name, year)
            return result

    # 删除与filename相关的节点及关系的函数
    def delete_records_by_filename(self,filename):

        with self.driver.session() as session:
            session.write_transaction(self._delete_records_by_filename, filename)

    @staticmethod
    def _delete_records_by_filename(tx,filename):
        # 删除与Personnel节点相关的所有关系
        tx.run("MATCH (p:Personnel)-[w:WORKS_ON]->(r:Report {filename: $filename}) DELETE w", filename=filename)
        # 删除Personnel节点和对应的Report节点
        tx.run("MATCH (p:Personnel)-[:WORKS_ON]->(r:Report {filename: $filename}) DELETE p, r", filename=filename)
    @staticmethod
    def _clear_db(tx):
        tx.run("MATCH (n) DETACH DELETE n")

    def check_report_exists(self, filename):
        with self.driver.session() as session:
            query = """
              MATCH (r:Report {filename: $filename})
              RETURN r
              """
            result = session.run(query, filename=filename)
            return result.single() is not None
    @staticmethod
    def _generate_member_obj(member,tx,statements,role,filename):
        name = member.get("name", "")
        title = member.get("title", "")
        job_title = member.get("job_titles", None) if member.get("job_titles",
                                                                 None) is not None else member.get(
            "job_title", "")
        statement = """
        MERGE (p:Personnel {name: $name, title: $title,job_title:$title,rank:$title, post: $job_title})
        ON CREATE SET p.filename = $filename
        MERGE (r:Report {filename: $filename})
        MERGE (p)-[:WORKS_ON {role: $role}]->(r)
        """
        tx.run(statement, name=name, title=title, job_title=job_title, filename=filename, role=role)
        statements.append((statement,
                           {"name": name, "title": title, "job_title": job_title, "filename": filename,
                            "role": role}))

    def _create_nodes_and_relationships(self,tx, filename, data):
        try:
            statements = []
            # 创建或更新报告节点
            report = data['report']
            year = int(report.get('year', 0))
            report_number = report.get('reportNumber', '')
            project_name = report.get('projectName', '')
            project_field = report.get('projectField', '')
            region = report.get('region', '')
            investment_amount = report.get('investment_amount', 0)
            try:
                # 尝试将值转换为 float
                investment_amount = float(investment_amount)
            except (ValueError, TypeError):
                # 如果发生 ValueError 或 TypeError 异常，则将值设为 0
                investment_amount = 0

            investment_amount_unit = report.get('investment_amount_unit', '')

            statement = """
            MERGE (r:Report {filename: $filename})
            ON CREATE SET r.year = $year, r.report_number = $report_number, r.project_name = $project_name, r.project_field = $project_field,
            r.investment_amount = $investment_amount,r.investment_amount_unit = $investment_amount_unit,r.region = $region
            """
            tx.run(statement, filename=filename, year=year, report_number=report_number, project_name=project_name,
                   project_field=project_field,investment_amount=investment_amount, investment_amount_unit=investment_amount_unit,region=region)
            statements.append((statement, {"filename": filename, "year": year, "report_number": report_number,
                                           "project_name": project_name, "project_field": project_field,
                                           "investment_amount": investment_amount,
                                           "investment_amount_unit": investment_amount_unit,"region": region}))

            # 创建人员节点并与报告建立关系
            for section, members in data["root"].items():
                role = section.replace("_", " ")
                if isinstance(members["member"], list):
                    for member in members["member"]:
                        self._generate_member_obj(member,tx,statements,role,filename)

                else:
                    member = members["member"]
                    self._generate_member_obj(member, tx, statements, role, filename)

            # 保存语句到文件
            # Neo4jHandler.save_statements_to_file(statements, filename)
            return None
        except Exception as e:
            return e
    @staticmethod
    def _count_reports_by_author_and_year(tx, author_name, year):
        query = """
        MATCH (p:Personnel {name: $author_name})-[:WORKS_ON]->(r:Report {year: $year})
        RETURN count(r) AS report_count
        """
        result = tx.run(query, author_name=author_name, year=year)
        return result.single()["report_count"]

    @staticmethod
    def save_statements_to_file(statements, filename):
        with open(f"{filename}_statements.txt", "w") as file:
            for statement, params in statements:
                file.write(f"{statement}\n")
                file.write(f"{params}\n")

    @staticmethod
    def load_statements_from_file(filename):
        statements = []
        with open(f"{filename}_statements.txt", "r") as file:
            while True:
                statement = file.readline().strip()
                if not statement:
                    break
                params = eval(file.readline().strip())
                statements.append((statement, params))
        return statements

    def replay_statements(self, filename):
        statements = self.load_statements_from_file(filename)
        with self.driver.session() as session:
            for statement, params in statements:
                session.write_transaction(self._run_statement, statement, params)

    @staticmethod
    def _run_statement(tx, statement, params):
        tx.run(statement, **params)


def New_conn_neo4j():
    return Neo4jHandler(uri, username, password)


if config.BaseConfig.RECREATE_TABLE and config.BaseConfig.NEO4J_USE:
    # 清空数据库（如果需要）
    New_conn_neo4j().clear_database()

# # 示例用法
# if __name__ == "__main__":
#     # 示例 JSON 数据
#     json_data_1 = {
#         "root": {
#             "Department_Head": {
#                 "member": {
#                     "name": "严碧波",
#                     "title": "正高级工程师"
#                 }
#             },
#             "Project_Manager": {
#                 "member": {
#                     "name": "杜建刚",
#                     "title": "正高级工程师"
#                 }
#             },
#             "Project_Team_Members": {
#                 "member": [
#                     {
#                         "name": "杨文婷",
#                         "title": "工程师"
#                     },
#                     {
#                         "name": "徐建强",
#                         "title": "正高级工程师"
#                     },
#                     {
#                         "name": "陈建林",
#                         "title": "正高级工程师",
#                         "job_title": "专家组长"
#                     }
#                 ]
#             }
#         },
#         "report": {
#             "year": "2022",
#             "reportNumber": "咨能源[2022]2546号",
#             "projectName": "青海同德抽水蓄能电站项目",
#             "projectField": "能源"
#         }
#     }
#
#     json_data_2 = {
#         "root": {
#             "Department_Head": {
#                 "member": {
#                     "name": "严碧波",
#                     "title": "正高级工程师"
#                 }
#             },
#             "Project_Manager": {
#                 "member": {
#                     "name": "杜建刚",
#                     "title": "正高级工程师"
#                 }
#             },
#             "Project_Team_Members": {
#                 "member": [
#                     {
#                         "name": "杨立锋",
#                         "title": "正高级工程师",
#                         "job_title": "水工"
#                     },
#                     {
#                         "name": "钟娜",
#                         "title": "正高级工程师",
#                         "job_title": "规划"
#                     }
#                 ]
#             }
#         },
#         "report": {
#             "year": "2022",
#             "reportNumber": "咨能源[2022]2547号",
#             "projectName": "另一个项目",
#             "projectField": "能源"
#         }
#     }
#
#     filename_1 = "file1.pdf"
#     filename_2 = "file2.pdf"
#
#     neo4j_handler = New_conn_neo4j()
#
#     # 清空数据库（如果需要）
#     neo4j_handler.clear_database()
#
#     # 插入第一个 JSON 数据
#     neo4j_handler.create_nodes_and_relationships(filename_1, json_data_1)
#     # 插入第二个 JSON 数据
#
#     # 插入第二个 JSON 数据
#     neo4j_handler.create_nodes_and_relationships(filename_2, json_data_2)
#
#     # 查询陈建林编写过的2022年报告的数量
#     author_name = "严碧波"
#     year = 2022
#     count = neo4j_handler.count_reports_by_author_and_year(author_name, year)
#     print(f"{author_name} 编写过 {count} 个 {year} 年的报告")
#
#     # 关闭连接
#     neo4j_handler.close()
