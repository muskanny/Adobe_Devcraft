import React from "react";
import { useNavigate } from "react-router-dom";

function Navbar({ advertiserData, setAdvertiserData }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    setAdvertiserData(null); // Clear advertiser data
    navigate("/"); // Redirect to landing page
  };

  return (
    <div className="bg-gray-800 text-white p-5 shadow-md flex justify-between items-center">
      <h1 className="text-xl font-semibold">RTB Optimization Dashboard</h1>
      
      {advertiserData && (
        <div className="flex items-center space-x-4">
          <span className="text-sm">Advertiser ID: {advertiserData.advertiserId}</span>
          <button 
            onClick={handleLogout} 
            className="bg-red-600 px-4 py-2 rounded-md text-white text-sm hover:bg-red-700 transition"
          >
            Logout
          </button>
        </div>
      )}
    </div>
  );
}

export default Navbar;
