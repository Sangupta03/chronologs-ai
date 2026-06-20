import { useCallback, useEffect, useState } from "react";
import API from "../services/api";
import Layout from "../components/Layout";
import { AlertTriangle, Loader2, ChevronLeft, ChevronRight } from "lucide-react";

const SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW"];

function Incidents() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [severity, setSeverity] = useState("");
  const [page, setPage] = useState(1);
  const [count, setCount] = useState(0);
  const pageSize = 10;

  const fetchIncidents = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const res = await API.get("/incidents/", {
        params: { severity: severity || undefined, page },
      });
      setIncidents(res.data.results);
      setCount(res.data.count);
    } catch (err) {
      const detail =
        err.response?.data?.detail || err.message || "Could not load incidents";
      setError(detail);
    } finally {
      setLoading(false);
    }
  }, [severity, page]);

  useEffect(() => {
    fetchIncidents();
  }, [fetchIncidents]);

  const severityStyle = (sev) => {
    switch (sev) {
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

  const totalPages = Math.max(1, Math.ceil(count / pageSize));

  return (
    <Layout>
      <h1 className="text-2xl font-semibold mb-6">Incidents</h1>

      <div className="flex items-center gap-3 mb-6">
        <select
          value={severity}
          onChange={(e) => {
            setSeverity(e.target.value);
            setPage(1);
          }}
          className="p-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm"
        >
          <option value="">All severities</option>
          {SEVERITIES.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

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
        <>
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

          <div className="flex items-center justify-between mt-6 text-sm text-slate-500 dark:text-slate-400">
            <span>Page {page} of {totalPages} ({count} total)</span>
            <div className="flex gap-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1}
                className="flex items-center gap-1 px-3 py-1.5 rounded-lg border border-slate-300 dark:border-slate-700 disabled:opacity-40"
              >
                <ChevronLeft size={14} /> Prev
              </button>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page >= totalPages}
                className="flex items-center gap-1 px-3 py-1.5 rounded-lg border border-slate-300 dark:border-slate-700 disabled:opacity-40"
              >
                Next <ChevronRight size={14} />
              </button>
            </div>
          </div>
        </>
      )}
    </Layout>
  );
}

export default Incidents;
