import { useEffect, useState } from "react";
import axios from "axios";
import Configurator from "../components/Configurator";
import RealTimeBidding from "../components/RealTimeBidding";
import MetricsCard from "../components/MetricsCard";
import BidChart from "../components/BidChart";

function Dashboard({ advertiserData, setAdvertiserData }) {
  const [performanceData, setPerformanceData] = useState(null);

  useEffect(() => {
    if (advertiserData) {
      axios.get(`http://127.0.0.1:5000/api/performance`)
        .then(response => {
          const advPerformance = response.data.find(adv => adv.AdvertiserID === advertiserData.advertiserId);
          setPerformanceData(advPerformance);
        })
        .catch(error => console.error("Error fetching performance data:", error));
    }
  }, [advertiserData]);

  return (
    <div className="px-10 py-6">
      <h2 className="text-3xl font-bold mb-4 text-gray-800">Dashboard</h2>
      <p className="text-lg font-semibold text-gray-600 mb-6">
        Advertiser ID: <span className="text-blue-600">{advertiserData.advertiserId}</span> | 
        Budget: <span className="text-green-600">${advertiserData.budget}</span>
      </p>

      {/* Performance Metrics */}
      <div className="grid grid-cols-3 gap-6">
        {performanceData ? (
          <>
            <MetricsCard title="Total Clicks" value={performanceData.total_clicks} color="bg-blue-100" />
            <MetricsCard title="Total Conversions" value={performanceData.total_conversions} color="bg-green-100" />
            <MetricsCard title="Budget Utilization" value={`${((performanceData.total_spent / advertiserData.budget) * 100).toFixed(2)}%`} color="bg-yellow-100" />
          </>
        ) : (
          <p>Loading...</p>
        )}
      </div>

      {/* Budget Configurator */}
      <Configurator advertiserData={advertiserData} setAdvertiserData={setAdvertiserData} />

      {/* Live Bid Monitoring */}
      <RealTimeBidding />

      {/* Bid Chart */}
      <div className="mt-8">
        <BidChart />
      </div>
    </div>
  );
}

export default Dashboard;
