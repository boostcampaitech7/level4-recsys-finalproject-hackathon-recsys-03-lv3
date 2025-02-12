from pydantic import BaseModel
from typing import List, Optional


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str
    userId: int
    userName: str
    userType: int


class FreelancerRegisterRequest(BaseModel):
    freelancerName: str
    email: str
    password: str
    workExp: int
    price: int
    workType: int
    role: str
    freelancerContent: Optional[str] = None
    locationId: int
    categoryList: List[int]
    skillList: List[int]


class CompanyRegisterRequest(BaseModel):
    companyName: str
    email: str
    companyContent: Optional[str] = None
    password: str
    locationId: int
