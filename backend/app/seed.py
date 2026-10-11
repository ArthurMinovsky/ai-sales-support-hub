from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Product

# Fictional demonstration catalog; never represent these as real Demo products.
SAMPLES = [
    {"name": "Demo Edge Vision Gateway", "brand": "ExampleTech", "description": "Fanless industrial vision gateway for edge inference with dual Ethernet ports.", "category": "Industrial AI", "type": "Gateway", "subtype": "Vision", "image_url": None},
    {"name": "Demo Sensor Monitor", "brand": "ExampleTech", "description": "Condition monitoring sensor for temperature and vibration in manufacturing plants.", "category": "Industrial IoT", "type": "Sensor", "subtype": "Monitoring", "image_url": None},
    {"name": "Demo Data Integration Hub", "brand": "ExampleWorks", "description": "Connects operational machine telemetry to business dashboards with secure APIs.", "category": "Software", "type": "Platform", "subtype": "Integration", "image_url": None},
]


def seed_demo_catalog(db: Session) -> None:
    if db.scalar(select(Product.id).limit(1)) is not None:
        return
    db.add_all(Product(**row) for row in SAMPLES)
    db.commit()
