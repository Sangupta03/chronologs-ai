import Sidebar from "./Sidebar";

function Layout({ children }) {
  return (
    <div className="flex bg-slate-900 text-white">

      <Sidebar />

      <div className="flex-1 p-8">
        {children}
      </div>

    </div>
  );
}

export default Layout;