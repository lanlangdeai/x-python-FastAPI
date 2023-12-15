from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Blog(BaseModel):
    title: str
    content: str
    published: Optional[bool]



@app.get("/")
def index():
    return {"code": 0, "msg": "hello,FastAPI"}

@app.get("/items/lists")
def fetch_items(page: int = 1, page_size: int = 10, keyword: Optional[str] = None):
    """
    获取数据列表
    :param page:
    :param page_size:
    :param keyword:
    :return:
    """
    return {
        "page": page,
        "page_size": page_size,
        "keyword": keyword
    }

# 可选参数 Optional
# 指定默认值, path路径中的参数必传
@app.get("/items/{item_id}")
def read_item(item_id: int, keyword: Optional[str] = None):
    """
    获取单条数据
    :param item_id:
    :param keyword:
    :return:
    """
    return {"item_id": item_id, "keyword": keyword}


@app.post("/blog")
def blog_create(param: Blog):
    """
    博客-创建
    :param param:
    :return:
    """
    data = param.model_dump_json()
    return {
        "data": data
    }