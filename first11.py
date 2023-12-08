from typing import List, Set

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy import Column, String, Integer, Text, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import declarative_base, relationship, Session, DeclarativeBase

# 创建一个 SQLAlchemy 引擎和一个基类
from sqlalchemy import create_engine
from service.llm import baichuan_llm
from sqlalchemy import UniqueConstraint
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
word_record_risk_table = Table(
    "word_record_risk",
    Base.metadata,
    Column("word_2_record_id", ForeignKey("word_2_record.id")),
    Column("risk_impact_id", ForeignKey("risk_impact.id")),
)


class word_2_record(Base):  # 继承生成的orm基类
    __tablename__ = "word_2_record"  # 表名
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    file_name = Column(String(256), comment='文件名')
    line = Column(Integer, comment='row number')
    reserved = Column(Boolean, default=False, comment='是否预留')
    dyx = Column(Boolean, default=False, comment='是否深圳第一线')
    file_type = Column(String(64), comment='文件类型')
    content = Column(Text, comment='内容')
    page_number = Column(String(24), comment='页码')
    part = Column(String(64), comment='段落')
    __table_args__ = (
        UniqueConstraint('dyx', 'reserved','line'),
    )
    risk_impact: Mapped[List["risk_impact"]] = relationship(secondary=word_record_risk_table,back_populates="word_2_record")


class risk_impact(Base):
    __tablename__ = "risk_impact"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    important_terms: Mapped[str] = mapped_column(String(256))
    risk_warning: Mapped[str] = mapped_column(String(256))
    Examples_terms: Mapped[str] = mapped_column(String(256))
    word_2_record: Mapped[List["word_2_record"]] = relationship(secondary=word_record_risk_table,back_populates="risk_impact")


# 创建数据库
Base.metadata.create_all(engine)


session.query(word_record_risk_table).delete()
# 清空 Word2Record 表中的数据
session.query(word_2_record).delete()

# 清空 OtherTable 表中的数据
session.query(risk_impact).delete()
# # # 创建两个老师
child1 = word_2_record(file_name="admin")
child2 = word_2_record(file_name="grunt")
child3 = word_2_record(file_name='shuihen')
#
# # 创建两门课程
Parent1 = risk_impact(name="java")
Parent2 = risk_impact(name="python")
#
# # 添加数据
child1.risk_impact = [Parent1, Parent2]
child2.risk_impact = [Parent1]

session.add(child1)
session.add(child2)
session.add(child3)
session.commit()
# #
# # 查询下数据(根据老师查询课程)
Parent = session.query(word_2_record).filter(word_2_record.file_name == "admin").first()
print(Parent.risk_impact)
for i in Parent.risk_impact:
    print(i.name,i.id)
# 根据课程查询老师
child = session.query(risk_impact).filter(risk_impact.name== "java").first()
# print(child.Parents)
for i in child.word_2_record:
    print(i.file_name,i.id)
