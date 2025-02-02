from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base


class Freelancer(Base):
    __tablename__ = "FREELANCER"

    id = Column("FREELANCER_ID", Integer, primary_key=True, index=True)
    name = Column("FREELANCER_NAME", String(100), nullable=False)
    email = Column("EMAIL", String(100), nullable=False, unique=True)
    password = Column("PASSWORD", String(100), nullable=False)
    work_exp = Column("WORK_EXP", Integer, nullable=False)
    price = Column("PRICE", Integer, nullable=False)
    work_type = Column("WORK_TYPE", Integer, nullable=False)
    role = Column("ROLE", String(100), nullable=False)
    content = Column("FREELANCER_CONTENT", Text)

    # 외래 키
    location_id = Column("LOCATION_ID", Integer, ForeignKey("LOCATION.LOCATION_ID"), nullable=False)

    # 관계 정의
    location = relationship(
        "Location",
        back_populates="freelancers",
        foreign_keys=[location_id]
    )
    categories = relationship(
        "FreelancerCategory",
        back_populates="freelancer",
        foreign_keys="FreelancerCategory.freelancer_id"
    )
    projects = relationship(
        "Project",
        back_populates="freelancer",
        foreign_keys="Project.freelancer_id"
    )
    skills = relationship(
        "FreelancerSkill",
        back_populates="freelancer",
        foreign_keys="FreelancerSkill.freelancer_id"
    )
    rankings = relationship(
        "ProjectRanking",
        back_populates="freelancer",
        foreign_keys="ProjectRanking.freelancer_id"
    )
    feedbacks = relationship(
        "Feedback",
        back_populates="freelancer",
        foreign_keys="Feedback.freelancer_id"
    )
