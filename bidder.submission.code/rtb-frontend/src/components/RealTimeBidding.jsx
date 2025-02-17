import React, { useState, useEffect } from "react";
import axios from "axios";

function RealTimeBidding() {
  const [bids, setBids] = useState([]);

  useEffect(() => {
    const fetchBids = () => {
      axios.get("http://127.0.0.1:5000/api/realtime-bids")
        .then(response => setBids(response.data.slice(0, 10))) // Limit to last 10 bids
        .catch(error => console.error("Error fetching real-time bids:", error));
    };

    fetchBids(); // Fetch immediately
    const interval = setInterval(fetchBids, 5000); // Refresh every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg mt-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-3">Live Bidding Stream</h3>
      <ul className="overflow-y-auto h-40">
        {bids.length > 0 ? (
          bids.map((bid, index) => (
            <li key={index} className={`p-2 ${bid.Click ? "text-green-600" : "text-red-600"}`}>
              Bid ${parseFloat(bid.Biddingprice).toFixed(2)} - {bid.Click ? "Won" : "Lost"}
            </li>
          ))
        ) : (
          <p className="text-gray-600">Loading bid data...</p>
        )}
      </ul>
    </div>
  );
}

export default RealTimeBidding;
