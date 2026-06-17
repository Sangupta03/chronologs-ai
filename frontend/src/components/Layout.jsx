import Sidebar from "./Sidebar";

function Layout({ children }) {
  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100">

      <Sidebar />

      <div className="flex-1 p-8">
        {children}
      </div>

    </div>
  );
}

export default Layout;