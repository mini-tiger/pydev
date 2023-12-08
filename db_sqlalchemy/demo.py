#  pip install sqlalchemy
# pip install psycopg2
import os
from typing import List

from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Text, PrimaryKeyConstraint, Boolean,Null
from sqlalchemy.dialects.postgresql import JSON,JSONB
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import not_

engine = create_engine("postgresql+psycopg2://test:test123@172.22.50.25:31867/postgres")

data = [
    {"id": 12,
     "important_terms": "知识产权权属",
     "examples_terms": "本合同履行过程中，乙方在技术服务中完成的技术成果的所有权益，包括但不限于知识产权及所有权，属于甲方。",
     "risk_warning": "从知识产权保护角度，应改为属于乙方。",
     "parts": "xxxxxxxxx",
     "focus": "left,change,right",
     "match_rule_json": "{'a':'abc','b':1}"
     },
    {"id": 13,
     "important_terms": "知识产权权属",
     "examples_terms": "本合同履行过程中，乙方在技术服务中完成的技术成果的所有权益，包括但不限于知识产权及所有权，属于甲方。",
     "risk_warning": "从知识产权保护角度，应改为属于乙方。",
     "parts": "xxxxxxxxx",
     "focus": "left,change,right",
     "key_words": "技术成果,属于",
     "match_rule_json": "{'include':{'and':['abc','bcd'],'or':['aaa','bbb']},'exclude':['bcd','abc']}"
     },
    {"id": 14,
     "important_terms": "知识产权权属",
     "examples_terms": "本合同履行过程中，乙方在技术服务中完成的技术成果的所有权益，包括但不限于知识产权及所有权，属于甲方。",
     "risk_warning": "从知识产权保护角度，应改为属于乙方。",
     "parts": "xxxxxxxxx",
     "focus": "left,change,right",
     },
]


class Base(DeclarativeBase):
    pass





class risk_impact(Base):
    __tablename__ = "risk_impact"

    id = Column(Integer, primary_key=True, autoincrement=True)
    important_terms = Column(String(256))
    risk_warning = Column(String(256))
    examples_terms = Column(Text)
    parts = Column(String(256))
    focus = Column(String(256))
    keyword = Column(String(256))
    match_rule_json = Column(JSONB)



# 创建表
Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

# 连接到数据库
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def to_dict(json_str):
    if json_str is not None:

        return eval(json_str)

# 获取数据库会话
session = loadSession()
def insert_risk_json_data(session, json_data):
    add_all = []
    for item in json_data:

        risk_impact_instance = risk_impact(
            important_terms=item.get("important_terms", ""),
            risk_warning=item.get("risk_warning", ""),
            examples_terms=item.get("examples_terms", ""),
            id=item.get("id", ""),
            parts=item.get("parts", ""),
            focus=item.get("focus", ""),
            # 如果关联关系需要建立，这里也可以处理关联关系
        )

        if "match_rule_json" in item.keys():
            match_rule_json=to_dict(item.get("match_rule_json",None))
            risk_impact_instance.match_rule_json=match_rule_json

        if "key_words" in item.keys():
            risk_impact_instance.keyword=item.get("key_words",None)



        add_all.append(risk_impact_instance)

    session.add_all(add_all)
    session.commit()



if __name__ == "__main__":
    # source_docx_path = "/data/work/pydev/word_对比转换/source_docx"


        # 清空 关联 表中的数据

        # 清空 Word2Record 表中的数据

        # 清空 risk_impact 表中的数据
    session.query(risk_impact).delete()

        # insert risk record
    insert_risk_json_data(session, json_data=data)
    risk_keyword_record = session.query(risk_impact).filter(not_(risk_impact.keyword==None)).all()
    risk_json_record = session.query(risk_impact).filter(not_(risk_impact.match_rule_json==None)).all()

    for i in risk_keyword_record:
        print(i.keyword)

    for i in risk_json_record:
        print(i.match_rule_json,type(i.match_rule_json))