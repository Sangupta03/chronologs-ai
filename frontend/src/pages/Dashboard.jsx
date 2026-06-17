import { useState } from "react";
import API from "../services/api";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import { Sparkles, AlertTriangle } from "lucide-react";

function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleAnalyze = async () => {
    const logId = localStorage.getItem("log_id");
    setError("");

    if (!logId) {
      setError("No log file found. Upload one first.");
      return;
    }

    setLoading(true);

    try {
      const res = await API.post(`/ai/analyze/${logId}/`);
      setResult(res.data);
    } catch (err) {
      const detail =
        err.response?.data?.error ||
        JSON.stringify(err.response?.data) ||
        err.message;
      setError(`Analysis failed: ${detail}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <h1 className="text-2xl font-semibold mb-6">Dashboard</h1>

      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="flex items-center gap-2 bg-accent-600 hover:bg-accent-700 disabled:opacity-60 text-white px-6 py-3 rounded-lg font-semibold transition"
      >
        <Sparkles size={18} />
        {loading ? "Analyzing..." : "Analyze Logs"}
      </button>

      {error && (
        <div className="mt-4 flex items-center gap-2 text-red-600 dark:text-red-400 text-sm">
          <AlertTriangle size={16} />
          {error}
        </div>
      )}

      {result && (
        <div className="mt-8 space-y-4 max-w-xl">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 rounded-lg">
            <p><strong>Total Events:</strong> {result.total_events}</p>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 rounded-lg">
            <p><strong>Incidents Created:</strong> {result.incidents_created}</p>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 rounded-lg">
            <p className="mb-2"><strong>Clusters:</strong></p>
            <div className="space-y-2">
              {Object.entries(result.clusters).map(([key, value]) => (
                <div
                  key={key}
                  className="bg-slate-100 dark:bg-slate-800 p-2 rounded flex justify-between text-sm"
                >
                  <span>Cluster {key}</span>
                  <span>{value} events</span>
                </div>
              ))}
            </div>
          </div>

          <button
            onClick={() => navigate("/incidents")}
            className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-lg font-semibold transition"
          >
            View Incidents
          </button>
        </div>
      )}
    </Layout>
  );
}

export default Dashboard;
