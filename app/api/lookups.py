from fastapi import APIRouter, Depends
from app.schemas.collisions import SeverityOut, CollisionTypeOut, SDOTCollisionTypeOut, JunctionTypeOut, LightConditionOut, WeatherConditionOut, RoadConditionOut, AddressTypeOut
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.models import Severity, CollisionType, SDOTCollisionType, JunctionType, LightCondition, WeatherCondition, RoadCondition, AddressType

router = APIRouter(
    prefix="/lookups",
    tags=["Lookups"]
)

@router.get("/severities", response_model=list[SeverityOut], response_model_exclude_none=True)
def list_severities(db: Session = Depends(get_db)):
    return db.query(Severity).order_by(Severity.code.asc()).all()

@router.get("/collision-types", response_model=list[CollisionTypeOut], response_model_exclude_none=True)
def list_collision_types(db: Session = Depends(get_db)):
    return db.query(CollisionType).order_by(CollisionType.name.asc()).all()

@router.get("/sdot_collision_types", response_model=list[SDOTCollisionTypeOut], response_model_exclude_none=True)
def list_sdot_collision_types(db: Session = Depends(get_db)):
    return db.query(SDOTCollisionType).order_by(SDOTCollisionType.code.asc()).all()

@router.get("/junction-types", response_model=list[JunctionTypeOut], response_model_exclude_none=True)
def list_junction_types(db: Session = Depends(get_db)):
    return db.query(JunctionType).order_by(JunctionType.name.asc()).all()


@router.get("/light-conditions", response_model=list[LightConditionOut], response_model_exclude_none=True)
def list_light_conditions(db: Session = Depends(get_db)):
    return db.query(LightCondition).order_by(LightCondition.name.asc()).all()


@router.get("/weather-conditions", response_model=list[WeatherConditionOut], response_model_exclude_none=True)
def list_weather_conditions(db: Session = Depends(get_db)):
    return db.query(WeatherCondition).order_by(WeatherCondition.name.asc()).all()


@router.get("/road-conditions", response_model=list[RoadConditionOut], response_model_exclude_none=True)
def list_road_conditions(db: Session = Depends(get_db)):
    return db.query(RoadCondition).order_by(RoadCondition.name.asc()).all()

@router.get("/address-types", response_model=list[AddressTypeOut], response_model_exclude_none=True)
def list_address_types(db: Session = Depends(get_db)):
    return db.query(AddressType).order_by(AddressType.name.asc()).all()