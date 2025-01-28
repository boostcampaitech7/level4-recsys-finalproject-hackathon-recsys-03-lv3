from fastapi import APIRouter

mymony = APIRouter()


@mymony.get("/")
def get_users():
    return {"message": "List of mymonies"}
