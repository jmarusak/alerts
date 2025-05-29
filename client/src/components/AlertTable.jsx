import { useState, useEffect } from "react";

export default function AlertTable() {
  const [alerts, setAlerts] = useState([]);

  // Fetch data from backend when component mounts
  useEffect(() => {
    fetch("http://localhost:8000/alerts")
      .then((response) => response.json())
      .then((data) => setAlerts(data))
      .catch((error) => console.error("Error fetching alerts:", error));
  }, []);

  const addAlert = () => {
    setAlerts([...alerts, { symbol: "", below: "", above: "", last: "" }]);
  };

  const deleteAlert = (index) => {
    const alert = alerts[index];
    if (alert.symbol) {
      // If symbol exists, delete from backend
      fetch(`http://localhost:8000/alert/${alert.symbol}`, {
        method: "DELETE",
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Delete failed");
          }
          return response.json();
        })
        .then((data) => {
          console.log("Deleted alert:", data);
          // Remove from frontend list
          const updatedAlerts = alerts.filter((_, i) => i !== index);
          setAlerts(updatedAlerts);
        })
        .catch((error) => console.error("Error deleting alert:", error));
    } else {
      // If no symbol (empty row), just remove locally
      const updatedAlerts = alerts.filter((_, i) => i !== index);
      setAlerts(updatedAlerts);
    }
  };

  const updateAlert = (index, key, value) => {
    const updatedAlerts = alerts.map((alert, i) =>
      i === index ? { ...alert, [key]: value } : alert
    );
    setAlerts(updatedAlerts);
  };

  // Save alert to backend
  const saveAlert = (index) => {
    const alert = alerts[index];
    fetch("http://localhost:8000/alert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(alert),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Saved alert:", data);
        // Optionally refresh alerts list from backend
        // Or update UI accordingly
      })
      .catch((error) => console.error("Error saving alert:", error));
  };
  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Below Price</th>
            <th>Above Price</th>
            <th>Last Alert</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((alert, index) => (
            <tr key={index}>
              <td>
                <input
                  value={alert.symbol}
                  onChange={(e) => updateAlert(index, "symbol", e.target.value)}
                />
              </td>
              <td>
                <input
                  value={alert.below}
                  onChange={(e) => updateAlert(index, "below", e.target.value)}
                />
              </td>
              <td>
                <input
                  value={alert.above}
                  onChange={(e) => updateAlert(index, "above", e.target.value)}
                />
              </td>
              <td>
                <input
                  value={alert.last}
                  onChange={(e) => updateAlert(index, "last", e.target.value)}
                />
              </td>
              <td>
		            <div className="action-buttons">
                  <button onClick={addAlert}>➕</button>
                  <button onClick={() => deleteAlert(index)}>❌</button>
                  <button onClick={() => saveAlert(index)}>✔️</button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
