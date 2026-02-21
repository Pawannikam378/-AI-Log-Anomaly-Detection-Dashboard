# AI Log Anomaly Detection Dashboard

A streamlined log analysis tool to catch potential incidents by examining features like log level severity, event frequency, and time differences using Scikit-Learn's Isolation Forest algorithm.

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Features

- Parses standard logs into structured details.
- Extracts meaningful indicators like `rolling_error_rate` or `failed_login_1m`.
- Employs Unsupervised Machine Learning (`IsolationForest`) to identify anomalous patterns automatically without needing labeled attacks.
- Provides interactive visual feedback using Streamlit and Matplotlib.
