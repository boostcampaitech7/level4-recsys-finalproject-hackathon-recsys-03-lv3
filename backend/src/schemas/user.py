from pydantic import BaseModel

# 요청 데이터
class UserLoginRequest(BaseModel):
    email: str
    password: str

# 응답 데이터
class UserLoginResponse(BaseModel):
    token: str
    user_id: int
    user_name: str
    team_id: int
    position_id: int