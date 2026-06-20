import { Link, useLocation, useNavigate } from "react-router-dom";
import { Activity, LayoutDashboard, Upload as UploadIcon, AlertTriangle, Search as SearchIcon, LogOut, Sun, Moon } from "lucide-react";
import { useTheme } from "../context/useTheme";
import { logout } from "../services/auth";

function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  const linkClass = (path) =>
    `flex items-center gap-3 px-4 py-2 rounded-lg transition ${
      location.pathname === path
        ? "bg-accent-600 text-white"
        : "text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
    }`;

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  return (
    <div className="w-64 min-h-screen p-6 border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex flex-col">
      <div className="flex items-center gap-2 mb-8">
        <div className="bg-accent-600 text-white p-2 rounded-lg">
          <Activity size={18} />
        </div>
        <h1 className="text-lg font-semibold">ChronoLogs AI</h1>
      </div>

      <nav className="space-y-2 flex-1">
        <Link to="/dashboard" className={linkClass("/dashboard")}>
          <LayoutDashboard size={18} />
          Dashboard
        </Link>

        <Link to="/upload" className={linkClass("/upload")}>
          <UploadIcon size={18} />
          Upload Logs
        </Link>

        <Link to="/incidents" className={linkClass("/incidents")}>
          <AlertTriangle size={18} />
          Incidents
        </Link>

        <Link to="/search" className={linkClass("/search")}>
          <SearchIcon size={18} />
          Search
        </Link>
      </nav>

      <div className="space-y-2 pt-4 border-t border-slate-200 dark:border-slate-800">
        <button
          onClick={toggleTheme}
          className="w-full flex items-center gap-3 px-4 py-2 rounded-lg text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
        >
          {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
          {theme === "dark" ? "Light mode" : "Dark mode"}
        </button>

        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-4 py-2 rounded-lg text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/40 transition"
        >
          <LogOut size={18} />
          Logout
        </button>
      </div>
    </div>
  );
}

export default Sidebar;
