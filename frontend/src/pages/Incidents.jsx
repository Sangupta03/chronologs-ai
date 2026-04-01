import { useEffect, useState } from "react";
import API from "../services/api";
import Layout from "../components/Layout";
function Incidents() {
  const [incidents, setIncidents] = useState([]);

  useEffect(() => {
    fetchIncidents();
  }, []);

  const fetchIncidents = async () => {
    try {
      const res = await API.get("/incidents/");
      setIncidents(res.data);
    } catch (err) {
      console.error("Error fetching incidents");
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case "CRITICAL":
        return "bg-red-500";
      case "HIGH":
        return "bg-orange-500";
      case "MEDIUM":
        return "bg-yellow-500";
      default:
        return "bg-gray-500";
    }
  };

  return (
    <Layout>
    <div className="min-h-screen bg-slate-900 text-white p-8">

      <h1 className="text-3xl font-bold mb-6">
        Incidents 🚨
      </h1>

      {incidents.length === 0 ? (
        <p>No incidents found</p>
      ) : (
        <div className="space-y-6">

          {incidents.map((incident) => (
            <div
              key={incident.id}
              className="bg-slate-800 p-6 rounded-xl shadow hover:scale-105 transition"
            >

              {/* Header */}
              <div className="flex justify-between items-center mb-3">
                <h2 className="text-xl font-semibold">
                  {incident.title}
                </h2>

                <span
                  className={`px-3 py-1 rounded text-sm font-semibold ${getSeverityColor(incident.severity)}`}
                >
                  {incident.severity}
                </span>
              </div>

              {/* Time */}
              <p className="text-sm text-gray-400">
                {new Date(incident.start_time).toLocaleTimeString()} -{" "}
                {new Date(incident.end_time).toLocaleTimeString()}
              </p>

              {/* Event count */}
              <p className="mt-2">
                Events: {incident.event_count}
              </p>

              {/* Summary (MOST IMPORTANT) */}
              <div className="mt-4 bg-slate-700 p-4 rounded-lg">
                <p className="text-sm whitespace-pre-line">
                  {incident.summary}
                </p>
              </div>

            </div>
          ))}

        </div>
      )}
    </div>
    </Layout>
  );
}

export default Incidents;

