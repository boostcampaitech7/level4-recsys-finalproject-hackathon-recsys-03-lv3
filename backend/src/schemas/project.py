from typing import List, Optional, Union
from pydantic import BaseModel, validator

from src.utils.utils import parse_json_to_list


class ProjectRequest(BaseModel):
    projectName: str
    duration: int
    budget: int
    workType: int
    contractType: int
    priority: int
    projectContent: str
    categoryId: int
    skillList: List[int]


class FeedbackRequest(BaseModel):
    projectId: int
    freelancerId: int
    expertise: float
    proactiveness: float
    punctuality: float
    communication: float
    maintainability: float
    feedbackContent: str
    skillIdList: List[int]


class ProjectListResponse(BaseModel):
    projectId: int
    projectName: str
    duration: int
    budget: int
    workType: int
    contractType: int
    status: int
    registerDate: str
    categoryName: str
    skillIdList: List[int]
    skillNameList: List[str]
    locationName: str
    matchingScore: Optional[float] = None
    applied: Optional[int] = None
    similarityScore: Optional[int] = None
    priority: Optional[int] = None

    @validator("skillIdList", "skillNameList", pre=True)
    def parse_skill_list(cls, value: str) -> List[Union[int, float, str]]:
        return parse_json_to_list(value)


class ProjectDetailResponse(BaseModel):
    projectId: int
    projectName: str
    duration: int
    budget: int
    workType: int
    contractType: int
    priority: int
    projectContent: str
    status: int
    registerDate: str
    categoryId: int
    categoryName: str
    skillList: List[str]
    companyId: int
    companyName: str
    locationName: str

    @validator("skillList", pre=True)
    def parse_skill_list(cls, value: str) -> List[Union[int, float, str]]:
        return parse_json_to_list(value)


class ProjectFeedbackResponse(BaseModel):
    projectId: int
    projectName: str
    duration: int
    budget: int
    workType: int
    contractType: int
    status: int
    registerDate: str
    companyName: str
    skillIdList: List[int]
    skillNameList: List[str]
    feedbackScore: float
    expertise: Optional[float] = None
    proactiveness: Optional[float] = None
    punctuality: Optional[float] = None
    communication: Optional[float] = None
    maintainability: Optional[float] = None
    feedbackContent: Optional[str] = None

    @validator("skillIdList", "skillNameList", pre=True)
    def parse_skill_list(cls, value: str) -> List[Union[int, float, str]]:
        return parse_json_to_list(value)


class CompanyResponse(BaseModel):
    companyId: int
    companyName: str
    companyContent: str
    locationName: str


class ProjectProgressResponse(BaseModel):
    projectCount: int
    ongoingCount: int
    completedCount: int
