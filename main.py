from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"code": 0, "msg": "hello,FastAPI"}

