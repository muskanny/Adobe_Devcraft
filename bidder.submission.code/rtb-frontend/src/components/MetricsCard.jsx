function MetricsCard({ title, value, color }) {
    // Format large numbers with commas, default to "N/A" if value is undefined
    const formattedValue = value !== undefined ? new Intl.NumberFormat().format(value) : "N/A";
  
    return (
      <div className={`p-6 rounded-lg shadow-lg ${color} text-gray-800`}>
        <h3 className="text-lg font-semibold">{title}</h3>
        <p className="text-3xl font-bold mt-2">{formattedValue}</p>
      </div>
    );
  }
  
  export default MetricsCard;
  