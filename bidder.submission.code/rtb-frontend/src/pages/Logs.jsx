import { useEffect, useState } from "react";
import axios from "axios";
import LogTable from "../components/LogTable";

function Logs() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/realtime-bids")
      .then(response => setLogs(response.data))
      .catch(error => console.error("Error fetching bid logs:", error));
  }, []);

  return (
    <div className="px-10 py-6">
      <h2 className="text-2xl font-bold mb-4">Bid Logs</h2>
      {logs.length > 0 ? <LogTable logs={logs} /> : <p>Loading bid logs...</p>}
    </div>
  );
}

export default Logs;
