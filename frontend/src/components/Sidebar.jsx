import { Link, useLocation } from "react-router-dom";

function Sidebar() {
  const location = useLocation();

  const linkClass = (path) =>
    `block px-4 py-2 rounded-lg ${
      location.pathname === path
        ? "bg-blue-500"
        : "hover:bg-slate-700"
    }`;

  return (
    <div className="w-64 bg-slate-800 min-h-screen p-6">

      <h1 className="text-xl font-bold mb-8">
        ChronoLogs AI 🚀
      </h1>

      <nav className="space-y-3">

        <Link to="/dashboard" className={linkClass("/dashboard")}>
          Dashboard 📊
        </Link>

        <Link to="/upload" className={linkClass("/upload")}>
          Upload Logs 📤
        </Link>

        <Link to="/incidents" className={linkClass("/incidents")}>
          Incidents 🚨
        </Link>

        <button
          onClick={() => {
            localStorage.removeItem("token");
            window.location.href = "/";
          }}
          className="w-full text-left px-4 py-2 rounded-lg hover:bg-red-500 mt-4"
        >
          Logout 🚪
        </button>

      </nav>
    </div>
  );
}

export default Sidebar;
