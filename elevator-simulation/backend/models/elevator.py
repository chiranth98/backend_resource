from pydantic import BaseModel

class Elevator(BaseModel):
    id: int
    current_floor: int = 1
    direction: str = "idle"  # 'up', 'down', or 'idle'
    queue: list[int] = []

    def step(self):
        if not self.queue:
            self.direction = "idle"
            return

        target = self.queue[0]
        if self.current_floor < target:
            self.current_floor += 1
            self.direction = "up"
        elif self.current_floor > target:
            self.current_floor -= 1
            self.direction = "down"
        else:
            self.queue.pop(0)  # Arrived at destination
            self.direction = "idle"
        print(f"Elevator {self.id} at floor {self.current_floor}, heading to {target}")


