from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to access API

# Load pre-trained models (ensure these files exist in your backend folder)
market_price_model = joblib.load("market_price_model.pkl")
ctr_model = joblib.load("ctr_model.pkl")
cvr_model = joblib.load("cvr_model.pkl")

# Load bidding data (ensure the CSV file exists)
bids = pd.read_csv("bids_with_final_prices.csv")

@app.route("/")
def home():
    return jsonify({"message": "RTB Backend API is running!"})

# Fetch advertiser performance
@app.route("/api/performance", methods=["GET"])
def get_performance():
    performance = bids.groupby("AdvertiserID").agg(
        total_clicks=("Click", "sum"),
        total_conversions=("Conversion", "sum"),
        total_impressions=("Impression", "sum"),
        total_spent=("Payingprice", "sum")
    ).reset_index()

    performance["ctr"] = performance["total_clicks"] / performance["total_impressions"].replace(0, np.nan)
    performance["cvr"] = performance["total_conversions"] / performance["total_clicks"].replace(0, np.nan)
    performance.fillna(0, inplace=True)

    return jsonify(performance.to_dict(orient="records"))

# Fetch real-time bid data
@app.route("/api/realtime-bids", methods=["GET"])
def get_realtime_bids():
    sample_bids = bids.sample(10)[["BidID", "Biddingprice", "Payingprice", "Click", "Conversion"]].to_dict(orient="records")
    return jsonify(sample_bids)

# Fetch advertiser data
@app.route("/api/advertiser/<int:advertiser_id>", methods=["GET"])
def get_advertiser_data(advertiser_id):
    advertiser_data = bids[bids["AdvertiserID"] == advertiser_id].iloc[0].to_dict()
    return jsonify(advertiser_data)

# Update advertiser budget
@app.route("/api/advertiser/<int:advertiser_id>/update-budget", methods=["POST"])
def update_budget(advertiser_id):
    data = request.get_json()
    new_budget = data.get("budget")

    if new_budget is None or new_budget <= 0:
        return jsonify({"error": "Invalid budget value"}), 400

    return jsonify({"message": "Budget updated successfully!", "new_budget": new_budget})

# Run the server
if __name__ == "__main__":
    app.run(debug=True, port=5000)
