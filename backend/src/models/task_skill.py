from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base


class TaskSkill(Base):
    __tablename__ = "TASK_SKILL"

    task_id = Column("TASK_ID", Integer, ForeignKey("TASK.TASK_ID"), primary_key=True)
    project_id = Column("PROJECT_ID", Integer, ForeignKey("TASK.PROJECT_ID"), primary_key=True)
    skill_id = Column("SKILL_ID", Integer, ForeignKey("SKILL.SKILL_ID"), primary_key=True)

    # 관계 정의
    task = relationship(
        "Task",
        back_populates="task_skills",
        primaryjoin="and_(TaskSkill.task_id == Task.id, TaskSkill.project_id == Task.project_id)"
    )
    skill = relationship(
        "Skill",
        back_populates="task_skills",
        foreign_keys=[skill_id]
    )
