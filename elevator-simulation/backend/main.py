from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from simulator.simulator import elevator_system

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def start_sim():
    elevator_system.start_simulation()

@app.get("/")
def health():
    return {"status": "running"}
