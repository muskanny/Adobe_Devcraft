from Bidder import Bidder
from BidRequest import BidRequest
import pandas as pd
import numpy as np

class Bid(Bidder):
    def __init__(self, budget, advertiser_N, historical_data):
        self.budget = budget
        self.advertiser_N = advertiser_N
        self.remaining_budget = budget
        self.historical_data = historical_data  # Preprocessed historical data
        self.total_clicks = 0
        self.total_conversions = 0

    def getHistoricalCTR(self, bid_request):
        # Extract relevant features from the bid request
        advertiser_id = bid_request.getAdvertiserId()
        adslot_id = bid_request.getAdSlotID()
        region = bid_request.getRegion()

        # Find the closest match in historical data
        match = self.historical_data[
            (self.historical_data['AdvertiserID'] == advertiser_id) &
            (self.historical_data['AdslotID'] == adslot_id) &
            (self.historical_data['Region'] == region)
        ]

        # Return the matched CTR or a default value
        if not match.empty:
            return match['CTR'].values[0]
        else:
            return 0.01  # Default CTR

    def getHistoricalCVR(self, bid_request):
        # Extract relevant features from the bid request
        advertiser_id = bid_request.getAdvertiserId()
        adslot_id = bid_request.getAdSlotID()
        region = bid_request.getRegion()

        # Find the closest match in historical data
        match = self.historical_data[
            (self.historical_data['AdvertiserID'] == advertiser_id) &
            (self.historical_data['AdslotID'] == adslot_id) &
            (self.historical_data['Region'] == region)
        ]

        # Return the matched CVR or a default value
        if not match.empty:
            return match['CVR'].values[0]
        else:
            return 0.001  # Default CVR

    def getBidPrice(self, bid_request):
        # Estimate CTR and CVR
        ctr = self.getHistoricalCTR(bid_request)
        cvr = self.getHistoricalCVR(bid_request)

        # Calculate expected value
        advertiser_id = bid_request.getAdvertiserId()
        n = self.advertiser_N.get(advertiser_id, 0)
        expected_value = ctr * (1 + n * cvr)

        # Scale the bid price dynamically
        scaling_factor = min(1000, self.remaining_budget / expected_value)
        bid_price = expected_value * scaling_factor

        # Ensure the bid price meets the floor price
        floor_price = bid_request.getAdSlotFloorPrice()
        bid_price = max(bid_price, floor_price)

        # Ensure the bid price does not exceed the remaining budget
        if bid_price <= self.remaining_budget:
            self.remaining_budget -= bid_price
            return bid_price
        else:
            return -1  # No bid placed