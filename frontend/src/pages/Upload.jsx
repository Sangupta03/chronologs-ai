import { useState } from "react";
import API from "../services/api";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";

function Upload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await API.post("/logs/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setMessage("Upload successful ✅");

      // Save log_file_id for next step
      localStorage.setItem("log_id", res.data.log_file_id);

      // Redirect to dashboard
      navigate("/dashboard");

    } catch (err) {
      setMessage("Upload failed ❌");
    }
  };

  return (
    <Layout>
    <div className="min-h-screen flex items-center justify-center bg-slate-900">

      <div className="bg-slate-800 p-8 rounded-2xl shadow-lg w-full max-w-md">

        <h1 className="text-2xl font-bold text-center mb-6">
          Upload Logs 📤
        </h1>

        <form onSubmit={handleUpload} className="space-y-4">

          <input
            type="file"
            className="w-full p-3 rounded-lg bg-slate-700"
            onChange={(e) => setFile(e.target.files[0])}
          />


          {message && (
            <p className="text-sm text-center">{message}</p>
          )}

          <button
            type="submit"
            className="w-full bg-blue-500 hover:bg-blue-600 p-3 rounded-lg font-semibold"
          >
            Upload
          </button>

        </form>
      </div>
    </div>
    </Layout>
  );
}

export default Upload;
