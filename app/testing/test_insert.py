from datetime import datetime
from app.core.database import SessionLocal
from app.models.traffic_collisions import TrafficCollision

def insert_test_data():
    # Open new session and create new collision object
    with SessionLocal() as session:
        collision = TrafficCollision(
            county="King",
            severity="Fatal",
            occurred_at=datetime(2026, 1, 14, 14, 0)
        )

        # Add to session for insertion
        session.add(collision)

        # Commit transaction
        session.commit()

        print(f"Inserted collision with ID: {collision.id}")

        # Retrieve all collisions
        all_collisions = session.query(TrafficCollision).all()

        for coll in all_collisions:
            print(coll.id, coll.county, coll.severity, coll.occurred_at)



if __name__ == "__main__":
    insert_test_data()