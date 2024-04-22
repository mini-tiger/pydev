# from sqlalchemy import create_engine, Column, Integer, String, func
# from sqlalchemy.orm import sessionmaker
# from config import BaseConfig as config
#
# engine = create_engine(
#     f"postgresql+psycopg2://{config.PG_VCT_USER}:{config.PG_VCT_PWD}@{config.PG_VCT_HOST}:{config.PG_VCT_PORT}/{config.PG_VCT_DB}")
#
#
# # 连接到数据库
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# def loadSession():
#     Session = sessionmaker(expire_on_commit=False, autoflush=False, bind=engine)
#     session = Session()
#     return session
#
#
#
# # 获取数据库会话
# session = loadSession()