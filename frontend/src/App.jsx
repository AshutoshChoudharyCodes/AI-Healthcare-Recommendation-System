import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    name: "",
    age: 0,
    fever: 0,
    cough: 0,
    headache: 0,
    fatigue: 0,
  });

  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  const fetchHistory = async () => {
    const response = await fetch("http://127.0.0.1:8000/history");
    const data = await response.json();
    setHistory(data);
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleSubmit = async () => {
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    const data = await response.json();
    setResult(data);

    fetchHistory();
  };

  return (
    <div className="container">
      <div className="card">
        <h1>🏥 AI Healthcare Recommendation System</h1>

        <input
          type="text"
          placeholder="Enter Name"
          onChange={(e) =>
            setFormData({ ...formData, name: e.target.value })
          }
        />

        <input
          type="number"
          placeholder="Enter Age"
          onChange={(e) =>
            setFormData({ ...formData, age: Number(e.target.value) })
          }
        />

        <input
          type="number"
          placeholder="Fever (0 or 1)"
          onChange={(e) =>
            setFormData({ ...formData, fever: Number(e.target.value) })
          }
        />

        <input
          type="number"
          placeholder="Cough (0 or 1)"
          onChange={(e) =>
            setFormData({ ...formData, cough: Number(e.target.value) })
          }
        />

        <input
          type="number"
          placeholder="Headache (0 or 1)"
          onChange={(e) =>
            setFormData({ ...formData, headache: Number(e.target.value) })
          }
        />

        <input
          type="number"
          placeholder="Fatigue (0 or 1)"
          onChange={(e) =>
            setFormData({ ...formData, fatigue: Number(e.target.value) })
          }
        />

        <button onClick={handleSubmit}>
          Predict Disease
        </button>

        {result && (
          <div className="result">
            <h2>Prediction Result</h2>

            <p><strong>Name:</strong> {formData.name}</p>
            <p><strong>Age:</strong> {formData.age}</p>
            <p><strong>Disease:</strong> {result.predicted_disease}</p>
            <p><strong>Medicine:</strong> {result.medicine}</p>
            <p><strong>Doctor:</strong> {result.doctor}</p>
            <p><strong>Precaution:</strong> {result.precaution}</p>
          </div>
        )}

        <div className="result">
          <h2>Prediction History</h2>

          <table style={{ width: "100%" }}>
            <thead>
              <tr>
                <th>Name</th>
                <th>Age</th>
                <th>Disease</th>
              </tr>
            </thead>

            <tbody>
              {history.map((item, index) => (
                <tr key={index}>
                  <td>{item.name}</td>
                  <td>{item.age}</td>
                  <td>{item.predicted_disease}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

      </div>
    </div>
  );
}

export default App;