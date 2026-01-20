from sqlalchemy import Integer, BigInteger,String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base

# Main Fact Table
class TrafficCollision(Base):
    __tablename__ = "traffic_collisions"

    __table_args__ = (
        # Data integrity constraints
        CheckConstraint("person_count IS NULL OR person_count >= 0", name="ck_person_count_nonneg"),
        CheckConstraint("ped_count IS NULL OR ped_count >= 0", name="ck_ped_count_nonneg"),
        CheckConstraint("pedcyl_count IS NULL OR pedcyl_count >= 0", name="ck_pedcyl_count_nonneg"),
        CheckConstraint("veh_count IS NULL OR veh_count >= 0", name="ck_veh_count_nonneg"),
        CheckConstraint("injuries IS NULL OR injuries >= 0", name="ck_injuries_nonneg"),
        CheckConstraint("serious_injuries IS NULL OR serious_injuries >= 0", name="ck_serious_injuries_nonneg"),
        CheckConstraint("fatalities IS NULL OR fatalities >= 0", name="ck_fatalities_nonneg"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inc_key: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)

    location: Mapped[str] = mapped_column(String(255), nullable=True)

    occurred_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    # Counts
    person_count: Mapped[int] = mapped_column(Integer, nullable=True)
    ped_count: Mapped[int] = mapped_column(Integer, nullable=True)
    pedcyl_count: Mapped[int] = mapped_column(Integer, nullable=True)
    veh_count: Mapped[int] = mapped_column(Integer, nullable=True)
    injuries: Mapped[int] = mapped_column(Integer, nullable=True)
    serious_injuries: Mapped[int] = mapped_column(Integer, nullable=True)
    fatalities: Mapped[int] = mapped_column(Integer, nullable=True)

    # Foreign Keys
    severity_id: Mapped[int] = mapped_column(ForeignKey("severity.id"), nullable=True, index=True)
    collision_type_id: Mapped[int] = mapped_column(ForeignKey("collision_type.id"), nullable=True, index=True)
    sdot_collision_type_id: Mapped[int] = mapped_column(ForeignKey("sdot_collision_type.id"), nullable=True, index=True)
    junction_type_id: Mapped[int] = mapped_column(ForeignKey("junction_type.id"), nullable=True, index=True)
    light_condition_id: Mapped[int] = mapped_column(ForeignKey("light_condition.id"), nullable=True, index=True)
    weather_condition_id: Mapped[int] = mapped_column(ForeignKey("weather_condition.id"), nullable=True, index=True)
    road_condition_id: Mapped[int] = mapped_column(ForeignKey("road_condition.id"), nullable=True, index=True)
    address_type_id: Mapped[int] = mapped_column(ForeignKey("address_type.id"), nullable=True, index=True)

    # Relationships
    severity = relationship("Severity", back_populates="collisions")
    collision_type = relationship("CollisionType", back_populates="collisions")
    sdot_collision_type = relationship("SDOTCollisionType", back_populates="collisions")
    junction_type = relationship("JunctionType", back_populates="collisions")
    light_condition = relationship("LightCondition", back_populates="collisions")
    weather_condition = relationship("WeatherCondition", back_populates="collisions")
    road_condition = relationship("RoadCondition", back_populates="collisions")
    address_type = relationship("AddressType", back_populates="collisions")