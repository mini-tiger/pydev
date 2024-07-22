import os
import time
import threading
import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, Float,Date,text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, sessionmaker
import pytz
from datetime import datetime
import config
def get_current_time_in_cst():
    utc_now = datetime.utcnow()
    cst_now = utc_now.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai'))
    return cst_now

engine = create_engine(
    url=config.BaseConfig.db_uri,
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    # pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收(重置)
)

# 基类
Base = declarative_base()

# 定义表对象
class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    year = Column(Integer, comment='年份')
    report_number = Column(String(50), comment='报告编号')
    project_name = Column(String(100), comment='项目名称')
    project_field = Column(String(50), comment='项目领域')
    region = Column(String(50), comment='区域')
    investment_amount = Column(Float, comment='投资额')
    investment_amount_unit = Column(String(25), comment='投资额单位')
    filename = Column(String(100), comment='文件名')
    report_time = Column(Date, comment='报告印发时间')
    insert_time = Column(DateTime, default=get_current_time_in_cst, comment='插入时间')
    xmbh = Column(String(128), nullable=True,comment='项目编号')


class Personnel(Base):
    __tablename__ = 'personnel'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    name = Column(String(100), comment='姓名')
    title = Column(String(100), comment='职级职称')
    # rank = Column(String(100))
    job_titles = Column(String(255), comment='工作职称')
    project_role = Column(String(50), comment='项目职位')
    filename = Column(String(100), comment='文件名')
    insert_time = Column(DateTime, default=get_current_time_in_cst, comment='插入时间')
    xmbh = Column(String(128), nullable=True,comment='项目编号')

def is_filename_exist(obj,filename):
    # 查询数据库中是否存在指定filename的记录
    return session.query(obj).filter_by(filename=filename).first() is not None


def get_xmbh_by_filename(filename):
    # 使用原生 SQL 查询数据库
    sql = text("SELECT xmbh FROM v_business_report WHERE filename = :filename")
    result = session.execute(sql, {'filename': filename}).fetchone()

    # 如果找不到记录，返回 None
    if result is None:
        return None

    # 否则返回 xmbh
    return result.xmbh

def delete_records_by_filename(filename):
    try:
        # 删除 reports 表中的记录
        reports_deleted = session.query(Report).filter(Report.filename == filename).delete(synchronize_session=False)

        # 删除 personnel 表中的记录
        personnel_deleted = session.query(Personnel).filter(Personnel.filename == filename).delete(
            synchronize_session=False)

        # 提交事务
        session.commit()

        print(f"Deleted {reports_deleted} records from reports table.")
        print(f"Deleted {personnel_deleted} records from personnel table.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()
def generate_instance_with_personnel(member, role, filename,xmbh):
    name = member.get("name", "")
    title = member.get("title", "")
    # rank = member.get("rank", "")
    job_title = member.get("job_titles", None) if member.get("job_titles",
                                                             None) is not None else member.get("job_title", "")
    # additional_titles = member.get("additional_titles", None)
    # if additional_titles is not None:
    #     title = title + "," + additional_titles
    return Personnel(
        name=name,
        title=title,
        job_titles=job_title,
        project_role=role,
        filename=filename,
        xmbh=xmbh
    )


def generate_instance_with_project(filename, parsed_xml,xmbh):
    # 从解析后的字典中提取数据，使用get方法防止键不存在
    year = int(parsed_xml['report'].get('year', 0))
    report_number = parsed_xml['report'].get('reportNumber', '')
    project_name = parsed_xml['report'].get('projectName', '')
    project_field = parsed_xml['report'].get('projectField', '')
    region = parsed_xml['report'].get('region', '')
    investment_amount_str = parsed_xml['report'].get('investment_amount', '0.0')
    investment_amount = float(investment_amount_str) if investment_amount_str else 0.0
    investment_amount_unit = parsed_xml['report'].get('investment_amount_unit', '')
    report_time = parsed_xml['report'].get('report_time', None)
    # 创建 Report 对象的参数字典
    report_params = {
        'year': year,
        'region': region,
        'report_number': report_number,
        'project_name': project_name,
        'project_field': project_field,
        'filename': filename,
        'investment_amount': investment_amount,
        'investment_amount_unit': investment_amount_unit,
        'xmbh':xmbh
    }

    # 仅在 report_time 存在时添加到参数字典中
    if report_time:
        report_params['report_time'] = report_time

    # 检查解析的值是否合理
    return Report(**report_params)


def insert_project(session, filename, parsed_xml,xmbh):
    try:
        new_project = generate_instance_with_project(filename=filename, parsed_xml=parsed_xml,xmbh=xmbh)
        session.add(new_project)
        session.commit()
        return None
    except Exception as e:
        session.rollback()
        return e

def role_rule_replace(role):
    if "Company Leader" in role:
        role = "公司领导"
    if "Department Head" in role:
        role = "部门负责人"
    if "Project Manager" in role:
        role = "项目经理"
    if "Project Team Member" in role:
        role = "项目组人员"
    if "Assessment Team Member" in role:
        role = "评估组成员"
    if "Energy Business Director" in role:
        role = "能源业务部负责人"

    return role
def insert_personnel(session, filename, parsed_xml,xmbh):
    try:
        for section, members in parsed_xml["root"].items():
            role = section.replace("_", " ")
            role = role_rule_replace(role)
            if isinstance(members["member"], list):
                for member in members["member"]:
                    new_personnel = generate_instance_with_personnel(member, role, filename,xmbh)
                    session.add(new_personnel)
            else:
                member = members["member"]
                new_personnel = generate_instance_with_personnel(member, role, filename,xmbh)
                session.add(new_personnel)
        session.commit()
        return None
    except Exception as e:
        session.rollback()
        return e


# 创建MySQL数据库连接
if config.BaseConfig.RECREATE_TABLE:
    # 删除并重新创建表

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
else:
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# # 清空表中的数据
# session.query(Personnel).delete()
# session.query(Report).delete()
session.commit()
