# Approach

This document describes the approach used in our DSP (Demand-Side Platform) bidding algorithm to optimize the number of clicks and conversions while staying within a fixed budget.

---

## **1. Problem Statement**
The goal of the advertising campaign is to maximize the score, defined as:
Score = Total Clicks + N * Total Conversions

Copy
where:
- `N` is a weight that reflects the relative importance of conversions vs. clicks for each advertiser.
- The bidding process is subject to a fixed budget constraint.

The task is to design a bidding strategy that:
- Decides whether to bid on a given impression.
- Determines the optimal bid price for each impression.

---

## **2. Key Challenges**
- **Real-Time Decision Making**: Bidding decisions must be made in real-time without knowledge of future impressions.
- **Budget Constraints**: The total spending must not exceed the fixed budget.
- **Second-Price Auction**: The winning bidder pays the second-highest bid price, so overbidding is not optimal.

---
## **3.1 Our ML Approach**
# Ad Bidding System with ML-Based Optimization

## 1. Problem Statement

In the digital advertising ecosystem, advertisers compete for ad placements through a real-time bidding (RTB) system. The challenge lies in efficiently allocating a fixed budget across multiple bidding opportunities to maximize the return on investment (ROI). The effectiveness of bidding is determined by two key probabilities:

- **Click-Through Rate (CTR)**: The likelihood that a user will click on an ad.
- **Conversion Rate (CVR)**: The probability that a click will result in a desired action (e.g., purchase, sign-up).

A robust bidding strategy requires:
- Predicting CTR and CVR accurately.
- Optimizing bid prices to maximize revenue while staying within budget constraints.
- Ensuring fairness and efficiency in resource allocation among multiple advertisers.

This project implements a **machine learning-based RTB system** that utilizes historical data to predict CTR and CVR, applying these predictions to optimize bid prices dynamically.

---

## 2. Solution Overview

The system is implemented using **XGBoost classifiers** for CTR and CVR predictions. The bidding strategy involves:

1. **Preprocessing Bid Requests**: Extracting relevant features and encoding categorical variables.
2. **Predicting CTR and CVR**: Using trained machine learning models to estimate click and conversion probabilities.
3. **Bid Price Calculation**: Determining the optimal bid based on an expected value formula:
   
   \[ Expected Value = CTR \times (1 + N \times CVR) \]
   
   where \( N \) is an advertiser-specific multiplier.
4. **Budget Constraint Handling**: Ensuring the bid does not exceed available budget and is at least the floor price.
5. **Historical Data Utilization**: Leveraging past bid outcomes to improve decision-making.

A **non-ML approach** is also provided, using historical CTR and CVR values instead of machine learning predictions.

---

## 3. Implementation Details

### 3.1. Code Structure

- `Bid.py`: Implements the **Bid** class, handling bid computation using ML models.
- `Bidder.py`: Defines the base class for bid computation.
- `BidRequest.py`: Represents a bid request containing details about the ad slot and advertiser.
- `main.py`: Loads and processes historical data, simulates bidding, and evaluates performance.

### 3.2. Log Loss Calculation for CTR & CVR

To evaluate model robustness, **log loss** is used for CTR and CVR predictions:

\[ Log Loss = - \frac{1}{N} \sum \left[ y \log(p) + (1 - y) \log(1 - p) \right] \]

where:
- \( y \) is the actual outcome (click/conversion: 0 or 1).
- \( p \) is the predicted probability.

This metric ensures the models produce well-calibrated probability scores, essential for effective bid optimization.

---

# Ad Prediction App

## Overview
This Streamlit application predicts the number of impressions, clicks, conversions, and bidding prices for online advertising campaigns using pre-trained machine learning models.

## Directory Structure
```
project_directory/
│-- python/
│   │-- app.py  # Main Streamlit app
│-- models/
│   │-- ctr_model.pkl  # Click-through rate model
│   │-- cvr_model.pkl  # Conversion rate model
│   │-- bid_price_model.pkl  # Bidding price model
│-- requirements.txt  # Required dependencies
```

