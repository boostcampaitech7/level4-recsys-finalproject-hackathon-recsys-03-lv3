from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.db import Base


class Category(Base):
    __tablename__ = "CATEGORY"

    id = Column("CATEGORY_ID", Integer, primary_key=True, index=True)
    name = Column("CATEGORY_NAME", String(100), nullable=False)

    # 관계 정의
    freelancers = relationship(
        "FreelancerCategory",
        back_populates="category",
        foreign_keys="FreelancerCategory.category_id"
    )
    projects = relationship(
        "Project",
        back_populates="category",
        foreign_keys="Project.category_id"
    )
