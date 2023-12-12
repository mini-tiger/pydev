from typing import List, Set

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy import Column, String, Integer, Text, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import declarative_base, relationship, Session, DeclarativeBase

# 创建一个 SQLAlchemy 引擎和一个基类
from sqlalchemy import create_engine
from service.llm import baichuan_llm

engine = create_engine("postgresql+psycopg2://test:test123@172.22.50.25:31867/postgres")
from sqlalchemy.orm import sessionmaker

# 连接到数据库
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# 获取数据库会话
session = loadSession()


class Base(DeclarativeBase):
    pass


from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

# note for a Core table, we use the sqlalchemy.Column construct,
# not sqlalchemy.orm.mapped_column
child_parent_table = Table(
    "child_parent_table",
    Base.metadata,
    Column("child_name", ForeignKey("Child.id")),
    Column("parent_name", ForeignKey("Parent.id")),
)


class Child(Base):
    __tablename__ = "Child"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    Parents: Mapped[List["Parent"]] = relationship(secondary=child_parent_table,back_populates="children")



class Parent(Base):
    __tablename__ = "Parent"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    children: Mapped[List["Child"]] = relationship(secondary=child_parent_table,back_populates="Parents")


# 创建数据库
Base.metadata.create_all(engine)

# # # 创建两个老师
child1 = Child(name='admin')
child2 = Child(name='grunt')
child3 = Child(name='shuihen')
#
# # 创建两门课程
Parent1 = Parent(name="java")
Parent2 = Parent(name="python")
#
# # 添加数据
Parent1.children = [child1, child2]
Parent2.children = [child1, child3]

session.add(Parent1)
session.add(Parent2)
session.commit()
# #
# # 查询下数据(根据老师查询课程)
Parent = session.query(Parent).filter(Parent.name == "java").first()
# print(Parent.children)
for i in Parent.children:
    print(i.name,i.id)
# 根据课程查询老师
child = session.query(Child).filter(Child.name== "admin").first()
# print(child.Parents)
for i in child.Parents:
    print(i.name,i.id)