## Installation and Setup
### 1. Clone the Repository
```sh
git clone <repository_url>
cd project_directory/python
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
Ensure you have Python 3.8+ installed. Then, install the required Python packages:
```sh
pip install -r requirements.txt
```

### 4. Ensure Models are Available
Place the model files (`ctr_model.pkl`, `cvr_model.pkl`, `bid_price_model.pkl`) inside the `models/` directory. If they are missing, ensure you have them before running the application.

### 5. Run the Streamlit App
Execute the following command from within the `python/` directory:
```sh
streamlit run app.py
```

### 6. Access the App
Once the server starts, Streamlit will display a local URL. Open it in your browser:
```
http://localhost:8501/
```

## Notes
- Make sure all dependencies in `requirements.txt` are installed.
- If using different model paths, update the `joblib.load()` paths in `app.py` accordingly.
- If encountering errors, verify that the model files exist and match the required format.

## Troubleshooting
### Error: Module Not Found
If you get a `ModuleNotFoundError`, install missing dependencies:
```sh
pip install -r requirements.txt
```

### Error: Model Not Found
Ensure the `.pkl` files are correctly placed in the `models/` directory.

### Error: Streamlit Port in Use
If Streamlit fails to start due to the port being in use, try running:
```sh
streamlit run app.py --server.port 8502
```


## **3.2 Our NON ML Approach**

### **3.1. Data Preprocessing**
- **Data Loading**: We load the bid, impression, click, and conversion logs from the provided dataset.
- **Feature Engineering**:
  - Calculate **Click-Through Rate (CTR)** and **Conversion Rate (CVR)** for each combination of `AdvertiserID`, `AdslotID`, and `Region`.
  - Handle missing values by using default values for `CTR` (0.01) and `CVR` (0.001).
- **Historical Data**: We preprocess the historical data to estimate `CTR` and `CVR` for incoming bid requests.

### **3.2. Bidding Strategy**
Our bidding strategy is based on the following steps:

1. **Estimate Expected Value**:
   - For each bid request, we estimate the expected value of the impression using:
     ```
     Expected Value = CTR * (1 + N * CVR)
     ```
     where:
     - `CTR` is the Click-Through Rate.
     - `CVR` is the Conversion Rate.
     - `N` is the advertiser-specific weight for conversions.

2. **Dynamic Budget Allocation**:
   - We allocate the budget dynamically across advertisers based on their expected value.
   - Advertisers with higher expected values receive a larger share of the budget.

3. **Bid Price Calculation**:
   - The bid price is calculated as:
     ```
     Bid Price = Expected Value * Scaling Factor
     ```
     where the scaling factor ensures the bid price is reasonable and within the remaining budget.
   - We ensure the bid price is at least equal to the floor price of the ad slot.

4. **Second-Price Auction Logic**:
   - Since the auction is a second-price auction, we bid slightly above the floor price to minimize costs while still winning the auction.

5. **Edge Cases**:
   - If no historical data is available for a specific combination of features, we use default values for `CTR` and `CVR`.
   - If the remaining budget is insufficient, we do not place a bid.

### **3.3. Performance Metrics**
We evaluate the performance of our bidding strategy using the following metrics:
- **Total Clicks**: The total number of clicks generated.
- **Total Conversions**: The total number of conversions generated.
- **Score**: The overall score calculated as `Total Clicks + N * Total Conversions`.
- **Budget Utilization**: The percentage of the budget spent.

---

## **. Validation and Results**
We validated our bidding strategy using the provided dataset. The results are as follows:

| Advertiser ID | Score  | Budget Spent |
|---------------|--------|--------------|
| 1458          | 2451.0 | 4,410,448,896 |
| 3358          | 1744.0 | 876,840,448  |
| 3386          | 2079.0 | 4,227,579,392 |
| 3427          | 1917.0 | 3,344,589,056 |
| 3476          | 1051.0 | 1,684,169,216 |

### **Key Insights**:
- **Advertiser 1458** has the highest score but also the highest budget spent, indicating inefficiency.
- **Advertiser 3358** has a moderate score with relatively low budget spent, indicating efficient budget utilization.
- **Advertiser 3476** has the lowest score, suggesting that the campaign needs optimization to improve conversions.

---

## **6. Future Improvements**
- **Machine Learning Models**: Use machine learning models to predict `CTR` and `CVR` more accurately.
- **Dynamic Scaling**: Adjust the scaling factor dynamically based on the remaining budget and expected value.
- **Advertiser-Specific Strategies**: Tailor the bidding strategy for each advertiser based on their goals (e.g., clicks vs. conversions).

---

## **7. Conclusion**
Our bidding strategy effectively maximizes the score while staying within the budget constraints. By dynamically allocating the budget and using historical data to estimate the expected value of impressions, we achieve a balance between clicks and conversions. Further improvements can be made by incorporating machine learning models and advertiser-specific strategies.
