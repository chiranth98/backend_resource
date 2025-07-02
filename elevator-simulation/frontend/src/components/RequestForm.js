import React, { useState } from "react";

function RequestForm() {
  const [origin, setOrigin] = useState(0);
  const [destination, setDestination] = useState(1);

  const handleOriginChange = (e) => {
    const cleaned = e.target.value.replace(/^0+(?=\d)/, ""); // remove leading zeros
    setOrigin(cleaned === "" ? 0 : parseInt(cleaned, 10));
  };

  const handleDestinationChange = (e) => {
    const cleaned = e.target.value.replace(/^0+(?=\d)/, "");
    setDestination(cleaned === "" ? 0 : parseInt(cleaned, 10));
  };

  const submitRequest = async () => {
    if (origin === destination) {
      alert("Origin and destination can't be the same");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/request", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          origin_floor: origin,
          destination_floor: destination,
        }),
      });

      const data = await response.json();
      console.log("Request created:", data);
      alert(`Request ID ${data.request_id} added.`);
    } catch (err) {
      console.error("Request failed", err);
      alert("Failed to send request.");
    }
  };

  return (
    <div style={{ margin: "1rem 0" }}>
      <h3>Create Elevator Request</h3>
      <label>From Floor: </label>
      <input
        type="number"
        min={0}
        value={origin}
        onChange={handleOriginChange}
      />
      <label> To Floor: </label>
      <input
        type="number"
        min={0}
        value={destination}
        onChange={handleDestinationChange}
      />
      <button onClick={submitRequest} style={{ marginLeft: "1rem" }}>
        Request Elevator
      </button>
    </div>
  );
}

export default RequestForm;
