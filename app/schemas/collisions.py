from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class SeverityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    desc: Optional[str] = None

class CollisionTypeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class SDOTCollisionTypeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    desc: Optional[str] = None

class AddressTypeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class JunctionTypeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class RoadConditionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class LightConditionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class WeatherConditionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class TrafficCollisionOut(BaseModel):
    """
    Full collision representation for detailed endpoints.
    Expands all lookup relationships.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
    inc_key: int
    location: Optional[str] = None
    occurred_at: datetime

    # Counts
    person_count: Optional[int] = None
    ped_count: Optional[int] = None
    pedcyl_count: Optional[int] = None
    veh_count: Optional[int] = None
    injuries: Optional[int] = None
    serious_injuries: Optional[int] = None
    fatalities: Optional[int] = None

    # Foreign Keys
    severity_id: Optional[int] = None
    collision_type_id: Optional[int] = None
    sdot_collision_type_id: Optional[int] = None
    junction_type_id: Optional[int] = None
    light_condition_id: Optional[int] = None
    weather_condition_id: Optional[int] = None
    road_condition_id: Optional[int] = None
    address_type_id: Optional[int] = None

    # Response models
    severity: Optional[SeverityOut] = None
    collision_type: Optional[CollisionTypeOut] = None
    sdot_collision_type: Optional[SDOTCollisionTypeOut] = None
    junction_type: Optional[JunctionTypeOut] = None
    light_condition: Optional[LightConditionOut] = None
    weather_condition: Optional[WeatherConditionOut] = None
    road_condition: Optional[RoadConditionOut] = None
    address_type: Optional[AddressTypeOut] = None

class TrafficCollisionListOut(BaseModel):
    """
    Lean collision representation for list endpoints.
    Includes only severity and collision type nested lookups.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
    inc_key: int
    location: Optional[str] = None
    occurred_at: datetime
    
    person_count: Optional[int] = None
    ped_count: Optional[int] = None
    pedcyl_count: Optional[int] = None
    veh_count: Optional[int] = None
    injuries: Optional[int] = None
    serious_injuries: Optional[int] = None
    fatalities: Optional[int] = None

    severity_id: Optional[int] = None
    collision_type_id: Optional[int] = None

    severity: Optional[SeverityOut] = None
    collision_type: Optional[CollisionTypeOut] = None

class PaginatedCollisionsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    limit: int
    offset: int
    items: list[TrafficCollisionListOut]