from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ElevatorRequest(BaseModel):
    id: int
    timestamp: datetime
    origin_floor: int
    destination_floor: int
    status: str = "pending"  # pending, assigned, completed
    assigned_elevator_id: int | None = None
    pickup_time: Optional[datetime] = None
    dropoff_time: Optional[datetime] = None
