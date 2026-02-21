import pandas as pd
import re
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_logs(file_content: str) -> pd.DataFrame:
    """
    Parses raw log content and returns a Pandas DataFrame containing
    timestamp, log_level, and message.
    """
    logger.info("Parsing log contents...")
    
    # Regex pattern: YYYY-MM-DD HH:MM:SS LEVEL Message
    pattern = re.compile(r"^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+([A-Z]+)\s+(.*)$")
    
    parsed_data = []
    
    for line in file_content.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
            
        match = pattern.match(line)
        if match:
            timestamp_str, level, message = match.groups()
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                parsed_data.append({
                    'timestamp': timestamp,
                    'log_level': level,
                    'message': message,
                    'raw_log': line
                })
            except ValueError as e:
                logger.warning(f"Failed to parse timestamp: {line} - Error: {e}")
        else:
            logger.warning(f"Line did not match expected format: {line}")
            
    df = pd.DataFrame(parsed_data)
    if df.empty:
        logger.warning("No valid log lines were parsed.")
        return pd.DataFrame(columns=['timestamp', 'log_level', 'message', 'raw_log'])
        
    logger.info(f"Successfully parsed {len(df)} log lines.")
    return df
