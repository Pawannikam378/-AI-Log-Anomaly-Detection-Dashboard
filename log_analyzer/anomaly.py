import pandas as pd
from sklearn.ensemble import IsolationForest
import logging

logger = logging.getLogger(__name__)

def detect_anomalies(df: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    """
    Fits an Isolation Forest model to detect anomalous log entries.
    Returns the dataframe with added 'anomaly_score' and 'is_anomaly' columns.
    """
    if df.empty:
        return df
        
    logger.info(f"Running anomaly detection with contamination={contamination}...")
    
    feature_cols = [
        'level_encoded', 
        'time_gap_seconds', 
        'error_count_1m', 
        'warning_count_1m',
        'rolling_error_rate',
        'message_length',
        'failed_login_1m'
    ]
    
    missing_cols = [col for col in feature_cols if col not in df.columns]
    if missing_cols:
        logger.error(f"Missing feature columns: {missing_cols}")
        raise ValueError(f"Missing feature columns: {missing_cols}")
        
    X = df[feature_cols].fillna(0)
    
    model = IsolationForest(
        n_estimators=100, 
        contamination=contamination, 
        random_state=42
    )
    
    model.fit(X)
    
    predictions = model.predict(X)
    df['is_anomaly'] = (predictions == -1).astype(int)
    
    # score_samples returns negative anomaly score (lower means more anomalous)
    # Scale/invert so higher score is intuitively more anomalous
    df['anomaly_score'] = -model.score_samples(X)
    
    logger.info(f"Anomaly detection complete. Found {df['is_anomaly'].sum()} anomalies.")
    return df
