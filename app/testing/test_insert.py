from datetime import datetime
from app.core.database import SessionLocal
from app.models.traffic_collisions import TrafficCollision
from app.models.severity import Severity
from app.models.collision_type import CollisionType

def insert_test_data():
    severity = Severity(code="1", desc="Property Damage")
    collision_type = CollisionType(code="2", desc="Parked Car Hit")

    # Open new session and create new collision object
    with SessionLocal() as session:
        collision = TrafficCollision(
            location="Port Orchard Ave",
            severity="Property Damage",
            inc_key=999999999999,
            occurred_at=datetime(2026, 1, 14, 14, 0),
            severity_id=severity.id,
            collision_type_id=collision_type.id
        )

        # Add to session for insertion
        session.add(collision)

        # Commit transaction
        session.commit()

        print(f"Inserted collision with ID: {collision.id}")

        # Retrieve all collisions
        all_collisions = session.query(TrafficCollision).all()

        for coll in all_collisions:
            print(coll.id, coll.inc_key, coll.location, coll.severity_id, coll.collision_type_id, coll.occurred_at)



if __name__ == "__main__":
    insert_test_data()