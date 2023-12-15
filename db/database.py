from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# @float

# @todo 放到配置文件中
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:123456@localhost/python-fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)  # 打印SQL
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# 生成的未来所有model的基类
# Base = declarative_base()





