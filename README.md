## Team Name: ctrl+r
## Team Members: Muskan Singh, Srishti Chugh, Nishtha Gupta, Shreeya Aggarwal


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

## **3. Our Approach**

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

## **4. Implementation Details**

### **4.1. Code Structure**
- **`BidRequest.py`**: Defines the `BidRequest` class, which represents a bidding request.
- **`Bidder.py`**: Defines the `Bidder` interface, which the `Bid` class implements.
- **`Bid.py`**: Implements the `Bid` class, which contains the core bidding logic.
- **`main.py`**: The entry point for the application. It loads the data, initializes the `Bid` class, and simulates the bidding process.

### **4.2. Key Methods**
- **`getHistoricalCTR`**: Estimates the CTR for a given bid request based on historical data.
- **`getHistoricalCVR`**: Estimates the CVR for a given bid request based on historical data.
- **`getBidPrice`**: Determines the bid price for a given bid request or returns `-1` if no bid is placed.

---

## **5. Validation and Results**
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
