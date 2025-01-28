from fastapi import APIRouter

resource = APIRouter()


@resource.get("/")
def get_users():
    return {"message": "List of resources"}
