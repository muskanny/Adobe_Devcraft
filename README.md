## Team Name: ctrl+r
## Team Members: Muskan Singh, Srishti Chugh, Nishtha Gupta, Shreeya Aggarwal


# Approach

This document describes the approach used in our DSP (Demand-Side Platform) bidding algorithm to optimize the number of clicks and conversions while staying within a fixed budget.

---

# Ad Bidding System with ML-Based Optimization

##  Problem Statement

In the digital advertising ecosystem, advertisers compete for ad placements through a real-time bidding (RTB) system. The challenge lies in efficiently allocating a fixed budget across multiple bidding opportunities to maximize the return on investment (ROI). The effectiveness of bidding is determined by two key probabilities:

- **Click-Through Rate (CTR)**: The likelihood that a user will click on an ad.
- **Conversion Rate (CVR)**: The probability that a click will result in a desired action (e.g., purchase, sign-up).

A robust bidding strategy requires:
- Predicting CTR and CVR accurately.
- Optimizing bid prices to maximize revenue while staying within budget constraints.
- Ensuring fairness and efficiency in resource allocation among multiple advertisers.

This project implements a **machine learning-based RTB system** that utilizes historical data to predict CTR and CVR, applying these predictions to optimize bid prices dynamically.

---

##  Solution Overview

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


# Ad Prediction App-- HOW TO RUN THE APP

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

###  Sample Output

```text
Bid placed: 7.85 for Advertiser 1458
Bid placed: 12.34 for Advertiser 3358
No bid placed for Advertiser 3386 (budget exceeded)
```

---
# Validation Results

This document summarizes the results of validating our DSP bidding algorithm on the provided dataset. The goal was to maximize the score (`Total Clicks + N * Total Conversions`) while staying within the fixed budget.

---
![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)
## **1. Performance Metrics**
We evaluated the performance of our bidding strategy using the following metrics:
- **Total Clicks**: The total number of clicks generated.
- **Total Conversions**: The total number of conversions generated.
- **Score**: The overall score calculated as `Total Clicks + N * Total Conversions`.
- **Budget Spent**: The total amount of budget spent by each advertiser.

---

## **2. Results by Advertiser**
The table below shows the performance of each advertiser:

| Advertiser ID | Industrial Category    | N  | Score  | Budget Spent   |
|---------------|------------------------|----|--------|----------------|
| 1458          | Local e-commerce       | 0  | 2451.0 | 4,410,448,896  |
| 3358          | Software               | 2  | 1744.0 | 876,840,448    |
| 3386          | Global e-commerce      | 0  | 2079.0 | 4,227,579,392  |
| 3427          | Oil                    | 0  | 1917.0 | 3,344,589,056  |
| 3476          | Tire                   | 10 | 1051.0 | 1,684,169,216  |

---

## **3. Key Insights**

### **3.1. Advertiser 1458 (Local e-commerce)**
- **Score**: 2451.0 (highest among all advertisers).
- **Budget Spent**: 4,410,448,896 (highest among all advertisers).
- **Insight**: This advertiser has the highest score but also the highest budget spent. Since `N = 0`, the score is entirely based on clicks. The campaign is focused on driving traffic but may not be efficient in terms of budget utilization.

### **3.2. Advertiser 3358 (Software)**
- **Score**: 1744.0.
- **Budget Spent**: 876,840,448.
- **Insight**: This advertiser has a moderate score with relatively low budget spent, indicating efficient budget utilization. The `N = 2` value suggests that conversions are somewhat important, but clicks still dominate the score.

### **3.3. Advertiser 3386 (Global e-commerce)**
- **Score**: 2079.0.
- **Budget Spent**: 4,227,579,392.
- **Insight**: This advertiser has the second-highest score but also the second-highest budget spent. Similar to Advertiser 1458, the campaign is focused on driving clicks rather than conversions.

### **3.4. Advertiser 3427 (Oil)**
- **Score**: 1917.0.
- **Budget Spent**: 3,344,589,056.
- **Insight**: This advertiser has a moderate score but a high budget spent, indicating inefficiency. The campaign is focused on clicks, similar to Advertisers 1458 and 3386.

### **3.5. Advertiser 3476 (Tire)**
- **Score**: 1051.0 (lowest among all advertisers).
- **Budget Spent**: 1,684,169,216.
- **Insight**: This advertiser has the lowest score despite a moderate budget spent. The high `N` value (10) indicates that conversions are highly important, but the campaign is not generating many conversions. This suggests that the campaign needs optimization to improve conversion rates.

---

## **4. Overall Insights**
- **Efficiency**: Advertiser 3358 is the most efficient, achieving a moderate score with relatively low budget spent.
- **Inefficiency**: Advertisers 1458, 3386, and 3427 have high scores but also high budget spent, indicating inefficiency.
- **Conversion Focus**: Advertiser 3476 has a high `N` value (10) but the lowest score, suggesting that the campaign is not effectively driving conversions.

---

## **5. Recommendations**
1. **Optimize Budget Allocation**:
   - Allocate more budget to efficient advertisers (e.g., Advertiser 3358) and less to inefficient ones (e.g., Advertisers 1458 and 3386).
2. **Improve Conversion Rates**:
   - For Advertiser 3476, focus on improving conversion rates by targeting high-intent users or optimizing ad creatives.
3. **Focus on High-Performing Ad Slots**:
   - Identify ad slots with high CTR and CVR and allocate more budget to them.
4. **Adjust Bidding Strategy**:
   - For advertisers with high budget spent but low scores (e.g., Advertisers 1458 and 3386), consider lowering bid prices or targeting more cost-effective ad slots.

---

## **6. Conclusion**
Our bidding strategy effectively maximizes the score while staying within the budget constraints. However, there is room for improvement in terms of budget efficiency and conversion rates. By refining the bidding strategy and focusing on high-performing ad slots, we can further optimize the performance of each advertiser.
## 7. Summary

This project demonstrates an ML-driven **real-time bidding system** with CTR and CVR prediction, leveraging **log loss evaluation** for model robustness. It optimizes ad spending dynamically, ensuring efficiency and profitability in programmatic advertising.

