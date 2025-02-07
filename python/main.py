import os
import pandas as pd
import numpy as np
from Bid import Bid
from BidRequest import BidRequest

# Define file paths
data_dir = "/content/drive/MyDrive"  # Update this path to your dataset location
bid_files = [f for f in os.listdir(data_dir) if f.startswith("bid")]
impression_files = [f for f in os.listdir(data_dir) if f.startswith("imp")]
click_files = [f for f in os.listdir(data_dir) if f.startswith("clk")]
conversion_files = [f for f in os.listdir(data_dir) if f.startswith("conv")]

# Define column names
columns = ["BidID", "Timestamp", "Logtype", "VisitorID", "User-Agent", "IP", "Region", "City",
           "Adexchange", "Domain", "URL", "AnonymousURLID", "AdslotID", "Adslotwidth", "Adslotheight",
           "Adslotvisibility", "Adslotformat", "Adslotfloorprice", "CreativeID", "Biddingprice", "Payingprice",
           "KeypageURL", "AdvertiserID", "Targetting_Categories"]

columnsbid = ["BidID", "Timestamp", "VisitorID", "User-Agent", "IP", "Region", "City", "Adexchange", "Domain", "URL",
             "AnonymousURLID", "AdslotID", "Adslotwidth", "Adslotheight", "Adslotvisibility", "Adslotformat",
             "Adslotfloorprice", "CreativeID", "Biddingprice", "Payingprice", "AdvertiserID", "Logtype", "KeypageURL",
             "Targetting_Categories"]

# Function to load log files
def load_log_files(file_list, log_type, has_payingprice=False):
    data = []
    for file in file_list:
        file_path = os.path.join(data_dir, file)
        print(f"Loading {log_type} file: {file}")

        df = pd.read_csv(file_path, delimiter='\t', header=None, dtype=str)

        if has_payingprice:
            df.columns = columns
        else:
            df.columns = [col for col in columns if col not in ['Payingprice', 'KeypageURL', 'Targetting_Categories']]
            df['Payingprice'] = np.nan
            df['KeypageURL'] = np.nan

        data.append(df)

    return pd.concat(data, ignore_index=True) if data else pd.DataFrame(columns=columns + ['LogType'])

# Load datasets
impressions = load_log_files(impression_files, log_type='impression', has_payingprice=True)
clicks = load_log_files(click_files, log_type='click', has_payingprice=True)
conversions = load_log_files(conversion_files, log_type='conversion', has_payingprice=True)
bids = load_log_files(bid_files, log_type='bid', has_payingprice=False)

# Convert necessary columns to numeric
for df in [bids, impressions, clicks, conversions]:
    for col in ['Biddingprice', 'Payingprice', 'Adslotfloorprice']:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('float32')

# Add 'Impression', 'Click', 'Conversion' columns to bids
bids['Impression'] = bids['BidID'].isin(impressions['BidID']).astype(int)
bids['Click'] = bids['BidID'].isin(clicks['BidID']).astype(int)
bids['Conversion'] = bids['BidID'].isin(conversions['BidID']).astype(int)

# Preprocess historical data
def preprocess_historical_data(bids):
    # Group by relevant features and calculate CTR and CVR
    historical_data = bids.groupby(
        ['AdvertiserID', 'AdslotID', 'Region']
    ).agg(
        Impressions=('Impression', 'sum'),
        Clicks=('Click', 'sum'),
        Conversions=('Conversion', 'sum')
    ).reset_index()

    # Calculate CTR and CVR
    historical_data['CTR'] = historical_data['Clicks'] / historical_data['Impressions']
    historical_data['CVR'] = historical_data['Conversions'] / historical_data['Clicks']

    # Handle NaN values
    historical_data['CTR'] = historical_data['CTR'].fillna(0.01)  # Default CTR
    historical_data['CVR'] = historical_data['CVR'].fillna(0.001)  # Default CVR

    return historical_data

# Preprocess the bids data
historical_data = preprocess_historical_data(bids)

# Define advertiser-specific N values
advertiser_N = {1458: 0, 3358: 2, 3386: 0, 3427: 0, 3476: 10}

# Initialize the Bid class
total_budget = 10000000  # Example total budget
bidder = Bid(total_budget, advertiser_N, historical_data)

# Example list of BidRequest objects
bid_requests = [
    BidRequest(advertiser_id=1458, adslot_id=123, region=1, floor_price=5.0),
    BidRequest(advertiser_id=3358, adslot_id=456, region=2, floor_price=10.0),
    # Add more BidRequest objects as needed
]

# Simulate bidding
for bid_request in bid_requests:
    bid_price = bidder.getBidPrice(bid_request)
    if bid_price != -1:
        print(f"Bid placed: {bid_price} for Advertiser {bid_request.getAdvertiserId()}")
    else:
        print(f"No bid placed for Advertiser {bid_request.getAdvertiserId()}")