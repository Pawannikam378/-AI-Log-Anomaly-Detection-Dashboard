# 🛡 AI Log Anomaly Detection Dashboard

A cybersecurity-focused log monitoring system built using **Python, Streamlit, and Unsupervised Machine Learning**.

This project parses system logs, extracts structured features, detects anomalous behavior using Isolation Forest, and visualizes suspicious activities through an interactive dashboard.

Designed to simulate a lightweight Security Information and Event Management (SIEM) system.

---

## 🚀 Live Demo

🔗 Demo Link: _(Add after deployment)_  

Run locally:

```bash
streamlit run app.py
```

---

## 🎯 Project Objective

Modern systems generate massive logs. Hidden inside these logs may be:

- Brute-force login attempts  
- Abnormal error spikes  
- Suspicious activity patterns  
- System misuse  

This application detects unusual behavior automatically using unsupervised learning.

---

## ✨ Features

### 📂 Log Input
- Upload `.txt` log files
- Built-in sample log generator
- Structured log parsing

Example Log Format:
```
2026-02-21 10:23:11 INFO User login success
2026-02-21 10:25:32 ERROR Failed login attempt
2026-02-21 10:26:02 WARNING Multiple failed attempts
```

---

### 🔎 Log Parsing
Extracts:
- Timestamp
- Log Level (INFO, WARNING, ERROR)
- Message
- Datetime conversion

---

### ⚙ Feature Engineering

Generated features include:

- Error count per minute
- Failed login frequency
- Time gap between events
- Log level encoding
- Rolling error rate

---

### 🤖 Anomaly Detection

Uses **Isolation Forest** (Unsupervised ML):

- No labeled data required
- Detects outliers automatically
- Adjustable contamination parameter
- Outputs anomaly score
- Flags suspicious events

---

### 📊 Interactive Dashboard

Displays:

- Total logs processed
- Total anomalies detected
- Log level distribution chart
- Timeline of activity
- Highlighted anomaly points
- Table of flagged suspicious logs

Anomalies are visually marked in red.

---

## 🧠 How Isolation Forest Works

Isolation Forest isolates anomalies instead of profiling normal behavior.

Core idea:
- Anomalies are easier to isolate
- Fewer splits required in decision trees
- Shorter average path length → higher anomaly score

Decision Rule:
```
Anomaly if predicted label == -1
```

---

## 🏗 Project Structure

```
log_analyzer/
│── app.py
│── parser.py
│── features.py
│── anomaly.py
│── visualizer.py
│── sample_logs.txt
│── requirements.txt
│── README.md
```

---

## 🛠 Tech Stack

| Layer | Technology |
|--------|------------|
| UI | Streamlit |
| Data Processing | Pandas |
| Numerical Ops | NumPy |
| ML Model | Isolation Forest (scikit-learn) |
| Visualization | Matplotlib |

---

## ⚙ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/log-analyzer.git
cd log-analyzer
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Application

```bash
streamlit run app.py
```

---

## 📊 Example Output

- Total Logs: 1,200
- Anomalies Detected: 37
- Suspicious Activity: Failed login spike
- Error Surge Identified at: 10:26:02

---

## 📉 Risk & Security Insight

This tool can detect:

- Brute-force attempts
- Sudden error bursts
- Unusual login timing
- Abnormal behavior patterns

---

## 🚀 Future Improvements

- Real-time log streaming
- Network packet integration
- Auto-generated synthetic attack simulation
- Multi-user authentication
- Email alert system
- Deploy on cloud server
- Integrate with SIEM tools

---

## ⚠ Disclaimer

This project is for educational and demonstration purposes only.  
It is not a production-grade security monitoring system.

---

## 📜 License

MIT License

---

## 👤 Author

Your Name: Pawan Nikam  
Final Year Engineering Student  
Focused on Embedded System, Machine Learning & Systems Engineering
