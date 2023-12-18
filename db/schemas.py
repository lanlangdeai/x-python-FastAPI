from typing import Optional

from pydantic import BaseModel


# 定义入参
class Blog(BaseModel):
    title: str
    content: str
    published: Optional[bool]



class User(BaseModel):
    username: str
    password: str
    age: int
    gender: str

class ShowUser(BaseModel):
    username: str
    age: int
    gender: str
    class Config():
        orm_mode = True