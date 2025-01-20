from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.db import Base

class Role(Base):
    __tablename__ = "ROLE"

    id = Column("ROLE_ID", Integer, primary_key=True, index=True)
    name = Column("ROLE_NAME", String(100), nullable=False)

    # 관계 정의
    users = relationship("User", back_populates="role")