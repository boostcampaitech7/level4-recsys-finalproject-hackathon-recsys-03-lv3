from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base


class Company(Base):
    __tablename__ = "COMPANY"

    id = Column("COMPANY_ID", Integer, primary_key=True, index=True)
    name = Column("COMPANY_NAME", String(100), nullable=False)
    email = Column("EMAIL", String(100), nullable=False, unique=True)
    password = Column("PASSWORD", String(100), nullable=False)

    # 외래 키
    location_id = Column("LOCATION_ID", Integer, ForeignKey("LOCATION.LOCATION_ID"), nullable=False)

    # 관계 정의
    location = relationship(
        "Location",
        back_populates="companies",
        foreign_keys=[location_id]
    )
    projects = relationship(
        "Project",
        back_populates="company",
        foreign_keys="Project.company_id"
    )
