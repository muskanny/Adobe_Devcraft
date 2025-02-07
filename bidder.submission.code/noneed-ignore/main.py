import os
import pandas as pd
import numpy as np

# Define file paths
data_dir = "dataset//dataset"
bid_files = [f for f in os.listdir(data_dir) if f.startswith("bid")]
impression_files = [f for f in os.listdir(data_dir) if f.startswith("imp")]
click_files = [f for f in os.listdir(data_dir) if f.startswith("clk")]
conversion_files = [f for f in os.listdir(data_dir) if f.startswith("conv")]

print("Found files:")
print("Bids:", bid_files)
print("Impressions:", impression_files)
print("Clicks:", click_files)
print("Conversions:", conversion_files)

# Advertiser-specific N values
advertiser_N = {1458: 0, 3358: 2, 3386: 0, 3427: 0, 3476: 10}

# Define column names
columns = ["BidID", "Timestamp", "Logtype", "VisitorID", "User-Agent", "IP", "Region", "City",
           "Adexchange", "Domain", "URL", "AnonymousURLID", "AdslotID", "Adslotwidth", "Adslotheight",
           "Adslotvisibility", "Adslotformat", "Adslotfloorprice", "CreativeID", "Biddingprice", "Payingprice",
           "KeypageURL", "AdvertiserID", "Targetting_Categories"]

def load_log_files(file_list, log_type, has_payingprice=False):
    """Loads log files efficiently with reduced memory usage."""
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

        df['LogType'] = log_type
        data.append(df)
    
    return pd.concat(data, ignore_index=True) if data else pd.DataFrame(columns=columns + ['LogType'])

# Load datasets
bids = load_log_files(bid_files, log_type='bid', has_payingprice=False)
impressions = load_log_files(impression_files, log_type='impression', has_payingprice=True)
clicks = load_log_files(click_files, log_type='click', has_payingprice=True)
conversions = load_log_files(conversion_files, log_type='conversion', has_payingprice=True)
print("Dataset Shapes:")
print("Bids:", bids.shape)
print("Impressions:", impressions.shape)
print("Clicks:", clicks.shape)
print("Conversions:", conversions.shape)
#Merge bids with impressions to get AdvertiserID
if 'BidID' in bids.columns and 'BidID' in impressions.columns and 'AdvertiserID' in impressions.columns:
    #imp_subset = impressions[['BidID', 'AdvertiserID']].copy()
    
    imp_subset = impressions.groupby('BidID')['AdvertiserID'].apply(list).reset_index()
    print(imp_subset.shape)
    #imp_subset['AdvertiserID'] = imp_subset['AdvertiserID'].astype('Int32')  # Convert to a compact type
    #bids = bids.merge(imp_subset, on='BidID', how='left')

    
else:
    print("Error: Missing required columns in bids or impressions.")


# Convert AdvertiserID to numeric type
# bids['AdvertiserID'] = pd.to_numeric(bids['AdvertiserID'], errors='coerce').astype('Int32')


# Convert necessary columns to numeric while keeping BidID as string
for df_name, df in zip(["Bids", "Impressions", "Clicks", "Conversions"], [bids, impressions, clicks, conversions]):
    for col in ['Biddingprice', 'Payingprice', 'AdvertiserID', 'Adslotfloorprice']:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('float32')
    print(f"Converted numeric columns for {df_name}")
# Debugging: Print first few rows
print("Sample Bids Data:")
print(bids.head(3))
print("Sample Impressions Data:")
print(impressions.head(3))

impressions.dropna(subset=['BidID'], inplace=True)
clicks.dropna(subset=['BidID'], inplace=True)
conversions.dropna(subset=['BidID'], inplace=True)

# Add 'Impression', 'Click', 'Conversion' columns to bids


bids['Impression'] = bids['BidID'].isin(impressions['BidID'])
bids['Click'] = bids['BidID'].isin(clicks['BidID'])
bids['Conversion'] = bids['BidID'].isin(conversions['BidID'])

print("Sample Bids Data:")
print(bids[['BidID', 'Biddingprice', 'Payingprice', 'Click', 'Conversion', 'AdvertiserID']].head(5))

