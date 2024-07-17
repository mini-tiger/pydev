from neo4j import GraphDatabase

# 配置Neo4j数据库连接
uri = "bolt://120.133.63.166:7687"

class Neo4jHandler:

    def __init__(self, uri):
        self.driver = GraphDatabase.driver(uri)

    def close(self):
        self.driver.close()

    def create_article_author_relationship(self):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_link_nodes)

    def count_articles_by_author(self, author_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._count_articles, author_name)
            return result

    @staticmethod
    def _create_and_link_nodes(tx):
        # 创建作者节点张三
        tx.run("MERGE (a:Author {name: $name})", name="张三")

        # 创建文章1节点并与作者张三建立关系
        tx.run("""
        MERGE (a1:Article {title: $title1})
        MERGE (auth:Author {name: $name})
        MERGE (a1)-[:WRITTEN_BY]->(auth)
        """, title1="发展研究报告", name="张三")

        # 创建文章2节点并与作者张三建立关系
        tx.run("""
        MERGE (a2:Article {title: $title2})
        MERGE (auth:Author {name: $name})
        MERGE (a2)-[:WRITTEN_BY]->(auth)
        """, title2="项目验收报告", name="张三")

        # 创建作者节点李四并与文章2建立关系
        tx.run("""
        MERGE (a2:Article {title: $title2})
        MERGE (auth:Author {name: $name})
        MERGE (a2)-[:WRITTEN_BY]->(auth)
        """, title2="项目验收报告", name="李四")

    @staticmethod
    def _count_articles(tx, author_name):
        query = """
        MATCH (auth:Author {name: $name})<-[:WRITTEN_BY]-(article:Article)
        RETURN count(article) AS article_count
        """
        result = tx.run(query, name=author_name)
        return result.single()["article_count"]

# 创建Neo4j处理器实例并执行操作
neo4j_handler = Neo4jHandler(uri)

# 创建新的节点和关系
neo4j_handler.create_article_author_relationship()

# 查询并打印张三和李四分别写了几篇文章
articles_by_zhangsan = neo4j_handler.count_articles_by_author("张三")
articles_by_lisi = neo4j_handler.count_articles_by_author("李四")

print(f"张三写了 {articles_by_zhangsan} 篇文章")
print(f"李四写了 {articles_by_lisi} 篇文章")

# 关闭连接
neo4j_handler.close()
