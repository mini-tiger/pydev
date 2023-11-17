#  pip install sqlalchemy
# pip install psycopg2
import os

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Text, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase
from service.确定版本 import *
from service.file_struct_define import *

engine = create_engine("postgresql+psycopg2://test:test123@172.22.50.25:31867/postgres")


class Base(DeclarativeBase):
    pass


class word_2_record(Base):  # 继承生成的orm基类
    __tablename__ = "word_2_record"  # 表名
    file_name = Column(String(256), comment='文件名')
    line = Column(Integer, comment='row number')
    reserved = Column(Boolean, default=False, comment='是否预留')
    dyx = Column(Boolean, default=False, comment='是否深圳第一线')
    file_type = Column(String(64), comment='文件类型')
    content = Column(Text, comment='内容')
    page_number = Column(String(24), comment='页码')
    part = Column(String(64), comment='段落')
    __table_args__ = (
        PrimaryKeyConstraint('dyx', 'reserved','line'),
    )


# 创建表
Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

# 连接到数据库
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# 获取数据库会话
session = loadSession()

from service.utils import replace_str
from unstructured.partition.docx import partition_docx



def record_save_db(name, elements, record_cls):
    add_all = []
    query = session.query(word_2_record).filter(
        word_2_record.file_name == name,
        word_2_record.file_type == "docx",
        word_2_record.reserved == record_cls.reserved,
        word_2_record.dyx == record_cls.dyx)

    deleted_num = query.delete()
    print(f"delete row : {deleted_num}")
    for index, value in enumerate(elements):
        real_txt = replace_str(value.text)
        if len(real_txt) == 0:
            print(f"file: {name},skip element {index}")
            continue
        page = record_cls.page_define(index, value)
        part = record_cls.part_define(index, value)
        to_create = word_2_record(file_name=name,
                                  file_type="docx",
                                  reserved=record_cls.reserved,
                                  dyx=record_cls.dyx,
                                  content=real_txt, part=part,
                                  page_number=page, line=index)
        add_all.append(to_create)

    session.add_all(add_all)
    session.commit()
    session.close()
    print(f"intert row : {len(add_all)},elements: {len(elements)},count: {query.count()}")


if __name__ == "__main__":
    source_docx_path = "/data/work/pydev/word_对比转换/source_docx"
    file_dict = {}
    for file in os.listdir(source_docx_path):
        if file.endswith(".docx"):
            file_dict.setdefault(file, os.path.join(source_docx_path, file))

    for name, file_path in file_dict.items():
        print(f"=====================begin file: {name}")
        elements = partition_docx(filename=file_path)
        file_content = ele2lines(elements=elements)

        if dyx_valid(file_content=file_content):
            if preset_valid(file_content=file_content):
                record_cls = dyx_unstd_reserved()
            else:
                record_cls = dyx_unstd_unreserved()
        else:
            if preset_valid(file_content=file_content):
                record_cls = undyx_unstd_reserved()
            else:
                record_cls = undyx_unstd_unreserved()
                print(f"file: {name} dyx:{record_cls.dyx} reserved:{record_cls.reserved}")

        record_save_db(name=name, elements=elements, record_cls=record_cls)
