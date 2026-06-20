import { useState } from "react";
import API from "../services/api";
import Layout from "../components/Layout";
import { Search as SearchIcon, AlertTriangle } from "lucide-react";

function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async (e) => {
    e.preventDefault();
    setError("");

    const logId = localStorage.getItem("log_id");
    if (!logId) {
      setError("No analyzed log file found. Upload and analyze one first.");
      return;
    }

    if (!query.trim()) return;

    setLoading(true);

    try {
      const res = await API.get(`/ai/search/${logId}/`, { params: { q: query } });
      setResults(res.data.results);
    } catch (err) {
      const detail =
        err.response?.data?.error ||
        JSON.stringify(err.response?.data) ||
        err.message;
      setError(`Search failed: ${detail}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <h1 className="text-2xl font-semibold mb-2">Semantic Search</h1>
      <p className="text-sm text-slate-500 dark:text-slate-400 mb-6">
        Search log events by meaning, not just keywords (vector similarity over Gemini embeddings).
      </p>

      <form onSubmit={handleSearch} className="flex gap-2 max-w-xl mb-6">
        <input
          type="text"
          placeholder="e.g. database connection issues"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 p-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-accent-500"
        />
        <button
          type="submit"
          disabled={loading}
          className="flex items-center gap-2 bg-accent-600 hover:bg-accent-700 disabled:opacity-60 text-white px-5 rounded-lg font-semibold transition"
        >
          <SearchIcon size={18} />
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {error && (
        <div className="flex items-center gap-2 text-red-600 dark:text-red-400 text-sm mb-4">
          <AlertTriangle size={16} />
          {error}
        </div>
      )}

      {results && results.length === 0 && (
        <p className="text-slate-500 dark:text-slate-400">No matches found.</p>
      )}

      {results && results.length > 0 && (
        <div className="space-y-3 max-w-2xl">
          {results.map((r) => (
            <div
              key={r.event_id}
              className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 rounded-lg"
            >
              <div className="flex justify-between text-xs text-slate-500 dark:text-slate-400 mb-1">
                <span>{r.service_name} · {r.log_level}</span>
                <span>similarity distance: {r.distance.toFixed(3)}</span>
              </div>
              <p className="text-sm">{r.message}</p>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}

export default Search;
