from app.core.database import engine
from app.core.base import Base

import app.models.traffic_collisions
import app.models.collision_type
import app.models.severity
import app.models.sdot_collision_type
import app.models.junction_type
import app.models.light_condition
import app.models.weather_condition
import app.models.road_condition
import app.models.address_type

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()