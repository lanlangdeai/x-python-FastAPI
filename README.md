# x-python-FastAPI
python的Web框架之Fastapi


## 待优化
- [ ] 统一返回值(验证+最终响应)
- [ ] 日志处理(支持分割)
- [ ] 项目结构优化





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
# 安装所有依赖
pip install "fastapi[all]"
# 将依赖放到requirements.txt文件
pip freeze > requirements.txt
```


## 涉及技术点
- 引入Python3.6+中的类型提示功能,基于pydantic库实现
- pydantic-数据验证
- SQLAlchemy-数据库ORM(https://docs.sqlalchemy.org/en/20/)
- PyMySQL-mysql库


## FastAPI框架
特点:
* 快速：拥有非常高的性能，归功于 Starlette 和 Pydantic；Starlette 用于路由匹配，Pydantic 用于数据验证；
* 开发效率：功能开发效率提升 200% 到 300%；
* 减少 bug：减少 40% 的因为开发者粗心导致的错误；
* 智能：内部的类型注解非常完善，IDE 可处处自动补全；
* 简单：框架易于使用，文档易于阅读；
* 简短：使代码重复最小化，通过不同的参数声明实现丰富的功能；
* 健壮：可以编写出线上使用的代码，并且会自动生成交互式文档；
* 标准化：兼容 API 相关开放标准；



参考文档:
- https://mp.weixin.qq.com/s/sA61QotzueIpvaVPGiUrAQ
- 