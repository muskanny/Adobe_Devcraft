import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Landing({ setAdvertiserData }) {
  const [advertiserId, setAdvertiserId] = useState("");
  const [budget, setBudget] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!advertiserId || !budget) {
      alert("Please fill in all fields.");
      return;
    }

    setLoading(true);

    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/advertiser/${advertiserId}`);
      setAdvertiserData({ ...response.data, budget });
      navigate("/dashboard");
    } catch (error) {
      alert("Invalid Advertiser ID. Please enter a valid one.");
      console.error("Error fetching advertiser data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gradient-to-r from-blue-500 to-indigo-600">
      <div className="bg-white p-8 rounded-lg shadow-lg w-96">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">
          Advertiser Login
        </h2>
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-gray-700 font-semibold">Advertiser ID:</label>
            <input
              type="number"
              value={advertiserId}
              onChange={(e) => setAdvertiserId(e.target.value)}
              className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <div>
            <label className="block text-gray-700 font-semibold">Budget ($):</label>
            <input
              type="number"
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-600 text-white p-3 rounded-lg font-semibold text-lg transition hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? "Loading..." : "Proceed to Dashboard"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Landing;
