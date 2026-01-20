from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base

class JunctionType(Base):
    __tablename__ = "junction_type"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(300), nullable=False, unique=True)

    collisions = relationship("TrafficCollision", back_populates="junction_type") 