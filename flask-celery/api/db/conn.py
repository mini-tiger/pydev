import os
import sqlite3
from flask import g

DATABASE = 'database.db'
# DATABASE = ':memory:'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def close_db(db):
    db.close()

def query_db(query, args=(), one=False):
    conn = get_db()
    conn.row_factory = sqlite3.Row  # 设置行工厂以获取包含列名的字典形式结果
    cur = conn.execute(query, args)

    if one:
        rv = cur.fetchone()
    else:
        rv = cur.fetchall()

    cur.close()


    if rv:
        return [dict(row) for row in rv]  # 将结果转换为包含列名的字典列表
    else:
        return []


def insert_job_score_db(filename,job_id,job_type_num,create_at,finish_at):
    conn = get_db()
    cursor=conn.cursor()
    insert_sql = """
    INSERT INTO job_score (filename, downloadurl, job_id,job_type_num, created_at, finish_at)
    VALUES (?, ?, ?,?,?,?);
    """

    # 要插入的数据
    data_to_insert = (filename,"",job_id,job_type_num,create_at,finish_at)  # 替换为实际数据

    # 执行插入数据的SQL语句
    cursor.execute(insert_sql, data_to_insert)

    # 提交更改并关闭连接
    conn.commit()
    cursor.close()
    return conn


def update_job_score_db(job_id,job_type_num,finish_at):
    conn = get_db()
    cursor=conn.cursor()
    # 更新数据的SQL语句
    update_sql = """
    UPDATE job_score SET finish_at = ?, job_type_num = ?
    WHERE job_id = ?;
    """

    # 要更新的数据
    # new_value1 = finish_at  # 替换为新的值
    # new_value2 = 'new_value2'  # 替换为新的值
    # condition_value = 'condition_value'  # 替换为满足条件的值

    # 执行更新数据的SQL语句
    cursor.execute(update_sql, (finish_at, job_type_num, job_id))

    # 提交更改并关闭连接
    conn.commit()
    cursor.close()
    return conn



def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # 创建表的SQL语句
        create_table_sql = ""
        with open("schema.sql", 'r') as file:
            sql_statements = file.read().split(';')
            for statement in sql_statements:
                if statement.strip():  # 忽略空语句
                    cursor.execute(statement)

        # 提交更改并关闭连接
        cursor.close()
        db.commit()

        db.close()