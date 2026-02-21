import streamlit as st
import pandas as pd
import logging
from parser import parse_logs
from features import generate_features
from anomaly import detect_anomalies
from visualizer import plot_anomaly_timeline, plot_log_level_distribution
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

st.set_page_config(page_title="AI Log Anomaly Detection", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ AI Log Anomaly Detection Dashboard")
st.markdown("Analyze log files, extract patterns, and identify suspicious events using Unsupervised Machine Learning.")

st.sidebar.header("⚙️ Configuration")
uploaded_file = st.sidebar.file_uploader("Upload Log File (.txt)", type=["txt"])

contamination = st.sidebar.slider(
    "Anomaly Sensitivity", 
    min_value=0.01, max_value=0.20, value=0.05, step=0.01,
    help="Higher values flag more anomalies."
)

@st.cache_data
def process_data(file_content, contamination_val):
    try:
        df = parse_logs(file_content)
        if df.empty:
            return df, "Parsed DataFrame is empty."
        df = generate_features(df)
        df = detect_anomalies(df, contamination=contamination_val)
        return df, None
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        return pd.DataFrame(), str(e)

def main():
    if uploaded_file is not None:
        file_content = uploaded_file.getvalue().decode("utf-8")
        st.sidebar.success(f"Loaded {uploaded_file.name}")
    else:
        st.sidebar.info("Using sample_logs.txt (fallback)")
        sample_path = "sample_logs.txt"
        if os.path.exists(sample_path):
            with open(sample_path, "r") as f:
                file_content = f.read()
        else:
            st.error(f"Could not find fallback file: {sample_path}")
            return
            
    with st.spinner("Analyzing logs..."):
        df, error_msg = process_data(file_content, contamination)
        
    if not df.empty and error_msg is None:
        
        min_time = df['timestamp'].min().to_pydatetime()
        max_time = df['timestamp'].max().to_pydatetime()
        
        st.sidebar.markdown("---")
        st.sidebar.header("📅 Filters")
        
        if min_time < max_time:
            time_range = st.sidebar.slider("Select Time Range", min_value=min_time, max_value=max_time, value=(min_time, max_time))
            mask = (df['timestamp'] >= time_range[0]) & (df['timestamp'] <= time_range[1])
            filtered_df = df.loc[mask]
        else:
            st.sidebar.info("Time range is too narrow to filter.")
            filtered_df = df

        total_logs = len(filtered_df)
        total_anomalies = filtered_df['is_anomaly'].sum()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Total Logs", total_logs)
        with col2: st.metric("Anomalies Detected", total_anomalies, delta_color="inverse", delta=f"{total_anomalies} flagged")
        with col3: st.metric("Critical Errors", len(filtered_df[filtered_df['log_level'] == 'ERROR']))
        with col4: st.metric("Anomaly Rate", f"{(total_anomalies/total_logs*100):.1f}%" if total_logs > 0 else "0%")
            
        st.markdown("---")
        col_chart1, col_chart2 = st.columns([2, 1])
        with col_chart1:
            st.subheader("📈 Anomaly Timeline")
            st.pyplot(plot_anomaly_timeline(filtered_df))
            
        with col_chart2:
            st.subheader("📊 Log Level Distribution")
            st.pyplot(plot_log_level_distribution(filtered_df))
            
        st.markdown("---")
        st.subheader("🚨 Flagged Suspicious Events")
        anomalies_only = filtered_df[filtered_df['is_anomaly'] == 1].copy()
        
        if not anomalies_only.empty:
            display_cols = ['timestamp', 'log_level', 'anomaly_score', 'message', 'rolling_error_rate', 'failed_login_1m']
            # Provide styling with pandas styling API, rendering dataframe with Streamlit.
            styled_df = (
                anomalies_only[display_cols].sort_values(by='anomaly_score', ascending=False)
                .style.apply(lambda x: ['background-color: #3d0000; color: #ffcccc' for _ in x], axis=1)
                .format({'anomaly_score': '{:.2f}', 'rolling_error_rate': '{:.2f}'})
            )
            st.dataframe(styled_df, use_container_width=True)
        else:
            st.success("No anomalous events detected.")
            
        with st.expander("View All Processed Log Data"):
            st.dataframe(filtered_df, use_container_width=True)

    else:
        st.error(f"Failed to process logs. Error: {error_msg}")
        
if __name__ == "__main__":
    main()
