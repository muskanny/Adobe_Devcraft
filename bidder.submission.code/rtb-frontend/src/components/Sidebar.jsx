import { Link, useLocation } from "react-router-dom";

function Sidebar() {
  const location = useLocation(); // Get the current route

  return (
    <div className="w-72 bg-gray-900 text-white h-screen p-6">
      <h2 className="text-2xl font-bold">RTB System</h2>
      <ul className="mt-6 space-y-4">
        <li>
          <Link
            to="/dashboard"
            className={`block p-3 rounded-lg transition ${
              location.pathname === "/dashboard" ? "bg-blue-600" : "bg-gray-700 hover:bg-gray-600"
            }`}
          >
            Dashboard
          </Link>
        </li>
        <li>
          <Link
            to="/logs"
            className={`block p-3 rounded-lg transition ${
              location.pathname === "/logs" ? "bg-blue-600" : "bg-gray-700 hover:bg-gray-600"
            }`}
          >
            Bid Logs
          </Link>
        </li>
      </ul>
    </div>
  );
}

export default Sidebar;
