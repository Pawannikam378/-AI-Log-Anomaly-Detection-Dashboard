import matplotlib.pyplot as plt
import pandas as pd
import logging

logger = logging.getLogger(__name__)
plt.style.use('dark_background')

def plot_anomaly_timeline(df: pd.DataFrame) -> plt.Figure:
    """
    Generates a timeline scatter plot of logs, highlighting anomalies.
    """
    if df.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.text(0.5, 0.5, 'No Data Available', ha='center', va='center')
        return fig
        
    fig, ax = plt.subplots(figsize=(12, 5))
    
    normal_df = df[df['is_anomaly'] == 0]
    ax.scatter(normal_df['timestamp'], normal_df['anomaly_score'], 
               color='cyan', alpha=0.6, label='Normal', s=30)
               
    anomaly_df = df[df['is_anomaly'] == 1]
    if not anomaly_df.empty:
        ax.scatter(anomaly_df['timestamp'], anomaly_df['anomaly_score'], 
                   color='red', alpha=0.9, label='Anomaly', s=80, edgecolors='white', marker='X')
                   
    ax.set_title('Log Anomaly Timeline', fontsize=16, pad=15)
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Anomaly Score', fontsize=12)
    ax.grid(True, alpha=0.2, linestyle='--')
    ax.legend()
    
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig

def plot_log_level_distribution(df: pd.DataFrame) -> plt.Figure:
    """
    Generates a bar chart showing log level distribution.
    """
    if df.empty or 'log_level' not in df.columns:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, 'No Data Available', ha='center', va='center')
        return fig
        
    fig, ax = plt.subplots(figsize=(8, 5))
    level_counts = df['log_level'].value_counts()
    
    colors = []
    for level in level_counts.index:
        if level == 'ERROR':
            colors.append('red')
        elif level == 'WARNING':
            colors.append('orange')
        else:
            colors.append('lightgreen')
            
    bars = ax.bar(level_counts.index, level_counts.values, color=colors, alpha=0.8)
    
    ax.set_title('Log Level Distribution', fontsize=16, pad=15)
    ax.set_xlabel('Log Level', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.grid(True, axis='y', alpha=0.2, linestyle='--')
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), 
                    textcoords="offset points",
                    ha='center', va='bottom')
                    
    fig.tight_layout()
    return fig
