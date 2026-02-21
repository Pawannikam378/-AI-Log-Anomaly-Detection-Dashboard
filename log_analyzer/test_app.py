import sys
import os
import io

print("Testing AI Log Anomaly Detection Project...")

# Add current directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    with open("sample_logs.txt", "r") as f:
        file_content = f.read()
        
    import parser
    df = parser.parse_logs(file_content)
    print(f"Parsed {len(df)} lines.")
    
    import features
    df = features.generate_features(df)
    print(f"Engineered features. Shape: {df.shape}")
    
    import anomaly
    df = anomaly.detect_anomalies(df, contamination=0.1)
    print(f"Detected {df['is_anomaly'].sum()} anomalies.")
    
    import visualizer
    fig1 = visualizer.plot_anomaly_timeline(df)
    fig2 = visualizer.plot_log_level_distribution(df)
    print("Visualizations generated successfully.")

    # Just import app.py to ensure no syntax errors
    import app
    print("app.py imported successfully!")
    
except Exception as e:
    print(f"Error during testing: {e}")
    sys.exit(1)

print("All tests passed successfully!")
