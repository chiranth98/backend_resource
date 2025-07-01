import React, { useEffect, useState } from "react";
import Elevator from "./components/Elevator";
import RequestForm from "./components/RequestForm";

function App() {
  const [elevators, setElevators] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://localhost:8000/state")
        .then(res => res.json())
        .then(data => setElevators(data.elevators));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const setSpeed = async (speed) => {
    try {
      await fetch("http://localhost:8000/speed", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(speed),
      });
      alert(`Simulation speed set to ${speed}x`);
    } catch (err) {
      console.error("Error setting speed:", err);
    }
  };

  const toggleAutoGenerate = async (start) => {
  try {
    await fetch(`http://localhost:8000/auto/${start ? "start" : "stop"}`, {
      method: "POST",
    });
    alert(`Auto generation ${start ? "started" : "stopped"}`);
  } catch (err) {
    console.error("Auto generate error:", err);
  }
};

const togglePeakMode = async (enable) => {
  try {
    await fetch(`http://localhost:8000/peak/${enable ? "enable" : "disable"}`, {
      method: "POST",
    });
    alert(`Peak mode ${enable ? "enabled" : "disabled"}`);
  } catch (err) {
    console.error("Peak mode error:", err);
  }
};


  return (
    <div className="App">
      <h1>Elevator Simulation</h1>
      <RequestForm />

      <div style={{ margin: "20px 0" }}>
        <strong>Speed Control:</strong>{" "}
        <button onClick={() => setSpeed(1)}>1x</button>{" "}
        <button onClick={() => setSpeed(2)}>2x</button>{" "}
        <button onClick={() => setSpeed(5)}>5x</button>
      </div>


      <div style={{ margin: "20px 0" }}>
        <strong>Request Generation:</strong>{" "}
        <button onClick={() => toggleAutoGenerate(true)}>Start Auto</button>{" "}
        <button onClick={() => toggleAutoGenerate(false)}>Stop Auto</button>
      </div>

      <div style={{ margin: "20px 0" }}>
        <strong>Peak Mode:</strong>{" "}
        <button onClick={() => togglePeakMode(true)}>Enable Peak</button>{" "}
        <button onClick={() => togglePeakMode(false)}>Disable Peak</button>
      </div>

      <div style={{ display: "flex", gap: "1rem" }}>
        {Array.isArray(elevators) && elevators.map((elevator) => (
          <Elevator key={elevator.id} {...elevator} />
        ))}
      </div>
    </div>
  );
}

export default App;
