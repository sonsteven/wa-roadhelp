from fastapi import APIRouter, Query, Depends
from sqlalchemy import func
from app.core.database import get_db
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional
from pathlib import Path
import json

from app.models.severity import Severity
from app.models.traffic_collisions import TrafficCollision


router = APIRouter(
    prefix="/viz",
    tags=["Visualizations"]
)

@router.get("/collisions-by-severity", response_model=None)
def collisions_by_severity(
    location: Optional[str] = Query(None, description="Filter by location"),
    start_date: Optional[datetime] = Query(None, description="Filter by results after start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by results before end date"),
    db: Session = Depends(get_db)
    ):

    spec_path = Path(__file__).resolve().parents[1] / "vega_specs" / "collisions_by_severity.vega.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    query = db.query(TrafficCollision)

    if location:
        query = query.filter(TrafficCollision.location.ilike(f"%{location}%"))
    if start_date:
        query = query.filter(TrafficCollision.occurred_at >= start_date)
    if end_date:
        query = query.filter(TrafficCollision.occurred_at <= end_date)

    rows = (
        query.join(TrafficCollision.severity)
        .with_entities(
            Severity.code.label("severity_code"),
            Severity.desc.label("category"),
            func.count(TrafficCollision.id).label("amount")
        )
        .group_by(Severity.code, Severity.desc)
        .order_by(func.count(TrafficCollision.id).desc())
        .all()
    )

    values = [dict(r._mapping) for r in rows]

    dataset = next(d for d in spec["data"] if d.get("name") == "table")
    dataset["values"] = values

    return spec