# Compute scores and optimize budget allocation
def optimize_bidding(bids):
    if bids.empty or 'AdvertiserID' not in bids.columns:
        print("No valid bids data available.")
        return {}, {}

    # Ensure Payingprice is properly handled
    bids['EffectivePrice'] = bids['Payingprice'].fillna(bids['Biddingprice'])

    # Remove NaN AdvertiserIDs
    #bids.dropna(subset=['AdvertiserID'], inplace=True)
    
    # Convert to integer type
    #bids['AdvertiserID'] = bids['AdvertiserID'].astype('int32')

    # Compute total spending per advertiser
    advertiser_budgets = bids.groupby('AdvertiserID')['EffectivePrice'].sum().to_dict()

    # Compute scores
    bids['Score'] = bids['Click'].astype(int) + bids['Conversion'].astype(int) * bids['AdvertiserID'].map(advertiser_N).fillna(1)

    # Sum scores per advertiser
    advertiser_scores = bids.groupby('AdvertiserID')['Score'].sum().to_dict()

    return advertiser_scores, advertiser_budgets

# Run optimization
scores, advertiser_budgets = optimize_bidding(bids)

print("Advertiser Performance:")
for adv, score in scores.items():
    print(f"Advertiser {adv}: Score {score}, Budget Spent {advertiser_budgets[adv]}")

# 4import os
# import pandas as pd
# import numpy as np

# # Define file paths
# data_dir = "dataset\\dataset"
# bid_files = [f for f in os.listdir(data_dir) if f.startswith("bid")]
# impression_files = [f for f in os.listdir(data_dir) if f.startswith("imp")]
# click_files = [f for f in os.listdir(data_dir) if f.startswith("clk")]
# conversion_files = [f for f in os.listdir(data_dir) if f.startswith("conv")]

# print("Found files:")
# print("Bids:", bid_files)
# print("Impressions:", impression_files)
# print("Clicks:", click_files)
# print("Conversions:", conversion_files)

# # Advertiser-specific N values
# advertiser_N = {1458: 0, 3358: 2, 3386: 0, 3427: 0, 3476: 10}

# # Define column names
# columns = ["BidID", "Timestamp", "Logtype", "VisitorID", "User-Agent", "IP", "Region", "City",
#            "Adexchange", "Domain", "URL", "AnonymousURLID", "AdslotID", "Adslotwidth", "Adslotheight",
#            "Adslotvisibility", "Adslotformat", "Adslotfloorprice", "CreativeID", "Biddingprice", "Payingprice",
#            "KeypageURL", "AdvertiserID", "Targetting_Categories"]

# def load_log_files(file_list, log_type, has_payingprice=False):
#     """Loads log files efficiently with reduced memory usage."""
#     data = []
#     for file in file_list:
#         file_path = os.path.join(data_dir, file)
#         print(f"Loading {log_type} file: {file}")
        
#         df = pd.read_csv(file_path, delimiter='\t', header=None, dtype=str)
        
#         if has_payingprice:
#             df.columns = columns
#         else:
#             df.columns = [col for col in columns if col not in ['Payingprice', 'KeypageURL', 'Targetting_Categories']]
#             df['Payingprice'] = np.nan
#             df['KeypageURL'] = np.nan

#         df['LogType'] = log_type
#         data.append(df)
    
#     return pd.concat(data, ignore_index=True) if data else pd.DataFrame(columns=columns + ['LogType'])

# # Load datasets
# bids = load_log_files(bid_files, log_type='bid', has_payingprice=False)
# impressions = load_log_files(impression_files, log_type='impression', has_payingprice=True)
# clicks = load_log_files(click_files, log_type='click', has_payingprice=True)
# conversions = load_log_files(conversion_files, log_type='conversion', has_payingprice=True)

# print("Dataset Shapes:")
# print("Bids:", bids.shape)
# print("Impressions:", impressions.shape)
# print("Clicks:", clicks.shape)
# print("Conversions:", conversions.shape)

# # Convert necessary columns to numeric with reduced memory usage
# for df_name, df in zip(["Bids", "Impressions", "Clicks", "Conversions"], [bids, impressions, clicks, conversions]):
#     for col in ['BidID', 'Biddingprice', 'Payingprice', 'AdvertiserID', 'Adslotfloorprice']:
#         df[col] = pd.to_numeric(df[col], errors='coerce').astype('float32')
#     df['BidID'] = df['BidID'].astype('int32', errors='ignore')
#     print(f"Converted numeric columns for {df_name}")

