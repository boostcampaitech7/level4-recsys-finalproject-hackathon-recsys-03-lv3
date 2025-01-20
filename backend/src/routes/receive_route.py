from fastapi import APIRouter

receive = APIRouter()

@receive.get("/")
def get_users():
    return {"message": "List of receives"}