# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os
import joblib

# Load models from disk
clicks_model = joblib.load(r"C:\\Users\\w10\\Downloads\\ctr_model (2).pkl")
conv_model = joblib.load(r"C:\\Users\\w10\\Downloads\\cvr_model (2).pkl")
bp_model = joblib.load(r"C:\\Users\\w10\\Downloads\\bid_price_model (2).pkl")

def main():
    # Setting Application title
    st.title('Number of Impressions, Clicks, Conversions and Bidding Price Prediction App')

    # Setting Application description
    st.markdown("""
     :dart:  This App is made to predict Number of Clicks, Conversions and Bidding Price from the saved model.
    The application is functional for online prediction.
    """)

    # Setting Application sidebar default
    image = Image.open(str(os.curdir) + "\\genai.png")
    st.sidebar.info('This app is created to predict Number of Impressions, Clicks, Conversions and Bidding Price')
    st.sidebar.image(image)
    st.info("Input data below")

    # Based on our optimal features selection
    st.subheader("Enter data for predicting impressions, clicks and conversions")

    # Input Fields
    adslotwidth = st.number_input("Adslot Width (px)", min_value=1, value=300)
    adslotheight = st.number_input("Adslot Height (px)", min_value=1, value=250)
   
    adslotfloorprice = st.number_input("Adslot Floor Price", min_value=0, value=0)
    market_price_estimate = st.number_input("Market Price Estimate", min_value=0, value=15)
    advertiser_id = st.number_input("Advertiser ID", min_value=1, value=2345)
    adexchange_1 = st.selectbox("Ad Exchange 1", options=[0, 1], index=0)
    adexchange_2 = st.selectbox("Ad Exchange 2", options=[0, 1], index=0)
    adexchange_3 = st.selectbox("Ad Exchange 3", options=[0, 1], index=0)
    rolling_ctr = st.number_input("Rolling CTR", min_value=0.0, value=0.02)
    rolling_cvr = st.number_input("Rolling CVR", min_value=0.0, value=0.05)
    # Precomputed interaction feature
    budget_remaining = st.number_input('Enter Advertiser Budget:', min_value=0.0, value=1000000.0)


