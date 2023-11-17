import docx
# import nltk
from difflibparser.difflibparser import *
# nltk.set_proxy('http://127.0.0.1:1081')
# nltk.download("punkt")
from service.utils import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text
from word_对比转换.run_init_db import word_2_record

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

from unstructured.partition.docx import partition_docx

elements = partition_docx(filename="/data/work/pydev/word_对比转换/source_docx/unlock_dyx_static_带宽罚则 非锁定版IDC主协议_深圳第一线通信服务协议(2023年版)-（预留机柜）.docx")
elements1 = partition_docx(filename="/data/work/pydev/word_对比转换/unlock_dyx_static_带宽罚则 非锁定版IDC主协议_深圳第一线通信服务协议(2023年版)-（预留机柜）.docx")


for i,value in enumerate(elements):
    print(elements[i].text)



src_unstruct_dict = {}
dest_unstruct_dict = {}
src_unstruct_elm = {}
dest_unstruct_elm = {}
with open("lock2023_new11.txt", "w") as f:
    for i in elements:
        f.write(i.text)
        f.write("\n")
        src_unstruct_dict[replace_str(i.text)] = {"id": i.id, "parent_id": i.metadata.parent_id,
                                                  "page_number": i.metadata.page_number}
        src_unstruct_elm[i.id] = i.text

with open("lock2023_new_modify11.txt", "w") as f:
    for i in elements1:
        f.write(i.text)
        f.write("\n")
        dest_unstruct_dict[replace_str(i.text)] = {"id": i.id, "parent_id": i.metadata.parent_id,
                                                   "page_number": i.metadata.page_number}
        dest_unstruct_elm[i.id] = i.text

with open("lock2023_new11.txt", 'r') as file1, open("lock2023_new_modify11.txt", 'r') as file2:
    file1_content = file1.readlines()
    file2_content = file2.readlines()

differ = DifflibParser(file1_content, file2_content)
line_number = 0

for line in differ:
    if line['code'] > 0:
        if line['code'] == DiffCode.LEFTONLY:
            row = line["line"]
            print(row)
            if str_valid(row):
                continue
            if src_unstruct_dict.get(replace_str(line["line"])):
                lc = src_unstruct_dict[replace_str(line["line"])]
                lca = session.query(word_2_record).filter(
                    word_2_record.content.like(f'%{replace_str(row)}%')).all()
                if len(lca) > 0:
                    print(lca[0].page_number, lca[0].part)
                print("l ", lc)
                if src_unstruct_elm.get(lc["parent_id"]):
                    print("source doc", src_unstruct_elm[lc["parent_id"]])

        if line['code'] == DiffCode.RIGHTONLY:
            print(line["line"])

            if dest_unstruct_dict.get(replace_str(line["line"])):
                rc = dest_unstruct_dict[replace_str(line["line"])]
                # print("r",rc)
                if dest_unstruct_elm.get(rc["parent_id"]):
                    print("dest doc", dest_unstruct_elm[rc["parent_id"]])

        if line['code'] == DiffCode.CHANGED:
            # print("ccline",line["line"])
            # print("ccnewline",line["newline"])
            leftchanges = line.get('leftchanges', [])
            rightchanges = line.get('rightchanges', [])
            if len(leftchanges) > 0:
                if src_unstruct_dict.get(replace_str(line["line"])):
                    lc = src_unstruct_dict[replace_str(line["line"])]
                    print("cl ", lc)
                    if src_unstruct_elm.get(lc["parent_id"]):
                        print("csource doc", src_unstruct_elm[lc["parent_id"]])
            if len(rightchanges) > 0:
                if dest_unstruct_dict.get(replace_str(line["newline"])):
                    rc = dest_unstruct_dict[replace_str(line["newline"])]
                    print("cr", rc)
                    if dest_unstruct_elm.get(rc["parent_id"]):
                        print("cdest doc", dest_unstruct_elm[rc["parent_id"]])
