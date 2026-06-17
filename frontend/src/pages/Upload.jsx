import { useState } from "react";
import API from "../services/api";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import { UploadCloud, FileText } from "lucide-react";

function Upload() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleUpload = async (e) => {
    e.preventDefault();
    setError("");

    if (!file) {
      setError("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const res = await API.post("/logs/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      localStorage.setItem("log_id", res.data.log_file_id);
      navigate("/dashboard");
    } catch (err) {
      const detail =
        err.response?.data?.error ||
        JSON.stringify(err.response?.data) ||
        err.message;
      setError(`Upload failed: ${detail}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="flex items-center justify-center min-h-[80vh]">
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-2xl shadow-sm w-full max-w-md">
          <div className="flex flex-col items-center mb-6">
            <div className="bg-accent-600 text-white p-3 rounded-xl mb-3">
              <UploadCloud size={24} />
            </div>
            <h1 className="text-2xl font-semibold">Upload Logs</h1>
            <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
              Upload a log file to analyze
            </p>
          </div>

          <form onSubmit={handleUpload} className="space-y-4">
            <label
              htmlFor="log-file"
              className="flex flex-col items-center justify-center gap-2 p-6 rounded-lg border-2 border-dashed border-slate-300 dark:border-slate-700 cursor-pointer hover:border-accent-500 transition"
            >
              <FileText size={28} className="text-slate-400" />
              <span className="text-sm text-slate-500 dark:text-slate-400 text-center">
                {file ? file.name : "Click to select a log file"}
              </span>
              <input
                id="log-file"
                type="file"
                className="hidden"
                onChange={(e) => setFile(e.target.files[0])}
              />
            </label>

            {error && <p className="text-red-500 text-sm">{error}</p>}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-accent-600 hover:bg-accent-700 disabled:opacity-60 text-white p-3 rounded-lg font-semibold transition"
            >
              {loading ? "Uploading..." : "Upload"}
            </button>
          </form>
        </div>
      </div>
    </Layout>
  );
}

export default Upload;
