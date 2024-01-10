from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# todo aiomysql 可以替代
Base = declarative_base()

_instance = create_engine(
    'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(user='kaleido', password='123456',
                                                                        host='192.168.43.152',
                                                                        port='3306',
                                                                        database='kaleido'),
    max_overflow=int(1),  # 超过连接池大小外最多创建的连接
    pool_size=int(5),  # 连接池大小,默认是5
    pool_timeout=int(1),  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=int(0)  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)



# 插入一条入口
def create_one(id, username, age):
    execute = _instance.execute("INSERT INTO `user`(`id`, `username`, `age`) VALUES (%(id)s, %(username)s,%(age)s);",
                                id=id, username=username, age=age)
    execute.close()

# 查询所有
def selectAll(sql:str):
    execute = _instance.execute(sql)
    list = execute.fetchall()
    execute.close()
    return list

# 根据id查询
def selectById(id):
    execute = _instance.execute("SELECT * FROM user WHERE id = %(id)s;",id=id)
    user = execute.first()
    execute.close();
    return user


# 修改
def updateById(id,username,age):
    execute = _instance.execute("UPDATE `user` SET `username` = %(username)s, `age` = %(age)s WHERE `id` = %(id)s;",username=username,age=age,id=id)
    execute.close()

# 删除
def deleteById(id):
    execute = _instance.execute("DELETE FROM user WHERE id = %(id)s",id=id)
    execute.close()