# # Debugging: Print first few rows
# print("Sample Bids Data:")
# print(bids.head(3))
# print("Sample Impressions Data:")
# print(impressions.head(3))
# # Drop NaNs before converting to int
# impressions = impressions.dropna(subset=['BidID'])
# clicks = clicks.dropna(subset=['BidID'])
# conversions = conversions.dropna(subset=['BidID'])

# # Ensure integer type after handling NaNs
# impressions['BidID'] = impressions['BidID'].astype('int32')
# clicks['BidID'] = clicks['BidID'].astype('int32')
# conversions['BidID'] = conversions['BidID'].astype('int32')


# # Add 'Impression', 'Click', 'Conversion' columns to bids using optimized merge
# bids['Impression'] = bids['BidID'].isin(impressions['BidID'].astype('int32'))
# bids['Click'] = bids['BidID'].isin(clicks['BidID'].astype('int32'))
# bids['Conversion'] = bids['BidID'].isin(conversions['BidID'].astype('int32'))

# # Compute scores and optimize budget allocation
# def optimize_bidding(bids):
#     if bids.empty or 'AdvertiserID' not in bids.columns:
#         print("No valid bids data available.")
#         return {}, {}

#     # Ensure Payingprice is properly handled
#     bids['EffectivePrice'] = bids['Payingprice'].fillna(bids['Biddingprice'])

#     # Remove NaN AdvertiserIDs
#     bids = bids.dropna(subset=['AdvertiserID'])

#     # Convert to integer type
#     bids['AdvertiserID'] = bids['AdvertiserID'].astype('int32')

#     # Compute total spending per advertiser
#     advertiser_budgets = bids.groupby('AdvertiserID')['EffectivePrice'].sum().to_dict()

#     # Compute scores
#     bids['Score'] = bids['Click'].astype(int) + bids['Conversion'].astype(int) * bids['AdvertiserID'].map(advertiser_N).fillna(1)

#     # Sum scores per advertiser
#     advertiser_scores = bids.groupby('AdvertiserID')['Score'].sum().to_dict()

#     return advertiser_scores, advertiser_budgets


# # Run optimization
# scores, advertiser_budgets = optimize_bidding(bids)

# print("Advertiser Performance:")
# for adv, score in scores.items():
#     print(f"Advertiser {adv}: Score {score}, Budget Spent {advertiser_budgets[adv]}")

# 3import os
# import pandas as pd

# # Define file paths (Assuming all .txt files are in 'dataset' folder)
# data_dir = "dataset\\dataset"
# bid_files = [f for f in os.listdir(data_dir) if f.startswith("bid")]
# impression_files = [f for f in os.listdir(data_dir) if f.startswith("imp")]
# click_files = [f for f in os.listdir(data_dir) if f.startswith("clk")]
# conversion_files = [f for f in os.listdir(data_dir) if f.startswith("conv")]

# print("Found files:")
# print("Bids:", bid_files)
# print("Impressions:", impression_files)
# print("Clicks:", click_files)
# print("Conversions:", conversion_files)

# # Advertiser-specific N values
# advertiser_N = {1458: 0, 3358: 2, 3386: 0, 3427: 0, 3476: 10}

# # Define column names based on dataset format
# columns = ["BidID", "Timestamp", "Logtype", "VisitorID", "User-Agent", "IP", "Region", "City",
#            "Adexchange", "Domain", "URL", "AnonymousURLID", "AdslotID", "Adslotwidth", "Adslotheight",
#            "Adslotvisibility", "Adslotformat", "Adslotfloorprice", "CreativeID", "Biddingprice", "Payingprice",
#            "KeypageURL", "AdvertiserID", "Targetting_Categories"]

# def load_log_files(file_list, log_type, has_payingprice=False):
#     """Loads log files and assigns correct column names."""
#     data = []
#     for file in file_list:
#         file_path = os.path.join(data_dir, file)
#         print(f"Loading {log_type} file: {file}")
#         df = pd.read_csv(file_path, delimiter='\t', header=None, dtype=str)
#         if has_payingprice:
#             df.columns = columns
#         else:
#             df.columns = [col for col in columns if col not in ['Payingprice', 'KeypageURL', 'Targetting_Categories']]
#             df['Payingprice'] = None
#             df['KeypageURL'] = None