# Prepare the data for prediction
    new_data = {
        "Adslotwidth": adslotwidth,
        "Adslotheight": adslotheight,
        
        "Adslotfloorprice": adslotfloorprice,
        "MarketPriceEstimate": market_price_estimate,
        "AdvertiserID": advertiser_id,
        "Adexchange_1": adexchange_1,
        "Adexchange_2": adexchange_2,
        "Adexchange_3": adexchange_3,
        "RollingCTR": rolling_ctr,
        "RollingCVR": rolling_cvr,
       
    }
    features_df = pd.DataFrame.from_dict([new_data])
    st.info('Overview of input is shown below')
    st.dataframe(features_df)

    # Input fields for bidding price prediction
    st.subheader("Enter data for predicting bidding price")
    # Input Fields
    # adslotwidth = st.number_input("Adslot Width (px)", min_value=1, value=300)
    # adslotheight = st.number_input("Adslot Height (px)", min_value=1, value=250)
    # log_biddingprice = st.number_input("Log of Bidding Price", min_value=0.0, value=np.log1p(753))
    # adslotfloorprice = st.number_input("Adslot Floor Price", min_value=0, value=0)
    # market_price_estimate = st.number_input("Market Price Estimate", min_value=0, value=15)
    # advertiser_id = st.number_input("Advertiser ID", min_value=1, value=2345)
    # adexchange_1 = st.selectbox("Ad Exchange 1", options=[0, 1], index=0)
    # adexchange_2 = st.selectbox("Ad Exchange 2", options=[0, 1], index=0)
    # adexchange_3 = st.selectbox("Ad Exchange 3", options=[0, 1], index=0)
    # rolling_ctr = st.number_input("Rolling CTR", min_value=0.0, value=0.02)
    # rolling_cvr = st.number_input("Rolling CVR", min_value=0.0, value=0.05)
    # adslot_bidding_interaction = adslotwidth * log_biddingprice  # Precomputed interaction feature
    advertiser_N = {1458: 0, 3358: 2, 3386: 0, 3427: 0, 3476: 10}
    biddata = {
        "Adslotwidth": adslotwidth,
        "Adslotheight": adslotheight,
      
        "Adslotfloorprice": adslotfloorprice,
        "MarketPriceEstimate": market_price_estimate,
        "AdvertiserID": advertiser_id,
        "Adexchange_1": adexchange_1,
        "Adexchange_2": adexchange_2,
        "Adexchange_3": adexchange_3,
        "RollingCTR": rolling_ctr,
        "RollingCVR": rolling_cvr,
        
    }
        
    bidfeatures_df = pd.DataFrame.from_dict([biddata])
    st.info('Overview of input is shown below')
    st.dataframe(bidfeatures_df)
    action = st.button('Predict')
    if action:
        # Predict CTR and CVR
        predicted_ctr = clicks_model.predict(features_df)[0]
        predicted_cvr = conv_model.predict(features_df)[0]

        # Predict Bidding Price
        predicted_bidding_price = bp_model.predict(bidfeatures_df)[0]
        
        # Calculate Advertiser Score
        N = advertiser_N.get(advertiser_id, 1)  # Get N for advertiser
        score = predicted_ctr + (N * predicted_cvr)

        # Calculate Estimated Spend
        estimated_spend = predicted_bidding_price * 1000  # Assuming CPM (cost per 1000 impressions)

        # Check Budget Constraint
        if estimated_spend <= budget_remaining:
            bid_decision = f"✅ Placing bid of {predicted_bidding_price:.4f} (within budget)"
        else:
            bid_decision = "❌ Bid exceeds budget. Consider adjusting bidding price."

        # Display Results
        st.text_area(
            "Prediction Results",
            f"📌 Predicted CTR: {predicted_ctr:.6f}\n"
            f"📌 Predicted CVR: {predicted_cvr:.6f}\n"
            f"📌 Predicted Bidding Price: {predicted_bidding_price:.4f}\n"
            f"📌 Advertiser Score: {score:.6f}\n"
            f"📌 Budget Remaining: {budget_remaining:.2f}\n"
            f"📌 Estimated Spend: {estimated_spend:.2f}\n"
            f"📌 Bid Decision: {bid_decision}"
        )

if __name__ == '__main__':
    main()
#     # Action button to trigger prediction
#     action = st.button('Predict')
#     if action:
#         # Predictions for impressions, clicks, conversions, and bidding price
#         impressions = features_df['Adslotwidth'] * features_df['Adslotheight']  # Example prediction logic for impressions
#         clicks = clicks_model.predict(features_df)
#         conversions = conv_model.predict(features_df)
#         CTR = (clicks / impressions) * 100
#         CVR = (conversions / clicks) * 100
#         expected_conversions = impressions * CTR / 100 * CVR / 100
#         biddingprice = bp_model.predict(bidfeatures_df)

#         # Display predictions
#         st.text_area("Predicted Values:", 
#                      "- Predicted # of Impressions: " + str(impressions[0]) + "\n" +
#                      " - Predicted # of Clicks: " + str(clicks[0]) + "\n" +
#                      " - Predicted # of Conversions: " + str(conversions[0]) + "\n" +
#                      " - Predicted Click Through Rate: " + str(CTR[0]) + "%" + "\n" +
#                      " - Predicted Conversion Rate: " + str(CVR[0]) + "%" + "\n" +
#                      " - Expected Conversions: " + str(expected_conversions[0]) + "\n" +
#                      " - Predicted Bidding Price: " + str(biddingprice[0]), 200)

# if __name__ == '__main__':
#     main()

# #Import libraries
# import streamlit as st
# import pandas as pd
# import numpy as np
# from PIL import Image
# import os
# #load the model from disk
# import joblib
# clicks_model = joblib.load(r"C:\\Users\\w10\\Downloads\\ctr_model.sav")
# conv_model = joblib.load(r"C:\\Users\\w10\\Downloads\\cvr_model.sav")
# #imp_model = joblib.load(r"C:\\Users\\w10\\Downloads\\imp_model.sav")
# bp_model = joblib.load(r"C:\\Users\\w10\\Downloads\\bidmodel.sav")

