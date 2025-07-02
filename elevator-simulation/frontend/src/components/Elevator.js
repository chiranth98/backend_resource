import React from "react";

function Elevator({
  id,
  current_floor,
  direction,
  door_state,
  current_passengers,
  capacity,
  utilization,
  preferred_floor,
  passenger_destinations,
}) {
  return (
    <div
      style={{ border: "1px solid black", padding: "1rem", minWidth: "150px" }}
    >
      <h3>Elevator {id}</h3>
      <p>Floor: {current_floor}</p>
      <p
        style={{
          fontStyle:
            direction === "idle" && current_floor !== preferred_floor
              ? "italic"
              : "normal",
        }}
      >
        Direction: {direction}
      </p>
      <p style={{ color: door_state === "open" ? "green" : "gray" }}>
        Door: {door_state}
      </p>
      <p>
        Passengers:{" "}
        <span
          style={{ color: current_passengers >= capacity ? "red" : "black" }}
        >
          {current_passengers}/{capacity}
        </span>
      </p>
      {passenger_destinations && Object.keys(passenger_destinations).length > 0 && (
        <div style={{ fontSize: "0.9em", marginBottom: "0.5em" }}>
          <strong>Destinations:</strong>
          <ul style={{ margin: 0, paddingLeft: "1.2em" }}>
            {Object.entries(passenger_destinations).map(([floor, count]) => (
              <li key={floor}>
                {count} to floor {floor}
              </li>
            ))}
          </ul>
        </div>
      )}
      <p>Utilization: {utilization}%</p>
      <p>Preferred Floor: {preferred_floor}</p>
    </div>
  );
}

export default Elevator;
