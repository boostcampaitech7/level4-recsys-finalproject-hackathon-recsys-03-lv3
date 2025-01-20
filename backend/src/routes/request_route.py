from fastapi import APIRouter

request = APIRouter()

@request.get("/")
def get_users():
    return {"message": "List of requests"}