# #Import python scripts
# #import preprocess

# def main():
#     #Setting Application title
#     st.title('Number of Impressions, Clicks, Conversions and Bidding Price Prediction App')

#       #Setting Application description
#     st.markdown("""
#      :dart:  This App is made to predict Number of Clicks, Conversions and Bidding Price from the saved model.
#     The application is functional for online prediction.
#     """)
#     #st.markdown("<h3></h3>", unsafe_allow_html=True)

#     #Setting Application sidebar default
#     image = Image.open(str(os.curdir)+"\\genai.png")
#     #add_selectbox = st.sidebar.selectbox(
#     #"How would you like to predict?", ("Online", "Batch"))
#     st.sidebar.info('This app is created to predict Number of Impressions, Clicks, Conversions and Bidding Price')
#     st.sidebar.image(image)
#     st.info("Input data below")

#     #Based on our optimal features selection
#     st.subheader("Enter data for predicting impressions, clicks and conversions")

#     region = st.number_input('Region:', step=1)
#     city = st.number_input('City:', step=1)
#     #st.selectbox('Region:',[{'USA':12, 'UK':14, 'India':15}])
#     adexchange = st.selectbox('AdExchange:', [1,2,3])
#     adslotwidth = st.number_input('Ad Slot Width:', step=1)
#     adslotheight = st.number_input('Ad Slot Height:', step=1)
#     adslotvisibility = st.selectbox('Ad Slot Visibility:', [0,1,2,255])
#     adslotformat = st.selectbox('Ad Slot Format:', [0,1,5])
           
#     data = {
#             'Region': region,
#             'City': city,
#             'Adexchange': adexchange,
#             'Adslotwidth': adslotwidth,
#             'Adslotheight': adslotheight,
#             'Adslotvisibility': adslotvisibility,
#             'Adslotformat': adslotformat
#             }
        
#     features_df = pd.DataFrame.from_dict([data])
#     st.info('Overview of input is shown below')
#     st.dataframe(features_df)

#     st.subheader("Enter data for predicting bidding price")

#     MarketPriceEstimate= st.number_input('MarketPriceEstimate:', step=0.0001)
#     HistoricalCTR = st.number_input('HistoricalCTR:', step=1)
#     HistoricalCVR = st.number_input('HistoricalCVR:', step=1)
#     WinRate = st.number_input('WinRate:', step=0.000001)
#     Adslotfloorprice = st.number_input('Adslotfloorprice:', step=0.1)

#     biddata = {
#             'MarketPriceEstimate': MarketPriceEstimate,
#             'HistoricalCTR': HistoricalCTR,
#             'HistoricalCVR': HistoricalCVR,
#             'WinRate': WinRate,
#             'Adslotfloorprice': Adslotfloorprice
#             }
        
#     bidfeatures_df = pd.DataFrame.from_dict([biddata])
#     st.info('Overview of input is shown below')
#     st.dataframe(bidfeatures_df)

#     #Preprocess inputs
#     #preprocess_df = preprocess.preprocess(features_df, 'Online')
#     action = st.button('Predict')
#     if action:
#         impressions = imp_model.predict(features_df)
#         clicks = clicks_model.predict(features_df)
#         conversions = conv_model.predict(features_df)
#         CTR = (clicks/impressions)*100
#         CVR = (conversions/clicks)*100
#         expected_conversions = impressions * CTR/100 * CVR/100
#         biddingprice = bp_model.predict(bidfeatures_df)
    
#         st.text_area("Predicted Values:", "- Predicted # of Impressions: " + str(impressions) + "\n" + 
#                      " - Predicted # of Clicks: " + str(clicks) + "\n" +
#                      " - Predicted # of Conversions:  " + str(conversions) + "\n" +
#                      " - Predicted Click Through Rate: " + str(CTR) + "%" + "\n" +
#                      " - Predicted Conversion Rate: " + str(CVR) + "%" + "\n" +
#                      " - Expected Conversions: " + str(expected_conversions) + "\n" +
#                      " - Predicted Bidding Price: " + str(biddingprice), 200)

# if __name__ == '__main__':
#         main()