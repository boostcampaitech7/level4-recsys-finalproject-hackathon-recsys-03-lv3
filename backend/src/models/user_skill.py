from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base


class UserSkill(Base):
    __tablename__ = "USER_SKILL"

    user_id = Column("USER_ID", Integer, ForeignKey("USER.USER_ID"), primary_key=True)
    skill_id = Column("SKILL_ID", Integer, ForeignKey("SKILL.SKILL_ID"), primary_key=True)

    # 관계 정의
    user = relationship(
        "User",
        back_populates="user_skills",
        foreign_keys=[user_id]
    )
    skill = relationship(
        "Skill",
        back_populates="user_skills",
        foreign_keys=[skill_id]
    )
