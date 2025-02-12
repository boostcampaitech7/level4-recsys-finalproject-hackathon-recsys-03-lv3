from typing import List, Optional, Union
from pydantic import BaseModel, validator

from src.utils.utils import parse_json_to_list


class ResourceListResponse(BaseModel):
    freelancerId: int
    freelancerName: str
    workExp: int
    price: Optional[int] = None
    workType: int
    role: str
    freelancerContent: Optional[str] = None
    locationName: str
    categoryList: List[str]
    skillList: List[str]
    skillScoreList: List[float]
    feedbackCount: Optional[int] = None
    feedbackScore: Optional[float] = None
    expertise: Optional[float] = None
    proactiveness: Optional[float] = None
    punctuality: Optional[float] = None
    communication: Optional[float] = None
    maintainability: Optional[float] = None
    matchingScore: Optional[float] = None
    applied: Optional[int] = None

    @validator("categoryList", "skillList", "skillScoreList", pre=True)
    def parse_skill_list(cls, value: str) -> List[Union[int, float, str]]:
        return parse_json_to_list(value)
