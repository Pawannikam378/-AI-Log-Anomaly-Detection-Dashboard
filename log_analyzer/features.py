import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def generate_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates engineered features for anomaly detection based on the parsed logs.
    Includes:
    - Time gap between events
    - Log level encoding (INFO=0, WARNING=1, ERROR=2)
    - Error count per minute
    - Rolling error rate
    """
    if df.empty:
        return df
        
    logger.info("Generating features for anomaly detection...")
    df = df.copy()
    
    # Ensure sorted by timestamp
    df = df.sort_values(by='timestamp').reset_index(drop=True)
    
    # Log level encoding
    level_mapping = {'INFO': 0, 'WARNING': 1, 'ERROR': 2}
    df['level_encoded'] = df['log_level'].map(level_mapping).fillna(0)
    
    # Time gap between events (in seconds)
    df['time_gap_seconds'] = df['timestamp'].diff().dt.total_seconds().fillna(0)
    
    # Time-based features
    temp_df = df.set_index('timestamp')
    temp_df['is_error'] = (temp_df['log_level'] == 'ERROR').astype(int)
    temp_df['is_warning'] = (temp_df['log_level'] == 'WARNING').astype(int)
    temp_df['event_count'] = 1
    
    # Count of events in the past 1 minute
    df['error_count_1m'] = temp_df['is_error'].rolling('1min').sum().values
    df['warning_count_1m'] = temp_df['is_warning'].rolling('1min').sum().values
    df['event_count_1m'] = temp_df['event_count'].rolling('1min').sum().values
    
    # Rolling error rate
    df['rolling_error_rate'] = df['error_count_1m'] / (df['event_count_1m'] + 1e-9)
    
    df['message_length'] = df['message'].str.len()
    
    df['is_failed_login'] = df['message'].str.lower().str.contains('failed login').astype(int)
    temp_df['is_failed_login'] = df['is_failed_login'].values
    df['failed_login_1m'] = temp_df['is_failed_login'].rolling('1min').sum().values

    logger.info("Feature engineering complete.")
    return df
