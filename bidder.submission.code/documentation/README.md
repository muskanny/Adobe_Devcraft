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

