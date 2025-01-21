from pydantic import BaseModel


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserLoginResponse(BaseModel):
    token: str
    user_id: int
    user_name: str
    team_id: int
    position_id: int
