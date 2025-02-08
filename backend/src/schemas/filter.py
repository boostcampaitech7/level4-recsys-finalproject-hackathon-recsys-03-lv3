from pydantic import BaseModel


class SkillResponse(BaseModel):
    skillId: int
    skillName: str


class CategoryResponse(BaseModel):
    categoryId: int
    categoryName: str


class LocationResponse(BaseModel):
    locationId: int
    locationName: str
