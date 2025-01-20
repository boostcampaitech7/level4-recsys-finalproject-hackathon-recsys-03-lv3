from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base

class Task(Base):
    __tablename__ = "TASK"

    project_id = Column("PROJECT_ID", Integer, ForeignKey("PROJECT.PROJECT_ID"), primary_key=True)
    id = Column("TASK_ID", Integer, primary_key=True, index=True)
    name = Column("TASK_NAME", String(100), nullable=False)
    size = Column("TASK_SIZE", Integer, nullable=False)

    # 관계 정의
    project = relationship("Project", back_populates="tasks")
    task_rankings = relationship("TaskRanking", back_populates="task")
    task_participants = relationship("TaskParticipants", back_populates="task")
    task_skills = relationship("TaskSkill", back_populates="task")