from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base

class AddressType(Base):
    __tablename__ = "address_type"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(12), nullable=False, unique=True)

    collisions = relationship("TrafficCollision", back_populates="address_type") 