#         df['LogType'] = log_type
#         print(f"Loaded {log_type} file: {file}, Shape: {df.shape}")
#         data.append(df)
    
#     return pd.concat(data, ignore_index=True) if data else pd.DataFrame(columns=columns + ['LogType'])

# # Load datasets
# bids = load_log_files(bid_files, log_type='bid', has_payingprice=False)
# impressions = load_log_files(impression_files, log_type='impression', has_payingprice=True)
# clicks = load_log_files(click_files, log_type='click', has_payingprice=True)
# conversions = load_log_files(conversion_files, log_type='conversion', has_payingprice=True)

# print("Dataset Shapes:")
# print("Bids:", bids.shape)
# print("Impressions:", impressions.shape)
# print("Clicks:", clicks.shape)
# print("Conversions:", conversions.shape)

# # Convert necessary columns to numeric
# for df_name, df in zip(["Bids", "Impressions", "Clicks", "Conversions"], [bids, impressions, clicks, conversions]):
#     df['BidID'] = pd.to_numeric(df['BidID'], errors='coerce')
#     df['Biddingprice'] = pd.to_numeric(df['Biddingprice'], errors='coerce')
#     df['Payingprice'] = pd.to_numeric(df['Payingprice'], errors='coerce')
#     df['AdvertiserID'] = pd.to_numeric(df['AdvertiserID'], errors='coerce')
#     df['Adslotfloorprice'] = pd.to_numeric(df['Adslotfloorprice'], errors='coerce')
#     print(f"Converted numeric columns for {df_name}")

# # Debugging: Print the first few rows
# print("Sample Bids Data:")
# print(bids.head(3))
# print("Sample Impressions Data:")
# print(impressions.head(3))

# # Add 'Impression', 'Click', 'Conversion' columns to bids using merges
# bids = bids.merge(impressions[['BidID']], on='BidID', how='left', indicator='Impression')
# bids['Impression'] = (bids['Impression'] == 'both')

# bids = bids.merge(clicks[['BidID']], on='BidID', how='left', indicator='Click')
# bids['Click'] = (bids['Click'] == 'both')

# bids = bids.merge(conversions[['BidID']], on='BidID', how='left', indicator='Conversion')
# bids['Conversion'] = (bids['Conversion'] == 'both')

# # Fill NaN with False
# bids[['Impression', 'Click', 'Conversion']] = bids[['Impression', 'Click', 'Conversion']].fillna(False)

# # Compute scores and optimize budget allocation
# def optimize_bidding():
#     # Ensure Payingprice is properly handled
#     bids['EffectivePrice'] = bids['Payingprice'].fillna(bids['Biddingprice'])

#     # Compute total spending per advertiser
#     advertiser_budgets = bids.groupby('AdvertiserID')['EffectivePrice'].sum().to_dict()

#     # Compute scores
#     bids['Score'] = bids['Click'].astype(int) + bids['Conversion'].astype(int) * bids['AdvertiserID'].map(advertiser_N).fillna(1)

#     # Sum scores per advertiser
#     advertiser_scores = bids.groupby('AdvertiserID')['Score'].sum().to_dict()

#     return advertiser_scores, advertiser_budgets

# # Run optimization
# scores, advertiser_budgets = optimize_bidding()

# print("Advertiser Performance:")
# for adv, score in scores.items():
#     print(f"Advertiser {adv}: Score {score}, Budget Spent {advertiser_budgets[adv]}")

# 2
# import os
# import pandas as pd
# from collections import defaultdict

# # Define file paths (Assuming all .txt files are in 'dataset' folder)
# data_dir = "dataset\\dataset"
# bid_files = [f for f in os.listdir(data_dir) if f.startswith("bid")]
# impression_files = [f for f in os.listdir(data_dir) if f.startswith("imp")]
# click_files = [f for f in os.listdir(data_dir) if f.startswith("clk")]
# conversion_files = [f for f in os.listdir(data_dir) if f.startswith("conv")]

# print("Found files:")
# print("Bids:", bid_files)
# print("Impressions:", impression_files)
# print("Clicks:", click_files)
# print("Conversions:", conversion_files)

