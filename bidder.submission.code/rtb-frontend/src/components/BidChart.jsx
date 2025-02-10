import { useEffect, useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import "chart.js/auto";

function BidChart() {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: "Bid Prices ($)",
        data: [],
        borderColor: "rgb(59, 130, 246)", // Blue
        backgroundColor: "rgba(59, 130, 246, 0.2)",
        tension: 0.3,
      },
    ],
  });

  useEffect(() => {
    const fetchBidData = () => {
      axios.get("http://127.0.0.1:5000/api/realtime-bids")
        .then(response => {
          const bids = response.data;

          // Extract timestamps and bid prices for the chart
          const labels = bids.map((bid, index) => `Bid ${index + 1}`);
          const bidPrices = bids.map(bid => bid.Biddingprice);

          setChartData({
            labels: labels,
            datasets: [
              {
                label: "Bid Prices ($)",
                data: bidPrices,
                borderColor: "rgb(59, 130, 246)", // Blue
                backgroundColor: "rgba(59, 130, 246, 0.2)",
                tension: 0.3,
              },
            ],
          });
        })
        .catch(error => console.error("Error fetching bid chart data:", error));
    };

    fetchBidData();
    const interval = setInterval(fetchBidData, 5000); // Refresh every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h3 className="text-lg font-semibold mb-3 text-gray-800">Bid Price Trends</h3>
      <Line data={chartData} />
    </div>
  );
}

export default BidChart;
