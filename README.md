Elevator System Simulation & Optimization
Overview
This project is a web-based elevator simulation system designed to model and optimize the operations of multiple elevators serving multiple floors in real time. The system focuses on request scheduling, passenger handling, and improving user-centric performance metrics such as wait time and travel time.

Built using React (frontend) and FastAPI (backend), the simulation displays elevator movements and state changes, and incorporates intelligent features like auto request generation, peak mode behavior, capacity constraints, utilization tracking, and smart idle positioning.

Features
Core Functionality
Multi-elevator simulation: Simulates multiple elevators (default: 3) across 10 floors.

Real-time visualization: Displays current floor, direction, door state, passenger count, and utilization of each elevator.

Dynamic request handling: Users or auto-generator can initiate requests between any floors.

Intelligent Scheduling
Requests are assigned based on:

Current elevator direction.

Proximity to request floor.

Elevator availability and capacity.

Request aging (requests waiting > 5s are prioritized).

Overcrowded elevators are avoided.

Starvation is prevented through priority escalation.

Metrics Dashboard
Displays:

Average wait time.

Average travel time.

Total requests generated.

Total requests completed.

Current simulation speed.

System Controls
Speed Control: Change simulation speed (1x, 2x, 5x).

Auto Request Generation:

Can be started/stopped at will.

Requests are randomly generated across floors.

Peak Mode:

Simulates 9 AM lobby rush: ~70% of requests originate from floor 0.

Disabling peak mode returns to uniform request generation.

Smart Idle Behavior:

When idle, elevators move toward their assigned preferred floors to anticipate future demand.

Technologies Used
Frontend: React.js

Backend: Python (FastAPI)

Async Engine: asyncio for event-driven simulation

Visualization: Live UI updates via polling /state and /status every second

Setup Instructions
Prerequisites
Node.js and npm

Python 3.8+

pip with FastAPI dependencies installed

Backend

cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Frontend

cd frontend
npm install
npm start

Frontend runs on http://localhost:3000
Backend runs on http://localhost:8000
