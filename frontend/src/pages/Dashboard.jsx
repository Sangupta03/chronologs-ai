import { useEffect, useState } from "react";
import API from "../services/api";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import { Sparkles, AlertTriangle } from "lucide-react";
import { pollUntil } from "../services/poll";
import {
  BarChart, Bar, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

const SEVERITY_COLORS = {
  CRITICAL: "#ef4444",
  HIGH: "#f97316",
  MEDIUM: "#eab308",
  LOW: "#94a3b8",
};

function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [stats, setStats] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await API.get("/incidents/stats/");
      setStats(res.data);
    } catch {
      // stats are a nice-to-have; ignore failures silently here
    }
  };

  const handleAnalyze = async () => {
    const logId = localStorage.getItem("log_id");
    setError("");

    if (!logId) {
      setError("No log file found. Upload one first.");
      return;
    }

    setLoading(true);

    try {
      await API.post(`/ai/analyze/${logId}/`);

      const data = await pollUntil(
        async () => (await API.get(`/ai/analyze/${logId}/status/`)).data,
        (data) => data.status === "completed" || data.status === "failed"
      );

      if (data.status === "failed") {
        throw new Error(data.error || "Analysis failed");
      }

      setResult(data.result);
      fetchStats();
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

  const severityData = stats
    ? Object.entries(stats.severity_counts).map(([severity, count]) => ({ severity, count }))
    : [];

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

      {stats && (severityData.length > 0 || stats.incidents_over_time.length > 0) && (
        <div className="mt-10 grid md:grid-cols-2 gap-6 max-w-4xl">
          {severityData.length > 0 && (
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 rounded-lg">
              <p className="mb-2 font-semibold text-sm">Severity distribution</p>
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={severityData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="currentColor" opacity={0.1} />
                  <XAxis dataKey="severity" tick={{ fontSize: 12 }} />
                  <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                    {severityData.map((entry) => (
                      <Cell key={entry.severity} fill={SEVERITY_COLORS[entry.severity] || "#6366f1"} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {stats.incidents_over_time.length > 0 && (
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 rounded-lg">
              <p className="mb-2 font-semibold text-sm">Incidents over time</p>
              <ResponsiveContainer width="100%" height={220}>
                <LineChart data={stats.incidents_over_time}>
                  <CartesianGrid strokeDasharray="3 3" stroke="currentColor" opacity={0.1} />
                  <XAxis dataKey="date" tick={{ fontSize: 11 }} />
                  <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Line type="monotone" dataKey="count" stroke="#6366f1" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      )}
    </Layout>
  );
}

export default Dashboard;