# # Advertiser-specific N values
# advertiser_N = {1458: 0, 3358: 2, 3386: 0, 3427: 0, 3476: 10}

# # Define column names based on dataset format
# columns = ["BidID", "Timestamp", "Logtype", "VisitorID", "User-Agent", "IP", "Region", "City",
#            "Adexchange", "Domain", "URL", "AnonymousURLID", "AdslotID", "Adslotwidth", "Adslotheight",
#            "Adslotvisibility", "Adslotformat", "Adslotfloorprice", "CreativeID", "Biddingprice", "Payingprice",
#            "KeypageURL", "AdvertiserID", "Targetting_Categories"]

# def load_log_files(file_list, log_type, has_payingprice=False):
#     """Loads log files and assigns correct column names."""
#     data = []
#     for file in file_list:
#         file_path = os.path.join(data_dir, file)
#         print(f"Loading {log_type} file: {file}")
#         df = pd.read_csv(file_path, delimiter='\t', header=None, dtype=str)
#         print(df.shape)
#         if has_payingprice:
#             df.columns = columns
#         else:
#             df.columns = [col for col in columns if col not in ['Payingprice', 'KeypageURL','Targetting_Categories']]
#             df['Payingprice'] = None
#             df['KeypageURL'] = None
#             df["Payingprice"] = None

#         df['LogType'] = log_type
#         print(f"Loaded {log_type} file: {file}, Shape: {df.shape}")
#         data.append(df)
    
#     return pd.concat(data, ignore_index=True) if data else pd.DataFrame(columns=columns + ['LogType'])

# # Load datasets
# bids = load_log_files(bid_files, log_type='bid', has_payingprice=False)
# impressions = load_log_files(impression_files, log_type='impression', has_payingprice=True)
# clicks = load_log_files(click_files, log_type='click', has_payingprice=True)
# conversions = load_log_files(conversion_files, log_type='conversion', has_payingprice=True)

# print("Dataset Shapes:")
# print("Bids:", bids.shape)
# print("Impressions:", impressions.shape)
# print("Clicks:", clicks.shape)
# print("Conversions:", conversions.shape)

# # Convert necessary columns to numeric
# for df_name, df in zip(["Bids", "Impressions", "Clicks", "Conversions"], [bids, impressions, clicks, conversions]):
#     df['Biddingprice'] = pd.to_numeric(df['Biddingprice'], errors='coerce')
#     df['Payingprice'] = pd.to_numeric(df['Payingprice'], errors='coerce')
#     df['AdvertiserID'] = pd.to_numeric(df['AdvertiserID'], errors='coerce')
#     df['Adslotfloorprice'] = pd.to_numeric(df['Adslotfloorprice'], errors='coerce')
#     print(f"Converted numeric columns for {df_name}")

# # Debugging: Print the first few rows
# print("Sample Bids Data:")
# print(bids.head(3))
# print("Sample Impressions Data:")
# print(impressions.head(3))

# # Map bids to impressions, clicks, and conversions
# bid_outcomes = defaultdict(lambda: {'Impression': False, 'Click': False, 'Conversion': False})
# for _, row in impressions.iterrows():
#     bid_outcomes[row['BidID']]['Impression'] = True
# for _, row in clicks.iterrows():
#     bid_outcomes[row['BidID']]['Click'] = True
# for _, row in conversions.iterrows():
#     bid_outcomes[row['BidID']]['Conversion'] = True

# print("Sample bid outcomes:")
# print(list(bid_outcomes.items())[:5])

# # Compute scores and optimize budget allocation
# advertiser_budgets = defaultdict(float)
# advertiser_scores = defaultdict(float)

# def optimize_bidding():
#     global advertiser_budgets, advertiser_scores
    
#     for _, bid in bids.iterrows():
#         adv_id = bid['AdvertiserID']
#         bid_id = bid['BidID']
#         paying_price = bid['Payingprice'] if pd.notna(bid['Payingprice']) else bid['Biddingprice']
        
#         # Deduct from advertiser budget
#         advertiser_budgets[adv_id] += paying_price if paying_price is not None else 0
        
#         # Calculate score
#         score = int(bid_outcomes[bid_id]['Click']) + advertiser_N.get(adv_id, 1) * int(bid_outcomes[bid_id]['Conversion'])
#         advertiser_scores[adv_id] += score
    
