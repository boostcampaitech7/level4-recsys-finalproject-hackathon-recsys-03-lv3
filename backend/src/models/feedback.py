from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base


class Feedback(Base):
    __tablename__ = "FEEDBACK"

    id = Column("FEEDBACK_ID", Integer, primary_key=True, index=True)
    score = Column("FEEDBACK_SCORE", Integer, nullable=False)
    content = Column("FEEDBACK_CONTENT", String(4000), nullable=False)

    # 외래 키
    project_id = Column("PROJECT_ID", Integer, ForeignKey("PROJECT.PROJECT_ID"), nullable=False)

    # 관계 정의
    project = relationship(
        "Project",
        back_populates="feedbacks",
        foreign_keys=[project_id]
    )
