import { useState } from "react";
import axios from "axios";

function Configurator({ advertiserData, setAdvertiserData }) {
  const [newBudget, setNewBudget] = useState(advertiserData.budget);
  const [loading, setLoading] = useState(false);

  const handleBudgetChange = async () => {
    if (newBudget <= 0) {
      alert("Budget must be greater than 0.");
      return;
    }

    setLoading(true);
    
    try {
      await axios.post(`http://127.0.0.1:5000/api/advertiser/${advertiserData.advertiserId}/update-budget`, {
        budget: newBudget,
      });

      setAdvertiserData(prev => ({ ...prev, budget: newBudget }));
      alert("Budget updated successfully!");
    } catch (error) {
      console.error("Error updating budget:", error);
      alert("Failed to update budget.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg mt-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-3">Budget Controls</h3>
      <label className="block text-gray-700 font-semibold">Adjust Budget ($):</label>
      <input
        type="number"
        value={newBudget}
        onChange={(e) => setNewBudget(e.target.value)}
        className="w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        onClick={handleBudgetChange}
        className="mt-3 w-full bg-green-600 text-white p-2 rounded-lg font-semibold transition hover:bg-green-700"
        disabled={loading}
      >
        {loading ? "Updating..." : "Update Budget"}
      </button>
    </div>
  );
}

export default Configurator;
