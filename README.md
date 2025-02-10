## Team Name: ctrl+r
## Team Members: Muskan Singh, Srishti Chugh, Nishtha Gupta, Shreeya Aggarwal


# Approach

This document describes the approach used in our DSP (Demand-Side Platform) bidding algorithm to optimize the number of clicks and conversions while staying within a fixed budget.

---

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

## 4. How to Run the Project

### 4.1. Prerequisites

Ensure you have the following installed:
- Python 3.x
- Pandas
- NumPy
- XGBoost
- Scikit-learn

Install dependencies using:
```bash
pip install pandas numpy xgboost scikit-learn
```

### 4.2. Running the Project

1. **Prepare the dataset**: Place bid logs, impression logs, click logs, and conversion logs in the `data` directory.
2. **Train CTR & CVR models**:
   ```python
   from xgboost import XGBClassifier
   model = XGBClassifier()
   model.fit(X_train, y_train)
   model.save_model("ctr_model.json")  # Save trained model
   ```
3. **Execute the bidding system**:
   ```bash
   python main.py
   ```
   This loads the dataset, processes bids, and outputs the bidding decisions.

### 4.3. Sample Output

```text
Bid placed: 7.85 for Advertiser 1458
Bid placed: 12.34 for Advertiser 3358
No bid placed for Advertiser 3386 (budget exceeded)
```

---

## 5. Summary

This project demonstrates an ML-driven **real-time bidding system** with CTR and CVR prediction, leveraging **log loss evaluation** for model robustness. It optimizes ad spending dynamically, ensuring efficiency and profitability in programmatic advertising.

