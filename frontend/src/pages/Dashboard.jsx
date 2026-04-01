import { useState } from "react";
import API from "../services/api";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";

function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const navigate = useNavigate();

  const handleAnalyze = async () => {
    const logId = localStorage.getItem("log_id");

    if (!logId) {
      alert("No log file found. Upload first.");
      return;
    }

    setLoading(true);

    try {
      const res = await API.post(`/ai/analyze/${logId}/`);

      setResult(res.data);

    } catch (err) {
      alert("Analysis failed ❌");
    }

    setLoading(false);
  };

  return (
    <Layout>
    <div className="min-h-screen bg-slate-900 text-white p-8">

      <h1 className="text-3xl font-bold mb-6">
        Dashboard 📊
      </h1>

      {/* Analyze Button */}
      <button
        onClick={handleAnalyze}
        className="bg-blue-500 hover:bg-blue-600 px-6 py-3 rounded-lg font-semibold"
      >
        {loading ? "Analyzing..." : "Analyze Logs"}
      </button>

      {/* Results */}
      {result && (
        <div className="mt-8 space-y-4">

          <div className="bg-slate-800 p-4 rounded-lg">
            <p><strong>Total Events:</strong> {result.total_events}</p>
          </div>

          <div className="bg-slate-800 p-4 rounded-lg">
            <p><strong>Incidents Created:</strong> {result.incidents_created}</p>
          </div>

          <div className="bg-slate-800 p-4 rounded-lg">
            <p><strong>Clusters:</strong></p>
            <div className="mt-2 space-y-2">
              {Object.entries(result.clusters).map(([key, value]) => (
                <div
                  key={key}
                  className="bg-slate-700 p-2 rounded flex justify-between"
                >
                  <span>Cluster {key}</span>
                  <span>{value} events</span>
                </div>
              ))}
            </div>
            {/* <pre className="text-sm mt-2">
              {JSON.stringify(result.clusters, null, 2)}
            </pre> */}
          </div>

          {/* Go to incidents */}
          <button
            onClick={() => navigate("/incidents")}
            className="bg-green-500 hover:bg-green-600 px-6 py-3 rounded-lg font-semibold"
          >
            View Incidents 🚨
          </button>

        </div>
      )}

    </div>
    </Layout>
  );
}

export default Dashboard;

