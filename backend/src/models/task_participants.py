from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base

class TaskParticipants(Base):
    __tablename__ = "TASK_PARTICIPANTS"

    task_id = Column("TASK_ID", Integer, ForeignKey("TASK.TASK_ID"), primary_key=True)
    project_id = Column("PROJECT_ID", Integer, ForeignKey("TASK.PROJECT_ID"), primary_key=True)
    user_id = Column("USER_ID", Integer, ForeignKey("USER.USER_ID"), primary_key=True)

    # 관계 정의
    task = relationship("Task", back_populates="task_participants")
    user = relationship("User", back_populates="task_participants")