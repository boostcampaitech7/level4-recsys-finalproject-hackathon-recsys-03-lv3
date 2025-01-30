from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base


class FreelancerCategory(Base):
    __tablename__ = "FREELANCER_CATEGORY"

    freelancer_id = Column("FREELANCER_ID", Integer, ForeignKey("FREELANCER.FREELANCER_ID"), primary_key=True)
    category_id = Column("CATEGORY_ID", Integer, ForeignKey("CATEGORY.CATEGORY_ID"), primary_key=True)

    # 관계 정의
    freelancer = relationship(
        "Freelancer",
        back_populates="categories",
        foreign_keys=[freelancer_id]
    )
    category = relationship(
        "Category",
        back_populates="freelancers",
        foreign_keys=[category_id]
    )
