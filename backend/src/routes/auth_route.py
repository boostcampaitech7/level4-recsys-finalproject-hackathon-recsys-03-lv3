from fastapi import APIRouter

auth = APIRouter()


@auth.get("/")
def get_users():
    return {"message": "List of auths"}
