from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class CollisionStatsSummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total_collisions: int
    total_fatalities: int
    total_injuries: int
    total_serious_injuries: int
    occurred_at_min: Optional[datetime] = None
    occurred_at_max: Optional[datetime] = None

class CollisionsStatsBySeverityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    severity_id: int
    severity_code: str
    severity_desc: Optional[str] = None
    total_collisions: int

