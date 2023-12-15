import http
from typing import Optional

from fastapi import FastAPI, Depends

from db.database import engine, SessionLocal
from db.models import Base, Blog as BlogModel
from db.schemas import Blog as BlogValidator
from sqlalchemy.orm.session import Session

app = FastAPI()
# auto migrate
Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


@app.post("/blog", status_code=http.HTTPStatus.OK)  # 执行状态码
def blog_create(param: BlogValidator, db: Session = Depends(get_db)):
    """
    博客-创建
    :param param:
    :return:
    """
    blog = BlogModel(title=param.title, content=param.content, published=param.published)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    # data = param.model_dump_json()
    return blog


@app.get("/blog/lists")
def blog_list(page: Optional[int] = 1, page_size: Optional[int] = 10, is_published: Optional[bool] = False,
              db: Session = Depends(get_db)):
    """
    博客-列表
    :return:
    """
    query = db.query(BlogModel).filter(BlogModel.published == is_published)
    total = query.count()
    offset = (page-1) * page_size
    lists = query.offset(offset).limit(page_size).all()
    return {
        "total": total,
        "list": lists
    }
