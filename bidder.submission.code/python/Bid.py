from Bidder import Bidder
from BidRequest import BidRequest
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import xgboost as xgb

from sklearn.preprocessing import LabelEncoder

class Bid:
    def __init__(self, budget, advertiser_N, ctr_model, cvr_model, historical_data):
        self.budget = budget
        self.advertiser_N = advertiser_N
        self.ctr_model = ctr_model
        self.cvr_model = cvr_model
        self.historical_data = historical_data
        self.label_encoders = {}

    def preprocess_features(self, features):
        """Convert categorical variables to numerical format."""
        for col in features.select_dtypes(include=['object']).columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                features[col] = self.label_encoders[col].fit_transform(features[col].astype(str))
            else:
                features[col] = self.label_encoders[col].transform(features[col].astype(str))
        return features.astype(float)

    def getBidPrice(self, bid_request):
        """Compute bid price using ML model-based predictions."""
        advertiser_id = bid_request.getAdvertiserId()
        floor_price = bid_request.getAdSlotFloorPrice()

        # Define the input feature vector for ML model
        features = pd.DataFrame([{
            "Hour": hour,
            "Adslotwidth": bid_request.getAdSlotWidth(),
            "Adslotheight": bid_request.getAdSlotHeight(),
            "Adslotvisibility": bid_request.getAdSlotVisibility(),
            "Adslotfloorprice": floor_price,
            "Biddingprice": floor_price,  # Initial bid assumption
            "Region": bid_request.getRegion(),
            "City": bid_request.getCity(),
            "Adexchange": bid_request.getAdExchange(),
            "AdvertiserID": advertiser_id
        }])

        features.fillna(0, inplace=True)
        features = self.preprocess_features(features)  # Convert categorical data

        # Predict CTR & CVR
        ctr_pred = self.ctr_model.predict_proba(features)[:, 1]  # Click probability
        cvr_pred = self.cvr_model.predict_proba(features)[:, 1]  # Conversion probability

        # Get advertiser-specific N value (default = 1)
        N = self.advertiser_N.get(advertiser_id, 1)

        # Compute Expected Value for bid optimization
        expected_value = ctr_pred * (1 + N * cvr_pred)

        # Scale bid based on the mean historical bidding price
        optimized_bid = expected_value * self.historical_data["Biddingprice"].mean()

        # Ensure bid is above floor price and within budget
        final_bid = max(optimized_bid, floor_price)
        if final_bid > self.budget:
            return -1  # Skip bidding if the bid exceeds budget

        return final_bid

# Load trained ML models
ctr_model = xgb.XGBClassifier()
cvr_model = xgb.XGBClassifier()
ctr_model.load_model("ctr_model.json")  # Load trained models
cvr_model.load_model("cvr_model.json")

# Define advertiser-specific N values
advertiser_N = {1458: 0, 3358: 2, 3386: 0, 3427: 0, 3476: 10}

# Assume `bids` is your dataset for historical data
historical_data =bids  # comes from running main.py

# Initialize Bid class with ML models
bidder = Bid(budget=1000000, advertiser_N=advertiser_N, ctr_model=ctr_model, cvr_model=cvr_model, historical_data=historical_data)

# Example Bid Requests
bid_requests = [
    BidRequest(advertiser_id=1458, adslot_id=123, region="12", floor_price=5.0),
    BidRequest(advertiser_id=3358, adslot_id=456, region="12", floor_price=10.0),
]

# Simulate bidding
for bid_request in bid_requests:
    bid_price = bidder.getBidPrice(bid_request)
    if bid_price != -1:
        print(f"Bid placed: {bid_price} for Advertiser {bid_request.getAdvertiserId()}")
    else:
        print(f"No bid placed for Advertiser {bid_request.getAdvertiserId()}")


#-----------------------------------NON ML APPROACH---------------------------------------
# class Bid(Bidder):
#     def __init__(self, budget, advertiser_N, historical_data):
#         self.budget = budget
#         self.advertiser_N = advertiser_N
#         self.remaining_budget = budget
#         self.historical_data = historical_data  # Preprocessed historical data
#         self.total_clicks = 0
#         self.total_conversions = 0

#     def getHistoricalCTR(self, bid_request):
#         # Extract relevant features from the bid request
#         advertiser_id = bid_request.getAdvertiserId()
#         adslot_id = bid_request.getAdSlotID()
#         region = bid_request.getRegion()

#         # Find the closest match in historical data
#         match = self.historical_data[
#             (self.historical_data['AdvertiserID'] == advertiser_id) &
#             (self.historical_data['AdslotID'] == adslot_id) &
#             (self.historical_data['Region'] == region)
#         ]

#         # Return the matched CTR or a default value
#         if not match.empty:
#             return match['CTR'].values[0]
#         else:
#             return 0.01  # Default CTR

#     def getHistoricalCVR(self, bid_request):
#         # Extract relevant features from the bid request
#         advertiser_id = bid_request.getAdvertiserId()
#         adslot_id = bid_request.getAdSlotID()
#         region = bid_request.getRegion()

#         # Find the closest match in historical data
#         match = self.historical_data[
#             (self.historical_data['AdvertiserID'] == advertiser_id) &
#             (self.historical_data['AdslotID'] == adslot_id) &
#             (self.historical_data['Region'] == region)
#         ]

#         # Return the matched CVR or a default value
#         if not match.empty:
#             return match['CVR'].values[0]
#         else:
#             return 0.001  # Default CVR

#     def getBidPrice(self, bid_request):
#         # Estimate CTR and CVR
#         ctr = self.getHistoricalCTR(bid_request)
#         cvr = self.getHistoricalCVR(bid_request)

#         # Calculate expected value
#         advertiser_id = bid_request.getAdvertiserId()
#         n = self.advertiser_N.get(advertiser_id, 0)
#         expected_value = ctr * (1 + n * cvr)

#         # Scale the bid price dynamically
#         scaling_factor = min(1000, self.remaining_budget / expected_value)
#         bid_price = expected_value * scaling_factor

#         # Ensure the bid price meets the floor price
#         floor_price = bid_request.getAdSlotFloorPrice()
#         bid_price = max(bid_price, floor_price)

#         # Ensure the bid price does not exceed the remaining budget
#         if bid_price <= self.remaining_budget:
#             self.remaining_budget -= bid_price
#             return bid_price
#         else:
#             return -1  # No bid placed