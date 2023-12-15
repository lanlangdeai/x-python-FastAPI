# x-python-FastAPI
python的Web框架之Fastapi


**Python版本: 3.10**

## 使用
### openAPI
1. 访问/docs(api管理和调试) **推荐**
2. 访问/redoc

两种风格


## 安装依赖:
```shell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

## 运行
```shell

uvicorn main:app --port 8040 --reload
# 指定文件名称:实例名称
# --reload 已调试模式启动
```

## 常用命令
```shell
# 将依赖放到requirements.txt文件
pip freeze > requirements.txt
```


## 涉及技术点
- 引入Python3.6+中的类型提示功能,基于pydantic库实现
- pydantic-数据验证
- SQLAlchemy-数据库ORM(https://docs.sqlalchemy.org/en/20/)
- PyMySQL-mysql库
