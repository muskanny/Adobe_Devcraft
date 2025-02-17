import React, { useEffect, useState } from "react";
import axios from "axios";

function LogTable() {
  const [bidLogs, setBidLogs] = useState([]);

  useEffect(() => {
    const fetchLogs = () => {
      axios.get("http://127.0.0.1:5000/api/realtime-bids")
        .then(response => setBidLogs(response.data))
        .catch(error => console.error("Error fetching bid logs:", error));
    };

    fetchLogs();
    const interval = setInterval(fetchLogs, 5000); // Refresh logs every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="overflow-x-auto">
      <table className="w-full border">
        <thead>
          <tr className="bg-gray-200">
            <th className="p-2">Bid ID</th>
            <th className="p-2">Bid Price</th>
            <th className="p-2">Paying Price</th>
            <th className="p-2">Click</th>
            <th className="p-2">Conversion</th>
          </tr>
        </thead>
        <tbody>
          {bidLogs.length > 0 ? (
            bidLogs.map((row, index) => (
              <tr key={index} className="border">
                <td className="p-2">{row.BidID}</td>
                <td className="p-2">${parseFloat(row.Biddingprice).toFixed(2)}</td>
                <td className="p-2">${parseFloat(row.Payingprice).toFixed(2)}</td>
                <td className={`p-2 ${row.Click ? "text-green-600" : "text-red-600"}`}>
                  {row.Click ? "Yes" : "No"}
                </td>
                <td className={`p-2 ${row.Conversion ? "text-blue-600" : "text-gray-600"}`}>
                  {row.Conversion ? "Yes" : "No"}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5" className="p-2 text-center">Loading bid logs...</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default LogTable;
