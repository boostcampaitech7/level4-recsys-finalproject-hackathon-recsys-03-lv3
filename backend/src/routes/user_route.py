from fastapi import APIRouter

user = APIRouter()

@user.get("/")
def get_users():
    return {"message": "List of users"}