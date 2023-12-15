from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import Mapped

class Base(DeclarativeBase):
    pass

class Blog(Base):

    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(32))
    content = Column(String(255))
    published = Column(Boolean)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32))
    password = Column(String(32))
    age = Column(Integer)
    gender = Column(String(32))


