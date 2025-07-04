class Elevator:
    def __init__(self, id, capacity=6):
        self.id = id
        self.current_floor = 0
        self.direction = "idle"
        self.queue = []
        self.door_state = "closed"
        self.current_passengers = 0
        self.capacity = capacity
        self.door_timer = 0
        self.total_ticks = 0
        self.active_ticks = 0
        self.preferred_floor = 0
        self.dropoff_map = {}  # floor -> number of passengers to drop at that floor

    def dict(self):
        return {
            "id": self.id,
            "current_floor": self.current_floor,
            "direction": self.direction,
            "queue": self.queue,
            "door_state": self.door_state,
            "current_passengers": self.current_passengers,
            "passenger_destinations": self.dropoff_map,
            "capacity": self.capacity,
            "utilization": round((self.active_ticks / self.total_ticks) * 100, 1) if self.total_ticks else 0,
            "preferred_floor": self.preferred_floor,
        }

    def step(self):
        self.total_ticks += 1

        if self.door_state == "open":
            if self.door_timer > 0:
                self.door_timer -= 1
                return
            else:
                self.door_state = "closed"
                return

        if self.queue:
            self.active_ticks += 1
            target = self.queue[0]
            if self.current_floor < target:
                self.current_floor += 1
                self.direction = "up"
            elif self.current_floor > target:
                self.current_floor -= 1
                self.direction = "down"
            else:
                # Arrived at target floor
                self.queue.pop(0)
                self.door_state = "open"
                self.door_timer = 1

                # Drop off
                if self.current_floor in self.dropoff_map:
                    self.current_passengers -= self.dropoff_map[self.current_floor]
                    del self.dropoff_map[self.current_floor]
                    self.current_passengers = max(0, self.current_passengers)

        else:
            if self.current_floor < self.preferred_floor:
                self.current_floor += 1
                self.direction = "up"
                self.active_ticks += 1
            elif self.current_floor > self.preferred_floor:
                self.current_floor -= 1
                self.direction = "down"
                self.active_ticks += 1
            else:
                self.direction = "idle"
            self.door_state = "closed"

    def pickup_passenger(self, destination_floor):
        if self.current_passengers < self.capacity:
            self.current_passengers += 1
            self.dropoff_map[destination_floor] = self.dropoff_map.get(destination_floor, 0) + 1
            return True
        return False
