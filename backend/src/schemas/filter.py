from pydantic import BaseModel


class Skill(BaseModel):
    skillId: int
    skillName: str


class Category(BaseModel):
    categoryId: int
    categoryName: str


class Location(BaseModel):
    locationId: int
    locationName: str