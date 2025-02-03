from fastapi import APIRouter

project = APIRouter()


@project.get("/")
def get_users():
    return {"message": "List of projects"}
