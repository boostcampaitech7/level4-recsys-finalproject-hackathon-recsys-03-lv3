from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base


class Feedback(Base):
    __tablename__ = "FEEDBACK"

    id = Column("FEEDBACK_ID", Integer, primary_key=True, index=True)
    expertise = Column("EXPERTISE", Float, nullable=False)
    proactiveness = Column("PROACTIVENESS", Float, nullable=False)
    punctuality = Column("PUNCTUALITY", Float, nullable=False)
    communication = Column("COMMUNICATION", Float, nullable=False)
    maintainability = Column("MAINTAINABILITY", Float, nullable=False)
    content = Column("FEEDBACK_CONTENT", String(4000), nullable=False)

    # 외래 키
    project_id = Column("PROJECT_ID", Integer, ForeignKey("PROJECT.PROJECT_ID"), nullable=False)
    freelancer_id = Column("FREELANCER_ID", Integer, ForeignKey("FREELANCER.FREELANCER_ID"), nullable=False)

    # 관계 정의
    project = relationship(
        "Project",
        back_populates="feedbacks",
        foreign_keys=[project_id]
    )
    freelancer = relationship(
        "Freelancer",
        back_populates="feedbacks",
        foreign_keys=[freelancer_id]
    )
