from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from simulator.simulator import elevator_system

router = APIRouter()

class RequestPayload(BaseModel):
    origin_floor: int
    destination_floor: int

class ConfigPayload(BaseModel):
    num_elevators: int

class SpeedPayload(BaseModel):
    speed: float

@router.post("/speed")
def set_speed(payload: SpeedPayload):
    elevator_system.set_speed(payload.speed)
    return {"status": f"Speed set to {payload.speed}x"}

@router.post("/config")
async def update_config(payload: ConfigPayload):
    await elevator_system.configure(payload.num_elevators)
    return {"status": "updated", "count": payload.num_elevators}

@router.post("/request")
def create_elevator_request(payload: RequestPayload):
    req = elevator_system.add_request(payload.origin_floor, payload.destination_floor)
    return {"status": "ok", "request_id": req.id}

@router.get("/state")
def get_elevator_state():
    return elevator_system.get_state()


@router.post("/auto-generate/start")
def start_auto_requests(background_tasks: BackgroundTasks):
    background_tasks.add_task(elevator_system.start_auto_generate)
    return {"status": "auto generation started"}

@router.post("/auto-generate/stop")
def stop_auto_requests():
    elevator_system.stop_auto_generate()
    return {"status": "auto generation stopped"}

@router.post("/auto-generate/peak-mode")
def enable_peak_mode():
    elevator_system.enable_peak_mode()
    return {"status": "peak mode ON"}

@router.post("/auto-generate/normal-mode")
def disable_peak_mode():
    elevator_system.disable_peak_mode()
    return {"status": "peak mode OFF"}

@router.get("/metrics")
def fetch_metrics():
    return elevator_system.get_metrics()


# @router.post("/start")
# def start_simulation():
#     elevator_system.start()
#     return {"status": "started"}

@router.post("/start")
def start_simulation(background_tasks: BackgroundTasks):
    background_tasks.add_task(elevator_system.start)
    return {"status": "started"}

@router.post("/stop")
def stop_simulation():
    elevator_system.stop()
    return {"status": "stopped"}

@router.post("/reset")
def reset_simulation():
    elevator_system.reset()
    return {"status": "reset"}

