from fastapi import FastAPI, HTTPException  # Creates API routes and handles API errors
from fastapi.middleware.cors import CORSMiddleware  # Allows React to access the API
from pydantic import BaseModel  # Validates incoming request data

from database import (
    get_devices,
    add_device,
    get_incidents,
    update_incident_status,
    get_incident_stats,
    get_topology
)  # Handles database operations

from monitor import monitor_all_devices, discover_all_routes  # Runs monitoring and route discovery


app = FastAPI(title="NetOps Incident Monitor")


# Allows the React development server to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Defines data required to add a device
class DeviceCreate(BaseModel):
    name: str
    host: str
    port: int
    service: str
    location: str


# Defines data required when changing a ticket status
class StatusUpdate(BaseModel):
    status: str


# Verifies that the API is running
@app.get("/")
def home():
    return {"message": "NetOps Incident Monitor API is running"}


# Returns all registered devices
@app.get("/devices")
def devices():
    return get_devices()


# Adds a new device to the monitoring inventory
@app.post("/devices")
def create_device(data: DeviceCreate):
    device_id = add_device(
        data.name,
        data.host,
        data.port,
        data.service,
        data.location
    )

    return {
        "message": "Device added successfully",
        "device_id": device_id
    }


# Returns all incident tickets
@app.get("/incidents")
def incidents():
    return get_incidents()


# Returns incident statistics
@app.get("/stats")
def stats():
    return get_incident_stats()


# Returns configured topology and discovered network paths
@app.get("/topology")
def topology():
    return get_topology()


# Runs one network monitoring cycle
@app.post("/scan")
def scan():
    monitor_all_devices()

    return {"message": "Network scan completed"}


# Automatically discovers network paths
@app.post("/discover")
def discover():
    discover_all_routes()

    return {"message": "Network path discovery completed"}


# Changes an incident ticket's status
@app.put("/incidents/{incident_id}/status")
def change_status(incident_id: int, data: StatusUpdate):
    status = data.status.upper()

    if status not in ["OPEN", "ACKNOWLEDGED", "RESOLVED"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be OPEN, ACKNOWLEDGED, or RESOLVED"
        )

    updated = update_incident_status(incident_id, status)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return {
        "message": "Incident status updated",
        "incident_id": incident_id,
        "status": status
    }

