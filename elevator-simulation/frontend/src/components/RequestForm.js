import React, { useState } from "react";

function RequestForm() {
  const [origin, setOrigin] = useState(1);
  const [destination, setDestination] = useState(5);

  const submitRequest = async () => {
    if (origin === destination) {
      alert("Origin and destination can't be the same");
      return;
    }

    const response = await fetch("http://localhost:8000/request", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        origin_floor: origin,
        destination_floor: destination
      })
    });

    const data = await response.json();
    console.log("Request created:", data);
    alert(`Request ID ${data.request_id} added.`);
  };

  return (
    <div style={{ margin: "1rem 0" }}>
      <h3>Create Elevator Request</h3>
      <label>From Floor: </label>
      <input type="number" value={origin} onChange={(e) => setOrigin(Number(e.target.value))} />
      <label> To Floor: </label>
      <input type="number" value={destination} onChange={(e) => setDestination(Number(e.target.value))} />
      <button onClick={submitRequest} style={{ marginLeft: "1rem" }}>Request Elevator</button>
    </div>
  );
}

export default RequestForm;