#     return advertiser_scores

# # Run optimization
# scores = optimize_bidding()
# print("Advertiser Performance:")
# for adv, score in scores.items():
#     print(f"Advertiser {adv}: Score {score}, Budget Spent {advertiser_budgets[adv]}")


#1
# import os
# import pandas as pd
# from collections import defaultdict

# # Define file paths (Assuming all .txt files are in 'dataset' folder)
# data_dir = "dataset\\dataset"
# bid_files = [f for f in os.listdir(data_dir) if f.startswith("bid")]
# impression_files = [f for f in os.listdir(data_dir) if f.startswith("imp")]
# click_files = [f for f in os.listdir(data_dir) if f.startswith("clk")]
# conversion_files = [f for f in os.listdir(data_dir) if f.startswith("conv")]

# print("found files: ")
# print("bids: ", bid_files)

# # Advertiser-specific N values
# advertiser_N = {1458: 0, 3358: 2, 3386: 0, 3427: 0, 3476: 10}

# # Load log files
# def load_log_files(file_list, columns, log_type):
#     data = []
#     for file in file_list:
#         file_path = os.path.join(data_dir, file)
#         print(f"Loading {log_type} file: {file}")
#         df = pd.read_csv(file_path, delimiter='\t', names=columns, dtype=str)
#         df['LogType'] = log_type
#         data.append(df)
#     return pd.concat(data, ignore_index=True) if data else pd.DataFrame(columns=columns + ['LogType'])

# # Define column names (based on the format shared)
# columns = ["BidID", "Timestamp", "Logtype", "VisitorID", "User-Agent", "IP", "Region", "City",
#            "Adexchange", "Domain", "URL", "AnonymousURLID", "AdslotID", "Adslotwidth", "Adslotheight",
#            "Adslotvisibility", "Adslotformat", "Adslotfloorprice", "CreativeID", "Biddingprice", "Payingprice",
#            "KeypageURL", "AdvertiserID"]

# # Load datasets
# bids = load_log_files(bid_files, columns, log_type='bid')
# impressions = load_log_files(impression_files, columns, log_type='impression')
# clicks = load_log_files(click_files, columns, log_type='click')
# conversions = load_log_files(conversion_files, columns, log_type='conversion')

# # Convert necessary columns to numeric
# for df in [bids, impressions, clicks, conversions]:
#     df['Biddingprice'] = pd.to_numeric(df['Biddingprice'], errors='coerce')
#     df['Payingprice'] = pd.to_numeric(df['Payingprice'], errors='coerce')
#     df['AdvertiserID'] = pd.to_numeric(df['AdvertiserID'], errors='coerce')
#     df['Adslotfloorprice'] = pd.to_numeric(df['Adslotfloorprice'], errors='coerce')

# # Map bids to impressions, clicks, and conversions
# bid_outcomes = defaultdict(lambda: {'Impression': False, 'Click': False, 'Conversion': False})
# for _, row in impressions.iterrows():
#     bid_outcomes[row['BidID']]['Impression'] = True
# for _, row in clicks.iterrows():
#     bid_outcomes[row['BidID']]['Click'] = True
# for _, row in conversions.iterrows():
#     bid_outcomes[row['BidID']]['Conversion'] = True

# # Compute scores and optimize budget allocation
# advertiser_budgets = defaultdict(float)
# advertiser_scores = defaultdict(float)

# def optimize_bidding():
#     global advertiser_budgets, advertiser_scores
    
#     for _, bid in bids.iterrows():
#         adv_id = bid['AdvertiserID']
#         bid_id = bid['BidID']
#         paying_price = bid['Payingprice'] if pd.notna(bid['Payingprice']) else bid['Biddingprice']
        
#         # Deduct from advertiser budget
#         advertiser_budgets[adv_id] += paying_price
        
#         # Calculate score
#         score = int(bid_outcomes[bid_id]['Click']) + advertiser_N.get(adv_id, 1) * int(bid_outcomes[bid_id]['Conversion'])
#         advertiser_scores[adv_id] += score
    
#     return advertiser_scores

# # Run optimization
# scores = optimize_bidding()
# print("Advertiser Performance:")
# for adv, score in scores.items():
#     print(f"Advertiser {adv}: Score {score}, Budget Spent {advertiser_budgets[adv]}")
