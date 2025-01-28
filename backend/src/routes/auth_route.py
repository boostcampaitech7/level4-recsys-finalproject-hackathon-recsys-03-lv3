from fastapi import APIRouter

filter = APIRouter()


@filter.get("/")
def get_users():
    return {"message": "List of auths"}
