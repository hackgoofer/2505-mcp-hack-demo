from fastapi import FastAPI

test_app = FastAPI()


@test_app.get("/")
def read_root():
    return {"Hello": "World"}


@test_app.get("/test")
def test_endpoint():
    return {"status": "working"}
