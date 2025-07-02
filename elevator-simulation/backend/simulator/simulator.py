from models.elevator import Elevator
from models.request import ElevatorRequest
import asyncio
from datetime import datetime
import random


class ElevatorSystem:
    def __init__(self):
        self.elevators = [Elevator(id=i) for i in range(3)]
        self.running = False
        self.requests = []
        self.request_id = 0
        self.speed_multiplier = 1.0
        self.metrics = {
            "wait_times": [],
            "travel_times": [],
        }
        self.auto_generate = False
        self.peak_mode = False
        self.assignment_logs = [] 

    def get_state(self):
        return {"elevators": [e.dict() for e in self.elevators]}

    def start_simulation(self):
        if not self.running:
            print("Simulation auto-started.")
            self.running = True
            loop = asyncio.get_running_loop()
            loop.create_task(self.simulate())

    async def simulate(self):
        while self.running:
            self.assign_requests()
            self.update_metrics()
            self.log_metrics()
            for elevator in self.elevators:
                elevator.step()
            await asyncio.sleep(1.0 / self.speed_multiplier)

    def update_metrics(self):
        for req in self.requests:
            if req.status == "assigned" and not req.pickup_time:
                elevator = next(
                    (e for e in self.elevators if e.id == req.assigned_elevator_id), None)
                if elevator and elevator.current_floor == req.origin_floor:
                    req.pickup_time = datetime.now()
                    wait = (req.pickup_time - req.timestamp).total_seconds()
                    self.metrics["wait_times"].append(wait)

            if req.pickup_time and not req.dropoff_time:
                elevator = next(
                    (e for e in self.elevators if e.id == req.assigned_elevator_id), None)
                if elevator and elevator.current_floor == req.destination_floor:
                    req.dropoff_time = datetime.now()
                    travel = (req.dropoff_time -
                              req.pickup_time).total_seconds()
                    self.metrics["travel_times"].append(travel)

    def get_metrics(self):
        def avg(lst):
            return round(sum(lst) / len(lst), 2) if lst else 0

        return {
            "average_wait_time": avg(self.metrics["wait_times"]),
            "average_travel_time": avg(self.metrics["travel_times"]),
            "total_requests": len(self.requests),
            "completed_requests": len(self.metrics["travel_times"]),
        }

    def add_request(self, origin, destination):
        req = ElevatorRequest(
            id=self.request_id,
            timestamp=datetime.now(),
            origin_floor=origin,
            destination_floor=destination,
        )
        self.requests.append(req)
        self.request_id += 1
        return req

    def assign_requests(self):
        now = datetime.now()
        unassigned = [r for r in self.requests if r.status == "pending"]

        for req in unassigned:
            waited_time = (now - req.timestamp).total_seconds()
            print(
                f"\nEvaluating Request {req.id} (from {req.origin_floor} → {req.destination_floor}, waited {round(waited_time, 1)}s)")

            best_elevator = None
            best_score = float("inf")

            for elevator in self.elevators:
                if elevator.current_passengers >= elevator.capacity:
                    continue

            # Base score is distance
                score = abs(elevator.current_floor - req.origin_floor)

            # Bias for idle elevators
                if elevator.direction == "idle":
                    score -= 1  # encourage idle

            # Penalize elevators already with long queues
                score += len(elevator.queue) * 0.5

                if score < best_score:
                    best_score = score
                    best_elevator = elevator

            if best_elevator:
                best_elevator.queue.append(req.origin_floor)
                best_elevator.queue.append(req.destination_floor)
                req.assigned_elevator_id = best_elevator.id
                req.status = "assigned"
                log = f"→ Request {req.id} assigned to Elevator {best_elevator.id} (waited {round(waited_time, 1)}s)"
                print(log)
                self.assignment_logs.append(log)

    async def configure(self, num_elevators: int):
        print(f"Reinitializing with {num_elevators} elevators...")
        self.stop()
        self.elevators = [Elevator(id=i) for i in range(num_elevators)]
        self.requests = []
        self.request_id = 0
        self.metrics = {
            "wait_times": [],
            "travel_times": [],
        }
        self.assignment_logs = []
        self.start_simulation()

    def stop(self):
        print("Simulation stopped.")
        self.running = False
        self.auto_generate = False

    def start(self):
        if not self.running:
            print("Simulation started.")
            self.running = True
            asyncio.create_task(self.simulate())

    def reset(self):
        print("System reset.")
        self.stop()
        self.elevators = [Elevator(id=i) for i in range(len(self.elevators))]
        self.requests = []
        self.request_id = 0
        self.metrics = {
            "wait_times": [],
            "travel_times": [],
        }
        self.assignment_logs = []

    def set_speed(self, speed: float):
        if speed > 0:
            self.speed_multiplier = speed
            print(f"Speed set to {speed}x")

    def start_auto_generate(self):
        self.auto_generate = True
        if not self.running:
            self.start()
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.create_task(self.generate_requests())
        print("Auto request generation started.")

    def stop_auto_generate(self):
        self.auto_generate = False
        print("Auto request generation stopped.")

    def enable_peak_mode(self):
        self.peak_mode = True
        print("Peak mode enabled (lobby requests).")
        for e in self.elevators:
            e.preferred_floor = 0

    def disable_peak_mode(self):
        self.peak_mode = False
        print("Peak mode disabled (normal distribution).")

        for i, e in enumerate(self.elevators):
            if e.queue:
                # Average of queued target floors
                e.preferred_floor = sum(e.queue) // len(e.queue)
            else:
                # Spread out across different default preferred floors
                # Elevator 0 → 2, 1 → 4, 2 → 6, etc.
                e.preferred_floor = min((i + 1) * 2, 9)

            print(
                f"Elevator {e.id} preferred_floor set to {e.preferred_floor}")

    async def generate_requests(self):
        num_floors = 10  # Static for now

        while self.auto_generate:
            if self.peak_mode:
                origin = 0 if random.random() < 0.7 else random.randint(1, num_floors - 1)
            else:
                origin = random.randint(0, num_floors - 1)

            dest = origin
            while dest == origin:
                dest = random.randint(0, num_floors - 1)

            self.add_request(origin, dest)
            await asyncio.sleep(random.uniform(1, 3))

    def log_metrics(self):
        m = self.get_metrics()
        print(f"[Speed: {self.speed_multiplier}x] [Metrics] Avg Wait: {m['average_wait_time']}s | Avg Travel: {m['average_travel_time']}s | Total: {m['total_requests']} | Completed: {m['completed_requests']}")


# Singleton instance
elevator_system = ElevatorSystem()
