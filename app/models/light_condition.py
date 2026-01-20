from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base

class LightCondition(Base):
    __tablename__ = "light_condition"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(300), nullable=False, unique=True)

    collisions = relationship("TrafficCollision", back_populates="light_condition") 