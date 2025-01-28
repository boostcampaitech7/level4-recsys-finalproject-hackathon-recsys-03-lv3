from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base


class FreelancerSkill(Base):
    __tablename__ = "FREELANCER_SKILL"

    freelancer_id = Column("FREELANCER_ID", Integer, ForeignKey("FREELANCER.FREELANCER_ID"), primary_key=True)
    skill_id = Column("SKILL_ID", Integer, ForeignKey("SKILL.SKILL_ID"), primary_key=True)
    skill_score = Column("SKILL_SCORE", Float, nullable=False)

    # 관계 정의
    freelancer = relationship(
        "Freelancer",
        back_populates="skills",
        foreign_keys=[freelancer_id]
    )
    skill = relationship(
        "Skill",
        back_populates="freelancers",
        foreign_keys=[skill_id]
    )
