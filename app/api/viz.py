from fastapi import APIRouter, Query, Depends
from sqlalchemy import func
from app.core.database import get_db
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional
from app.viz_specs import build_collisions_by_severity_spec, build_horizontal_bar_graph_spec, build_line_chart_spec


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
) -> dict:
    """
    Returns a Vega spec (JSON) with data embedded for collisions grouped by severity.
    """

    return build_collisions_by_severity_spec(
        db,
        location=location,
        start_date=start_date,
        end_date=end_date
    )


#/most-dangerous-addr @parameter -> addr_type intersection, block, mid
@router.get("/most-dangerous-intersections", response_model=None)
def most_dangerous_intersections(
    metric: str = Query("harm", pattern="^(harm|count)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> dict:
    """
    Returns a Vega spec (JSON) with data embedded for most dangerous intersections.
    """

    return build_horizontal_bar_graph_spec(
        db,
        address_type_name="Intersection",
        metric=metric,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/most-dangerous-blocks", response_model=None)
def most_dangerous_blocks(
    metric: str = Query("harm", pattern="^(harm|count)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> dict:
    """
    Returns a Vega spec (JSON) with data embedded for most dangerous blocks.
    """

    return build_horizontal_bar_graph_spec(
        db,
        address_type_name="Block",
        metric=metric,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )


# Need to address NULL locations to make this work
@router.get("/most-dangerous-alleys", response_model=None)
def most_dangerous_alleys(
    metric: str = Query("harm", pattern="^(harm|count)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> dict:
    """
    Returns a Vega spec (JSON) with data embedded for most dangerous alleys.
    """

    return build_horizontal_bar_graph_spec(
        db,
        address_type_name="Alley",
        metric=metric,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )

# Consolidate /most-dangerous-... into one endpoint, use parameter for determining ADDR_TYPE (INTERSECTION, ALLEY, BLOCK)

