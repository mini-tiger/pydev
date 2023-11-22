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
from sqlalchemy import Column, String, Integer, Text, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase
from service.确定版本 import *
from service.file_struct_define import *
from sqlalchemy import UniqueConstraint
from service.utils import split_str
from sqlalchemy import func
engine = create_engine("postgresql+psycopg2://test:test123@172.22.50.25:31867/postgres")

data = [
    {"id": 1,
     "important_terms": "互联网信息安全责任书 网站备案义务告知书",
     "Examples_terms": "IDC销售合同模板中的《互联网信息安全责任书》、《网站备案义务告知书》。",
     "risk_warning": "出处：《互联网信息服务管理办法》、《计算机信息网络国际联网安全保护管理办法》、《网络安全法》、《非经营性互联网信息服务备案管理办法》、《关于整治虚拟货币“挖矿”活动的通知》、《中华人民共和国计算机信息网络国际联网管理暂行规定》、《工业和信息化部关于清理规范互联网网络接入服务市场的通知》。",
     "parts": "互联网信息安全责任书,网站备案义务告知书",
     "focus": "left,change",
     },
    {"id": 2,
     "important_terms": "排除我司留置权条款",
     "Examples_terms": "若甲方发生逾期支付，乙方不得留置并擅自处置甲方所有资产。",
     "risk_warning": "甲方有资产托管在我司机房，甲方如逾期付款，我司享有留置权，即有权留置甲方资产通过拍卖、变卖优先受偿所得价款，以抵扣甲方欠款。如甲方在协议中排除我司留置权，则我司无权留置并处置甲方资产。",
     "parts": "5.9.1.,5.9.2.,5.9.3.",
     "focus": "left,change",
     },
    {"id": 3,
     "important_terms": "间接损失赔偿条款",
     "Examples_terms": "乙方应赔偿甲方的全部损失，包括但不限于直接经济损失、可得收入和利润损失、商誉损失等，甲方因追究乙方违约责任而发生的包括但不限于诉讼费、律师费、公证费、保全费、公告费、鉴定费等各项费用均应由乙方承担。",
     "risk_warning": "此损失赔偿范围太过广泛，赔偿责任过重，通常只能接受赔偿客户的直接经济损失。但如销售侧确无法删除的话，则需要在最后补充约定我司赔偿责任的上限，如合同总金额的一定百分比。",
     "parts": "建议做一张新表 匹配文本中的关键字",
     "focus": "left,change",
     },
    {"id": 4,
     "important_terms": "删除我司赔偿责任上限条款",
     "Examples_terms": "无论何种情形下，服务方最高赔偿额不超过赔偿事项发生当月相关服务的月服务费或等额服务。",
     "risk_warning": "如删除或修改我司赔偿责任上限条款，意味着我司对客户应承担的赔偿责任风险不可控，该赔偿责任不以我司已收取的服务费金额为赔偿上限。",
     "parts": "2.4.,2.4节中的表格",
     "focus": "left,change",
     },
    {"id": 5,
     "important_terms": "删除不可抗力条款中某些事由",
     "Examples_terms": "非因双方原因发生的火灾、电信网络、供电单位的电力设施故障、黑客攻击、尚无有效防御措施的计算机病毒的发作。",
     "risk_warning": "在IDC行业，发生以上事项属于我司不能预见并且对其发生和后果不能防止并避免的不可控因素，具体明确约定清楚，我司可免责。否则，我司存在违约风险。",
     "parts": "11.",
     "focus": "left,change",
     },
    {"id": 6,
     "important_terms": "删除我司免责条款或某些事由",
     "Examples_terms": "因存在下列任何一种情形，导致服务不能提供、不能及时提供或造成服务不达标的，服务方不承担责任：     9.1	用户方未依约支付费用；     9.2	自服务中断发生之时起24小时之内，用户方未向服务方书面报告的 ；     9.3	因用户方设备中的操作系统、应用程序、用户方数据以及有关的系统配置数据等的安全或管理问题而引起的；     9.4	任何用户方的电路或设备（包括用户方租用的第三方提供的设备）所引起的；     9.5	用户方的疏忽或由用户方授权服务方进行的操作所引起的；     9.6	供电单位采取的限电或断电措施；     9.7	其他由用户方原因所引起的情况。",
     "risk_warning": "主要因用户方原因，或供电单位原因导致的服务不能提供、不能及时提供或造成服务不达标的，我司免责。否则，会造成不是我司原因导致的，我司还要承担赔偿责任。",
     "parts": "2.3.2.,9.1.,9.2.,9.3.,9.4.,9.5.,9.6.,9.7.",
     "focus": "left,change",
     },
    {"id": 7,
     "important_terms": "删除设备赔偿上限条款",
     "Examples_terms": "服务期内因服务方故意或重大过失造成用户方设备遗失或损毁的，服务方须修复、重置或赔偿，赔偿金额为所遗失或损毁的用户方设备届时重新购置的市场价格（“封顶金额”），超过封顶金额以外的部分由用户方自行承担。     改为      服务期内因服务方原因造成用户方设备遗失或损毁的，服务方须修复、重置或赔偿，赔偿金额为所遗失或损毁的用户方设备届时重新购置的市场价格，给用户方造成其他损失的，用户方应承担赔偿责任，此赔偿责任不适用本协议第8.1条。",
     "risk_warning": "由因服务方故意或重大过失改为“因服务方原因”，造成的原因范围扩大了；其次，不仅赔偿用户方设备还需赔偿其他损失（例如数据丢失），赔偿责任加重了，且不受协议中关于赔偿上限条款的约束。整体上，提高了我司的赔偿风险。",
     "parts": "3.1.,6.5.",
     "focus": "left,change",
     },
]


