import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";  // Import axios for API calls
import Landing from "./pages/Landing";
import Dashboard from "./pages/Dashboard";
import Logs from "./pages/Logs";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";

function App() {
  const [advertiserData, setAdvertiserData] = useState(null);

  useEffect(() => {
    if (advertiserData) {
      axios.get(`http://127.0.0.1:5000/api/advertiser/${advertiserData.advertiserId}`)
        .then(response => {
          setAdvertiserData(prev => ({ ...prev, ...response.data })); // Merge backend data
        })
        .catch(error => console.error("Error fetching advertiser data:", error));
    }
  }, [advertiserData]);

  return (
    <Router>
      <div className="flex">
        {advertiserData ? (
          <>
            <Sidebar />
            <div className="flex-1 px-8 py-6">
              <Navbar />
              <Routes>
                <Route path="/dashboard" element={<Dashboard advertiserData={advertiserData} setAdvertiserData={setAdvertiserData} />} />
                <Route path="/logs" element={<Logs />} />
              </Routes>
            </div>
          </>
        ) : (
          <Routes>
            <Route path="/" element={<Landing setAdvertiserData={setAdvertiserData} />} />
          </Routes>
        )}
      </div>
    </Router>
  );
}

export default App;
