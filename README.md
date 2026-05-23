# 🏦 SMART Banking ML Suite
### AI-Powered Fraud Detection · Loan Approval · Credit Risk Scoring

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![XGBoost](https://img.shields.io/badge/XGBoost-Latest-orange?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=flat-square&logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-yellow?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

> ## 🚧 PROJECT STATUS — Work In Progress
>
> ### 📓 Currently Available for Testing:
> The **Jupyter Notebooks** for Fraud Detection and Loan Approval modules are fully functional and available for testing right now.
>
> ```
> ✅ fraud_detection.ipynb   → Fully working
> ✅ loan_approval.ipynb     → Fully working  
> ⏳ credit_risk.ipynb       → Coming soon
> ```
>
> ### 🖥️ UI Dashboard — Under Active Development
> We are currently building the **frontend  Web Dashboard** for all three modules. The UI is not yet fully production-ready.
>
> ```
> ✅ Fraud Detection page     → Built
> ✅ Loan Approval page       → Built
> ⏳ Credit Risk page         → Coming soon
> ⏳ Performance Analytics    → Coming soon
> ⏳ Full PDF reporting       → In progress
> ```
>
> > 💡 **For now:** Use the Jupyter Notebooks in the `Notebook/` folder to test all ML models directly. Full UI will be available in the next release.

---

> ## ⚠️ IMPORTANT NOTE — Currency & Data Disclaimer
>
> ### 🇺🇸 Current Version — USD Based
> The **Loan Approval** and **Fraud Detection** models in this version are trained on **US-based financial datasets** where all monetary values are in **USD ($)**.
>
> Feeding **INR (₹) values directly** into the current model **will affect prediction accuracy** due to the massive scale difference:
> ```
> Example:
> $50,000 income (USD) ≈ ₹41,50,000 income (INR)
>
> If you enter ₹50,000 as income → model treats it as $50,000
> → Completely different financial profile → incorrect prediction ⚠️
> ```
>
> ### 📊 How It Affects Each Module:
> | Module | Trained On | INR Input Impact |
> |--------|------------|-----------------|
> | Fraud Detection | PaySim (African mobile banking) | Transaction amounts in different scale |
> | Loan Approval | UCI Dataset (USD based) | Income & loan amounts misinterpreted |
> | Credit Risk | German Credit Data (EUR based) | Risk scoring may be inaccurate |
>
> ### 🇮🇳 Version 2.0 — INR Support (Coming Soon)
> We are actively working on an **India-specific version** of this ML Suite that will:
> - [ ] Be trained on **Indian banking datasets** in **INR (₹)**
> - [ ] Use **RBI-compliant** credit scoring standards
> - [ ] Incorporate **Indian CIBIL score** ranges (300–900)
> - [ ] Support **UPI, NEFT, RTGS, IMPS** transaction types
> - [ ] Use **Indian income brackets** for loan eligibility
>
> > 💡 **For now:** If testing with Indian values, convert INR to USD before entering
> > (Divide INR amount by 83 to get approximate USD equivalent)

---

## 📌 Overview

The **SMART Banking ML Suite** is an industrial-level Machine Learning system built for the banking and financial sector. It automates three critical banking operations using advanced ML algorithms, replacing slow manual processes with intelligent, real-time predictions.

| Module | Algorithm | Dataset | Key Metric |
|--------|-----------|---------|------------|
| 🚨 Fraud Detection | XGBoost + Pipeline | PaySim (6.3M rows) | **99.57% Recall** |
| ✅ Loan Approval | Random Forest | UCI Loan (50K rows) | **98.75% Accuracy** |
| 📊 Credit Risk | XGBoost + CatBoost | German Credit (1K) | Coming Soon |

> **Key Outcome:** Reduced banking decision time from 2–3 hours to under **5 seconds** — a 99%+ improvement.

---

## 🗂️ Project Structure

```
SMART_Banking_System/
│
├── 📁 data/                          # Raw datasets
│   ├── Synthetic_Financial_datasets_log.csv   # PaySim fraud dataset
│   ├── loan_data.csv                          # UCI loan dataset
│   └── german_credit.csv                      # Credit risk dataset
│
├── 📁 models/                        # Trained ML models
│   ├── fraud_model.pkl               # Fraud detection pipeline
│   ├── loan_model.pkl                # Loan approval model
│   └── credit_model.pkl             # Credit risk model (coming soon)
│
├── 📁 Notebook/                      # Jupyter notebooks
│   ├── fraud_detection.ipynb         # Module 1 — complete workflow
│   ├── loan_approval.ipynb           # Module 2 — complete workflow
│   └── credit_risk.ipynb            # Module 3 — coming soon
│
├── 📁 app/                           # Streamlit dashboard
│   └── app.py                        # Main dashboard application
│
├── .gitignore
└── README.md
```

---

## 🚀 Features

### 🚨 Module 1 — Fraud Detection
- Trained on **6.3 million** PaySim banking transactions
- Covers CASH-IN, CASH-OUT, TRANSFER, PAYMENT, DEBIT
- **SMOTE + RandomUnderSampler** for imbalanced data handling
- **Domain-driven feature engineering** (balance drop, account drain detection)
- Full **imblearn Pipeline** — zero data leakage
- Bulk CSV upload + **PDF report generation**
- Caught **1,632 out of 1,639** fraud cases in testing

### ✅ Module 2 — Loan Approval
- Predicts loan eligibility from customer financial profile
- Features: Income, Credit Score, Loan Amount, Employment History
- Auto-calculates **Loan-to-Income Ratio**
- Bulk CSV processing with PDF report export
- **98.75% accuracy** on test set

### 📊 Module 3 — Credit Risk Scoring *(Coming Soon)*
- Customer risk categorization (Low / Medium / High)
- Probability-based credit scoring
- Feature importance analysis
- Target: ROC-AUC > 90%

### 🖥️ Interactive Dashboard
- Unified Streamlit dashboard for all modules
- Single prediction + bulk CSV upload modes
- Downloadable PDF reports
- No ML expertise required to operate

---

## ⚙️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.8+ |
| ML Framework | Scikit-learn, XGBoost, CatBoost |
| Imbalanced Data | Imbalanced-learn (SMOTE) |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Dashboard | Streamlit |
| PDF Export | ReportLab |
| Model Saving | Pickle |
| Version Control | Git & GitHub |

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/SMART_Banking_System.git
cd SMART_Banking_System
```

### 2. Install dependencies
```bash
pip install pandas numpy scikit-learn xgboost imbalanced-learn
pip install streamlit reportlab matplotlib seaborn
```

### 3. Run the dashboard
```bash
cd app
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## 📊 Model Performance

### Fraud Detection
```
              precision    recall  f1-score   support

Not Fraud         1.00      1.00      1.00   1,270,777
Fraud             0.26      1.00      0.41       1,639

accuracy                              1.00   1,272,416

Confusion Matrix:
True Positive  → 1,632  (Fraud correctly detected)
False Negative →     7  (Fraud missed)
False Positive → 4,660  (False alarms)
True Negative  → 1,266,117 (Normal correctly identified)
```

### Loan Approval
```
Model          → Random Forest
Accuracy       → 98.75%
```

---

## 🔄 ML Pipeline Architecture

```
Raw Data Input
      ↓
ColumnTransformer
      ├── OneHotEncoder   (categorical: transaction type)
      └── StandardScaler  (numerical: amount, balances)
      ↓
RandomUnderSampler  (reduces majority class)
      ↓
SMOTE               (synthesizes minority class samples)
      ↓
XGBClassifier       (gradient boosted trees)
      ↓
Prediction + PDF Report
```

---

## 📁 Dataset Information

### Fraud Detection — PaySim Dataset
- **Source:** Kaggle (PaySim Synthetic Financial Dataset)
- **Size:** 6.3 Million transactions
- **Period:** 30 days simulated mobile banking activity
- **Fraud Rate:** 0.13% (highly imbalanced)
- **Transaction Types:** CASH-IN, CASH-OUT, TRANSFER, PAYMENT, DEBIT

### Loan Approval — UCI Loan Dataset
- **Source:** UCI Machine Learning Repository
- **Size:** 50,000 records
- **Features:** income, credit_score, loan_amount, years_employed, loan_income_ratio

### Credit Risk — German Credit Dataset
- **Source:** UCI Machine Learning Repository
- **Size:** 1,000 records
- **Target:** Good / Bad credit risk

---

## 📋 CSV Upload Format

### Fraud Detection CSV:
```
step,type,amount,oldbalanceOrg,newbalanceOrig,oldbalanceDest,newbalanceDest
1,TRANSFER,181.0,181.0,0.0,0.0,0.0
1,PAYMENT,9839.64,170136.0,160296.36,0.0,0.0
```

### Loan Approval CSV:
```
income,credit_score,loan_amount,years_employed
500000,720,200000,3
250000,580,300000,1
```

---

## 🎯 Key ML Concepts Used

| Concept | Applied Where |
|---------|--------------|
| Classification | All 3 modules |
| Anomaly Detection | Fraud Detection |
| SMOTE | Fraud Detection |
| Feature Engineering | Fraud Detection (4 derived features) |
| Log Transformation | Amount column (fraud) |
| Pipeline | Fraud Detection |
| ColumnTransformer | Fraud Detection |
| OneHotEncoder | Transaction type column |
| StandardScaler | All numerical features |
| Stratified Split | All modules |

---

## 💡 Feature Engineering (Fraud Detection)

Four domain-driven features created from banking knowledge:

```python
# 1. Did sender's balance drain completely?
balanceDropOrig = oldbalanceOrg - newbalanceOrig

# 2. Did receiver actually gain money?
balanceGainDest = newbalanceDest - oldbalanceDest

# 3. Sender account went to zero (common fraud pattern)
origBalanceZero = (newbalanceOrig == 0).astype(int)

# 4. High risk transaction types (fraud only in these)
isHighRiskType  = type.isin(['CASH_OUT', 'TRANSFER']).astype(int)
```

---

## 🏭 Industrial Applications

This system can be deployed in:
- 🏦 Banking & Financial Institutions
- 💳 FinTech Companies (Razorpay, CRED, PhonePe)
- 🛡️ Insurance Companies
- 📱 Online Payment Systems (PayPal, Visa, Mastercard)

---

## 🔮 Future Scope

- [ ] Real-time transaction monitoring (Kafka + Spark)
- [ ] Cloud deployment (AWS / Azure / GCP)
- [ ] REST API endpoints (Flask)
- [ ] AI chatbot for customer advisory
- [ ] Mobile application
- [ ] Deep Learning implementation
- [ ] Email alert system for fraud detection

---

## 👨‍💻 Author

**Vedant**
- 🎓 Campus Placement Project — Banking ML Suite
- 📧 vedant18vasava@gmail.com
- 🔗 [GitHub][https://github.com/vedantvsv]
- 🔗 [LinkedIn][https://www.linkedin.com/in/vedant-vasava-089130318/]

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
    <b>Built with ❤️ using Python, XGBoost, and Streamlit</b><br>
    <i>AI-Powered Banking Intelligence — From Data to Decision in Under 5 Seconds</i>
</div>