class Base(DeclarativeBase):
    pass


word_record_risk_table = Table(
    "word_record_risk",
    Base.metadata,
    Column("word_2_record_id", ForeignKey("word_2_record.id")),
    Column("risk_impact_id", ForeignKey("risk_impact.id")),
)


class word_2_record(Base):  # 继承生成的orm基类
    __tablename__ = "word_2_record"  # 表名
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_name = Column(String(256), comment='文件名')
    line = Column(Integer, comment='row number')
    reserved = Column(Boolean, default=False, comment='是否预留')
    dyx = Column(Boolean, default=False, comment='是否深圳第一线')
    file_type = Column(String(64), comment='文件类型')
    content = Column(Text, comment='内容')
    page_number = Column(String(24), comment='页码')
    part = Column(String(64), comment='段落')
    __table_args__ = (
        UniqueConstraint('dyx', 'reserved', 'line'),
    )
    risk_impact: Mapped[List["risk_impact"]] = relationship(secondary=word_record_risk_table,
                                                            back_populates="word_2_record")


class risk_impact(Base):
    __tablename__ = "risk_impact"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    important_terms: Mapped[str] = mapped_column(String(256))
    risk_warning: Mapped[str] = mapped_column(String(256))
    examples_terms: Mapped[str] = mapped_column(Text)
    parts: Mapped[str] = mapped_column(String(256))
    focus: Mapped[str] = mapped_column(String(256))
    word_2_record: Mapped[List["word_2_record"]] = relationship(secondary=word_record_risk_table,
                                                                back_populates="risk_impact")


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


def insert_word2record_json_data(name, elements, record_cls):
    add_all = []
    query = session.query(word_2_record).filter(
        word_2_record.file_name == name,
        word_2_record.file_type == "docx",
        word_2_record.reserved == record_cls.reserved,
        word_2_record.dyx == record_cls.dyx)
    #
    # deleted_num = query.delete()
    # print(f"delete row : {deleted_num}")
    id = 0
    max_id = session.query(func.max(word_2_record.id)).scalar()
    if max_id is not None:
        id =max_id

    for index, value in enumerate(elements):
        id = id+1
        real_txt = replace_str(value.text)
        if len(real_txt) == 0:
            print(f"file: {name},skip element {index}")
            continue
        page = record_cls.page_define(index, value)
        part = record_cls.part_define(index, value)
        to_create = word_2_record(
                                id=id,
                                file_name=name,
                                  file_type="docx",
                                  reserved=record_cls.reserved,
                                  dyx=record_cls.dyx,
                                  content=real_txt, part=part,
                                  page_number=page, line=index)

        add_all.append(to_create)

    session.add_all(add_all)
    session.commit()

    print(f"insert row : {len(add_all)},elements: {len(elements)},count: {query.count()}")


def insert_association_json_data():

    risk_impact_data = session.query(risk_impact).all()
    for v in risk_impact_data:
        for subv in split_str(v.parts,","):
            # 不能是 like %% , 5.9.1  与 9.1类似
            word_2_record_datas = session.query(word_2_record).filter(word_2_record.part.like(f"{subv}%")).all()

            v.word_2_record.extend(word_2_record_datas)
    session.commit()

    # d=session.query(word_2_record).filter(word_2_record.part.like(f"%网站备案义务告知书%")).first()
    # ddd = "\n".join([v.risk_warning for v in d.risk_impact])
    # print(ddd)


def insert_risk_json_data(session, json_data):
    add_all = []
    for item in json_data:
        risk_impact_instance = risk_impact(
            important_terms=item.get("important_terms", ""),
            risk_warning=item.get("risk_warning", ""),
            examples_terms=item.get("Examples_terms", ""),
            id=item.get("id", ""),
            parts=item.get("parts", ""),
            focus=item.get("focus", ""),
            # 如果关联关系需要建立，这里也可以处理关联关系
        )
        add_all.append(risk_impact_instance)
    session.add_all(add_all)
    session.commit()


if __name__ == "__main__":
    source_docx_path = "/data/work/pydev/word_对比转换/source_docx"

    # 清空 关联 表中的数据
    session.query(word_record_risk_table).delete()
    # 清空 Word2Record 表中的数据
    session.query(word_2_record).delete()
    # 清空 risk_impact 表中的数据
    session.query(risk_impact).delete()

    insert_risk_json_data(session, json_data=data)

    file_dict = {}
    for file in os.listdir(source_docx_path):
        if file.endswith(".docx"):
            file_dict.setdefault(file, os.path.join(source_docx_path, file))
    #
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

        insert_word2record_json_data(name=name, elements=elements, record_cls=record_cls)
    insert_association_json_data()
    session.close()
