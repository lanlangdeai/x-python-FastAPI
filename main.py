import http
from typing import Optional, List

from fastapi import FastAPI, Depends

import db.schemas
from db.database import engine, SessionLocal
from db.models import Base, Blog as BlogModel, User as UserModel
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
    offset = (page - 1) * page_size
    lists = query.offset(offset).limit(page_size).all()
    return {
        "total": total,
        "list": lists
    }


@app.get("/blog/detail")
def blog_detail(id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter_by(id=id).first()
    return blog


@app.delete("/blog/{id}")
def blog_del(id: int, db: Session = Depends(get_db)):
    db.query(BlogModel).filter_by(id=id).delete(synchronize_session=False)
    db.commit()
    return {"msg": "success"}


@app.put("/blog/{id}")
def blog_update(id: int, param: BlogValidator, db: Session = Depends(get_db)):
    db.query(BlogModel).filter_by(id=id).update(param.model_dump())
    db.commit()
    return {"msg": "success"}


# =================================== 用户


@app.get("/user/list", response_model=List[db.schemas.ShowUser])  # 只返回指定字段
def user_list(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users
