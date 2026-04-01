import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Upload from "./pages/Upload";
import Dashboard from "./pages/Dashboard";
import Incidents from "./pages/Incidents";

const isAuthenticated = () => {
  return localStorage.getItem("token");
};

function App() {
  return (
    <div className="bg-slate-900 text-white min-h-screen">
      <Routes>
        <Route path="/" element={<Login />} />
        <Route
          path="/upload"
          element={isAuthenticated() ? <Upload /> : <Navigate to="/" />}
        />
        <Route
          path="/dashboard"
          element={isAuthenticated() ? <Dashboard /> : <Navigate to="/" />}
        />
        <Route
          path="/incidents"
          element={isAuthenticated() ? <Incidents /> : <Navigate to="/" />}
        />
      </Routes>
    </div>
  );
}

export default App;
