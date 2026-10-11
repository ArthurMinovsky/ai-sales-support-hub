from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Product

# Synthetic internal catalog for the project workspace. Product families and
# names are fictional Sales Support Hub-style examples, not real offerings.
SAMPLES = [
    {
        "name": "VisionScan IQ-200 Edge Vision Gateway",
        "brand": "Demo Sensors",
        "description": "Fanless IP67 edge gateway for machine-vision inference on the production line. Dual GbE with PoE, supports RTSP and GigE Vision inputs, runs detection models locally with sub-150 ms latency.",
        "category": "Industrial AI",
        "type": "Edge Gateway",
        "subtype": "Machine Vision",
        "image_url": None,
    },
    {
        "name": "VisionScan IQ-450 Vision Analytics Server",
        "brand": "Demo Sensors",
        "description": "Rack server for multi-camera visual inspection across up to 32 concurrent streams. GPU-accelerated defect classification, REST and MQTT event output, and a web console for model rollout.",
        "category": "Industrial AI",
        "type": "Analytics Server",
        "subtype": "Visual Inspection",
        "image_url": None,
    },
    {
        "name": "VibeSense VM-40 Wireless Vibration Monitor",
        "brand": "Demo Sensors",
        "description": "Tri-axial MEMS vibration sensor with 3-year battery life and LoRaWAN connectivity for rotating equipment. Streams RMS velocity, acceleration envelope, and temperature for predictive maintenance.",
        "category": "Industrial IoT",
        "type": "Wireless Sensor",
        "subtype": "Condition Monitoring",
        "image_url": None,
    },
    {
        "name": "ThermoNode TN-12 Environmental Sensor Node",
        "brand": "Demo Sensors",
        "description": "IP65 environmental node measuring temperature, humidity, and differential pressure for cleanrooms and cold chains. Modbus RTU and MQTT output, calibrated at factory with a 12-month certificate.",
        "category": "Industrial IoT",
        "type": "Sensor Node",
        "subtype": "Environmental",
        "image_url": None,
    },
    {
        "name": "FlowBridge FDX Data Integration Platform",
        "brand": "Demo Automation",
        "description": "Industrial data platform that connects PLC, historian, and MES sources into a governed pipeline. 90+ connectors including OPC UA and Siemens S7, with schema mapping, buffering, and store-and-forward.",
        "category": "Data & Integration",
        "type": "Platform",
        "subtype": "Data Integration",
        "image_url": None,
    },
    {
        "name": "FlowBridge StreamPipe Realtime ETL",
        "brand": "Demo Automation",
        "description": "Low-latency stream processing add-on for FlowBridge that transforms and routes telemetry at up to 50k events per second per node. Supports windowed aggregation, filtering, and Kafka or MQTT sinks.",
        "category": "Data & Integration",
        "type": "Software Module",
        "subtype": "Stream Processing",
        "image_url": None,
    },
    {
        "name": "DocuMind IDP Intelligent Document Processing",
        "brand": "Demo Automation",
        "description": "Document AI service that classifies, extracts, and validates fields from invoices, purchase orders, and customs forms. LLM-assisted extraction with human-in-the-loop review and confidence scoring.",
        "category": "Intelligent Automation",
        "type": "Document AI",
        "subtype": "Data Extraction",
        "image_url": None,
    },
    {
        "name": "AssistDesk AI Customer Support Copilot",
        "brand": "Demo Automation",
        "description": "Retrieval-augmented copilot for support agents that drafts replies from the knowledge base and product catalog. Includes citation of source documents, tone controls, and full conversation audit logs.",
        "category": "Intelligent Automation",
        "type": "Copilot",
        "subtype": "Customer Support",
        "image_url": None,
    },
    {
        "name": "PredictIQ Maintenance Analytics Suite",
        "brand": "Demo Automation",
        "description": "Analytics suite that turns vibration, temperature, and process signals into failure-risk scores for critical assets. Includes anomaly baselining, work-order triggers via REST, and explainable alerts.",
        "category": "Industrial AI",
        "type": "Analytics Suite",
        "subtype": "Predictive Maintenance",
        "image_url": None,
    },
    {
        "name": "GateLink OPC UA Edge Connector",
        "brand": "Demo Sensors",
        "description": "Protocol converter that exposes legacy PLC registers as secure OPC UA and MQTT topics. DIN-rail mounted, TLS 1.3 support, and store-and-forward buffering for unstable plant networks.",
        "category": "Industrial IoT",
        "type": "Protocol Converter",
        "subtype": "Connectivity",
        "image_url": None,
    },
]


def seed_demo_catalog(db: Session) -> None:
    if db.scalar(select(Product.id).limit(1)) is not None:
        return
    db.add_all(Product(**row) for row in SAMPLES)
    db.commit()
