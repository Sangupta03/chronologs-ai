import { useEffect, useState } from "react";
import API from "../services/api";
import Layout from "../components/Layout";
import { AlertTriangle, Loader2 } from "lucide-react";

function Incidents() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchIncidents();
  }, []);

  const fetchIncidents = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await API.get("/incidents/");
      setIncidents(res.data);
    } catch (err) {
      const detail =
        err.response?.data?.detail || err.message || "Could not load incidents";
      setError(detail);
    } finally {
      setLoading(false);
    }
  };

  const severityStyle = (severity) => {
    switch (severity) {
      case "CRITICAL":
        return "bg-red-100 text-red-700 dark:bg-red-950/50 dark:text-red-400";
      case "HIGH":
        return "bg-orange-100 text-orange-700 dark:bg-orange-950/50 dark:text-orange-400";
      case "MEDIUM":
        return "bg-yellow-100 text-yellow-700 dark:bg-yellow-950/50 dark:text-yellow-400";
      default:
        return "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300";
    }
  };

  return (
    <Layout>
      <h1 className="text-2xl font-semibold mb-6">Incidents</h1>

      {loading && (
        <div className="flex items-center gap-2 text-slate-500 dark:text-slate-400">
          <Loader2 size={18} className="animate-spin" />
          Loading incidents...
        </div>
      )}

      {!loading && error && (
        <div className="flex items-center gap-2 text-red-600 dark:text-red-400 text-sm">
          <AlertTriangle size={16} />
          {error}
        </div>
      )}

      {!loading && !error && incidents.length === 0 && (
        <p className="text-slate-500 dark:text-slate-400">No incidents found</p>
      )}

      {!loading && !error && incidents.length > 0 && (
        <div className="space-y-4">
          {incidents.map((incident) => (
            <div
              key={incident.id}
              className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-xl shadow-sm"
            >
              <div className="flex justify-between items-center mb-3">
                <h2 className="text-lg font-semibold">{incident.title}</h2>

                <span
                  className={`px-3 py-1 rounded-full text-xs font-semibold ${severityStyle(incident.severity)}`}
                >
                  {incident.severity}
                </span>
              </div>

              <p className="text-sm text-slate-500 dark:text-slate-400">
                {new Date(incident.start_time).toLocaleTimeString()} -{" "}
                {new Date(incident.end_time).toLocaleTimeString()}
              </p>

              <p className="mt-2 text-sm">Events: {incident.event_count}</p>

              <div className="mt-4 bg-slate-50 dark:bg-slate-800 p-4 rounded-lg">
                <p className="text-sm whitespace-pre-line">{incident.summary}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}

export default Incidents;
