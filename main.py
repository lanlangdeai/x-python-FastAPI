import http
from enum import Enum
from typing import Optional, List, Union

from fastapi import FastAPI, Depends, Query, Path, Request, Response
import orjson

import db.schemas
from db.database import engine, SessionLocal
from db.models import Base, Blog as BlogModel, User as UserModel
from db.schemas import Blog as BlogValidator
from sqlalchemy.orm.session import Session

app = FastAPI(title="x-python-FastAPI",
              description="python fastapi",
              # docs_url=  # 文档地址
              # openapi_url=  # openapi地址
              )
# auto migrate
Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def index():
    return {"code": 0, "msg": "hello,FastAPI"}



@app.get("/text/response")
async def test_response():
    data = {
        "name": "ixng",
        "age": 10
    }

    response = Response(

    )


@app.get("/request/info")
async def request_info(request: Request):
    """
    路径参数必须体现在参数中, 但是查询参数可以不写
    :param request:
    :return:
    """
    name = request.query_params.get("name")  # 获取某个key参数
    hobby = request.query_params.getlist("hobby")  # 获取同一个字段,传递多个值的情况
    return dict(
        query_params=request.query_params,
        method=request.method,  # 请求方式 GET/POST/DELETE/PUT/HEAD
        headers=request.headers,  # 请求头参数
# "host": "127.0.0.1:8040",
# "connection": "keep-alive",
# "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
# "accept": "application/json",
# "sec-ch-ua-mobile": "?0",
# "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
# "sec-ch-ua-platform": "\"Windows\"",
# "sec-fetch-site": "same-origin",
# "sec-fetch-mode": "cors",
# "sec-fetch-dest": "empty",
# "referer": "http://127.0.0.1:8040/docs",
# "accept-encoding": "gzip, deflate, br",
# "accept-language": "zh-CN,zh;q=0.9,en;q=0.8"
        cookies=request.cookies  # 请求cookie
    )


'''
Response 内部接收如下参数：

content：返回的数据；
status_code：状态码；
headers：返回的响应头；
media_type：响应类型（就是响应头里面的 Content-Type，这里单独作为一个参数出现了，其实通过 headers 参数设置也是可以的）；
background：接收一个任务，Response 在返回之后会自动异步执行；

'''




@app.get("/items/lists")
async def fetch_items(page: int = 1, page_size: int = 10, keyword: Optional[str] = None):
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
async def read_item(
        item_id: int = Path(..., alias="item-id"),  # 对于path中的数据校验使用Path,校验方式与Query一样
        keyword: Optional[str] = None):
    """
    获取单条数据
    :param item_id:
    :param keyword:
    :return:
    """
    return {"item_id": item_id, "keyword": keyword}


@app.get("/items")
async def read_items(
        a1: str,
        a2: List[str] = Query(...),  # 需要指定Query(...),否则会识别为body中的数据
        # b: List[str] = Query(...)
        b: List[str] = Query(["1", "好好"])  # 指定默认参数
):
    return {"a1": a1, "a2": a2, "b": b}




# @app.get("/items")
# async def read_items(
#     # 三个查询参数，分别是 item-query、@@@@、$$$$
#     # 但它们不符合 Python 变量的命名规范
#     # 于是要为它们起别名
#     item1: Optional[str] = Query(None, alias="item-query"),
#     item2: str = Query("哈哈", alias="@@@@"),
#     # item3 是必传的
#     item3: str = Query(..., alias="$$$$")
# ):
#     return {"item-query": item1, "@@@@": item2, "$$$$": item3}


'''
参数校验:
string:
    min_length=2  最小长度
    max_length=10  最大长度
integer:
    gt=5  大于5
    le=10 小于等于10
    ge=10,le=10 必须等于10
'''







# ===================================== Blog
@app.post("/blog", status_code=http.HTTPStatus.OK)  # 执行状态码
async def blog_create(param: BlogValidator, db: Session = Depends(get_db)):
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
async def blog_list(page: Optional[int] = 1, page_size: Optional[int] = 10, is_published: Optional[bool] = False,
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
async def blog_detail(id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter_by(id=id).first()
    return blog


@app.delete("/blog/{id}")
async def blog_del(id: int, db: Session = Depends(get_db)):
    db.query(BlogModel).filter_by(id=id).delete(synchronize_session=False)
    db.commit()
    return {"msg": "success"}


@app.put("/blog/{id}")  # 不指定默认值,表明该字段是需要必传的
async def blog_update(id: int, param: BlogValidator, db: Session = Depends(get_db)):
    db.query(BlogModel).filter_by(id=id).update(param.model_dump())
    db.commit()
    return {"msg": "success"}


# 声明 file_path 的类型为 path
# 这样它会被当成一个整体
@app.get("/files/{file_path:path}")
async def get_file(file_path: str):
    return {"file_path": file_path}






# =================================== 用户


# 定义统一列表参数
async def common_list_params(
        page: int = 1,
        page_size: int = 10,
):
    return {"page": page, "page_size": page_size}


# @app.get("/user/list", response_model=List[db.schemas.ShowUser])  # 只返回指定字段
@app.get("/user/list")  # 只返回指定字段
async def user_list(
        params: dict = Depends(common_list_params),
        db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return {
        'user': users,
        'params': params
    }


# 验证参数
@app.get("/user/check")
async def check_user(
        password: str = Query(..., min_length=2, max_length=10),  # 对于必传参数进行校验, 注意默认值为"..."
        user_id: Optional[str] = Query(None, min_length=4, max_length=20)  # 指定参数默认值,最短与最长
#         更多校验regex=r"^prefix" 以prefix为前缀的字符串等
):
    return {'user_id': user_id}

# 指定枚举类型
class Name(str, Enum):
    lanName = "lan"  # key只是指定字段, 限制输入参数为值, 返回该参数
    langName = "lang"


# @app.get("/user/{username}")
# async def get_user(username: Name):
#     return {"user_id": username}

# 用户ID,同时支持int和str, name为可选字段
@app.get("/user/{user_id}")
async def get_one_user(user_id: Union[int, str], name: Optional[str] = None):
    return {'user_id': user_id, 'name': name}





