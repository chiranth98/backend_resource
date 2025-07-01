import React from "react";

function Elevator({ id, current_floor, direction }) {
  console.log(`Rendering Elevator ${id}: Floor ${current_floor}, Direction ${direction}`);

  return (
    <div style={{ border: "1px solid gray", padding: "1rem" }}>
      <h3>Elevator {id}</h3>
      <p>Floor: {current_floor}</p>
      <p>Direction: {direction}</p>
    </div>
  );
}


export default Elevator;