
import { useEffect, useState } from "react";
import "./App.css";

function App() {

  const [data, setData] = useState({
    motion: "none",
    person_detected: false,
    person_id: "—",
    safety: "—",
    privacy: "—",
    ethical_score: "—",
    temperature: "—",
    humidity: "—"
  });

  useEffect(() => {

    const getDashboardData = async () => {

      try {

        const response = await fetch(
          "http://127.0.0.1:5000/dashboard"
        );

        const result = await response.json();

        console.log(result);

        setData(result);

      } catch (error) {

        console.log(
          "Flask connection error:",
          error
        );

      }

    };

    getDashboardData();

    const interval = setInterval(
      getDashboardData,
      1000
    );

    return () => {
      clearInterval(interval);
    };

  }, []);


  return (

    <div className="dashboard">

      <header>

        <h1>
          EDGE-AI ETHICAL COMPLIANCE
        </h1>

        <p>
          Real-Time Autonomous AI Monitoring System
        </p>

      </header>


      <div className="status-grid">


        <div className="card">

          <h3>Motion Detected</h3>

          <p>
            {data.motion === "detected"
              ? "YES"
              : "NO"}
          </p>

        </div>


        <div className="card">

          <h3>Person Detected</h3>

          <p>
            {data.person_detected
              ? "YES"
              : "NO"}
          </p>

        </div>


        <div className="card">

          <h3>Person ID</h3>

          <p>
            {data.person_id}
          </p>

        </div>


        <div className="card">

          <h3>Temperature</h3>

          <p>
            {data.temperature === "—"
              ? "—"
              : `${data.temperature} °C`}
          </p>

        </div>


        <div className="card">

          <h3>Humidity</h3>

          <p>
            {data.humidity === "—"
              ? "—"
              : `${data.humidity} %`}
          </p>

        </div>


        <div className="card">

          <h3>Safety</h3>

          <p>
            {data.safety}
          </p>

        </div>


        <div className="card">

          <h3>Privacy</h3>

          <p>
            {data.privacy}
          </p>

        </div>


        <div className="score-card">

          <h3>Ethical Score</h3>

          <div className="score">

            {data.ethical_score}

            {data.ethical_score !== "—"
              ? "/100"
              : ""}

          </div>

        </div>


      </div>


      <footer>

        <p>
          Edge AI • Local Processing • Privacy Preserving
        </p>

      </footer>

    </div>

  );

}

export default App;

