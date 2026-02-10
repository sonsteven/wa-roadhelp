import json
from pathlib import Path
from typing import Literal, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.address_type import AddressType
from app.models.severity import Severity
from app.models.traffic_collisions import TrafficCollision


def load_vega_spec(filename: str) -> dict:
    """
    Load a Vega JSON spec template from `app\vega_specs\`.
    """
    spec_path = Path(__file__).resolve().parent / "vega_specs" / filename
    return json.loads(spec_path.read_text(encoding="utf-8"))


def inject_values(spec: dict, values: list[dict]) -> dict:
    """
    Inject data values in to Vega dataset "tables".
    """
    dataset = next(d for d in spec.get("data", []) if d.get("name") == "table")
    dataset["values"] = values
    return spec


def build_collisions_by_severity_spec(
        db: Session,
        location: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
) -> dict:
    """
    Build bar chart with collisions data grouped by severity.
    """
    spec = load_vega_spec("collisions_by_severity.vega.json")

    # Query collisions, then optionally apply filters
    query = db.query(TrafficCollision)
    if location:
        query = query.filter(TrafficCollision.location.ilike(f"%{location}%"))
    if start_date:
        query = query.filter(TrafficCollision.occurred_at >= start_date)
    if end_date:
        query = query.filter(TrafficCollision.occurred_at <= end_date)

    # Group and count by severity
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

    return inject_values(spec, values)


def build_horizontal_bar_graph_spec(
    db: Session,
    *,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    address_type_name: str,
    metric: Literal["harm", "count"] = "harm",
    limit: int
) -> dict:
    """
    Build "top N locations" horizontal bar chart.
    - If address_type_name == "Intersection": grouped by int_key
    - Otherwise: group by location text
    """
    spec = load_vega_spec("horizontal_bar_graph.vega.json")

    # Query restricted to address type name
    query = (
        db.query(TrafficCollision)
        .join(TrafficCollision.address_type)
        .filter(AddressType.name == address_type_name)
    )

    if start_date:
        query = query.filter(TrafficCollision.occurred_at >= start_date)
    if end_date:
        query = query.filter(TrafficCollision.occurred_at <= end_date)

    # Aggregates for calculating metrics
    collision_count = func.count(TrafficCollision.id)
    injuries_total = func.coalesce(func.sum(TrafficCollision.injuries), 0)
    serious_injuries_total = func.coalesce(func.sum(TrafficCollision.serious_injuries), 0)
    fatalities_total = func.coalesce(func.sum(TrafficCollision.fatalities), 0)

    # Weighted "harm score", numbers easily adjustable
    harm_score = (
        fatalities_total * 5
        + serious_injuries_total * 3
        + injuries_total * 2
        + collision_count * 1
    )

    # Metric determining y-axis data
    amount_expr = collision_count if metric == "count" else harm_score

    # Intersections grouped by int_key
    if address_type_name.strip().lower() == "intersection":
        query = query.filter(TrafficCollision.int_key.isnot(None))

        rows = (
            query.with_entities(
                TrafficCollision.int_key.label("int_key"),
                func.max(TrafficCollision.location).label("category"),
                amount_expr.label("amount"),
            )
            .group_by(TrafficCollision.int_key)
            .order_by(amount_expr.desc())
            .limit(limit)
            .all()
        )
    # Non-intersections grouped by location.    
    else:
        # Drop NULL locations.
        query = query.filter(TrafficCollision.location.isnot(None))

        rows = (
            query.with_entities(
                TrafficCollision.location.label("category"),
                amount_expr.label("amount"),
            )
            .group_by(TrafficCollision.location)
            .order_by(amount_expr.desc())
            .limit(limit)
            .all()
        )

    values = [dict(r._mapping) for r in rows]

    return inject_values(spec, values)


