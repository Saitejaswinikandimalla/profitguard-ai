# 🛡️ ProfitGuard AI
**Intelligent Revenue Leakage Detection & Business Decision-Support Platform**  
*DATATHON 2026 — Track 4: Business (The Money Leak)*

---

## 📌 Executive Summary
**ProfitGuard AI** bridges disconnected transactional, catalog, and customer data to audit unit-level transaction economics, detect hidden revenue leakage, and segment customer purchasing behaviors using from-scratch Machine Learning.

In an audit of **18,000 real-world competition records**:
* **13,962** completed transactions evaluated.
* **₹73.02 Lakhs** ($7.30M) completed topline revenue.
* **5,315 orders (38.07%)** sold at negative estimated margins.
* **₹12.14 Lakhs** ($1.21M) in cumulative financial leakage (16.6% bottom-line loss).

---

## 🚀 Key Modules
1. **Executive Intelligence Dashboard**: Real-time business KPIs, category revenue vs margin breakdown, and priority leakage queue.
2. **Deterministic Revenue Leakage Auditor**: Traceable unit economics on every transaction:
   $$\text{Estimated Margin} = Q \times [P(1 - D) - C]$$
   Automatically classifies root causes into **Catalog Mispricing ($P < C$)** vs. **Excessive Promo Leakage**.
3. **Customer Intelligence (ML)**: Unsupervised RFM (Recency, Frequency, Monetary) behavioral segmentation implemented **from scratch using pure NumPy K-Means** (Sample Silhouette Score: `0.384`, $K=4$).

---

## 🖼️ Prototype UI Preview
![ProfitGuard Minimal Dashboard](screenshots/screen2_minimal_light.png)

---

## ⚙️ Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/tejaswinikandimalla09/profitguard-ai.git
cd profitguard-ai
```

### 2. Launch Local Server (Zero External Dependencies)
```bash
py server.py
```
Open your browser at `http://localhost:8501`.

### 3. Launch Streamlit Application (Optional)
```bash
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

---

## 📁 Repository Structure
```
profitguard-ai/
├── app.py                      # Interactive Streamlit application
├── server.py                   # Lightweight standalone zero-dependency dashboard
├── ml.py                       # Pure NumPy K-Means and RFM feature extractor
├── requirements.txt            # Python dependencies
├── data/                       # Datathon Track 4 CSV datasets
│   ├── transactions.csv
│   ├── products.csv
│   ├── customers.csv
│   ├── inventory.csv
│   └── campaigns.csv
└── screenshots/                # Verified application screenshots
```

---

## 🎓 Competition & Team Details
* **Event**: DATATHON 2026
* **Host**: Data Science Club, VIT-AP University & IIEC
* **Track**: Track 4 — Business (The Money Leak)
* **Team**: Sai Tejaswini Kandimalla & Collaborator
