from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.db import Base


class Skill(Base):
    __tablename__ = "SKILL"

    id = Column("SKILL_ID", Integer, primary_key=True, index=True)
    name = Column("SKILL_NAME", String(100), nullable=False)

    # 관계 정의
    freelancers = relationship(
        "FreelancerSkill",
        back_populates="skill",
        foreign_keys="FreelancerSkill.skill_id"
    )
    projects = relationship(
        "ProjectSkill",
        back_populates="skill",
        foreign_keys="ProjectSkill.skill_id"
    )
