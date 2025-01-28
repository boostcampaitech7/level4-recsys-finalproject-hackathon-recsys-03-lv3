from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base


class ProjectSkill(Base):
    __tablename__ = "PROJECT_SKILL"

    project_id = Column("PROJECT_ID", Integer, ForeignKey("PROJECT.PROJECT_ID"), primary_key=True)
    skill_id = Column("SKILL_ID", Integer, ForeignKey("SKILL.SKILL_ID"), primary_key=True)

    # 관계 정의
    project = relationship(
        "Project",
        back_populates="skills",
        foreign_keys=[project_id]
    )
    skill = relationship(
        "Skill",
        back_populates="projects",
        foreign_keys=[skill_id]
    )
