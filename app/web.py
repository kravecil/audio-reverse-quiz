from fastapi import APIRouter

web = APIRouter()


@web.get("/")
def get_web(): ...
