# 💸 Smart Budgeting and Expense Tracker

An interactive financial dashboard built in **Streamlit** for personal budgeting, expense tracking, savings goals, and macroeconomic insights. Designed for ease-of-use, visualization, and practical utility.

---

## 🚀 Features

### 🔹 Transaction Management
- Add, view, edit, or delete income and expenses
- Upload transactions from CSV
- Download full transaction history as CSV

### 🔹 Visual Dashboards
- Pie chart of expenses by category
- Income vs. Expenses over time
- Net savings and monthly budget compliance

### 🔹 Savings & Budget Tools
- Set and track savings goals
- Monitor monthly spending vs. budget

### 🔹 Market Insights (FMP + FRED API)
- Stock quotes for AAPL, MSFT, WMT
- U.S. Inflation Rate (CPI)
- Federal Funds Rate
- Unemployment Rate
- Real U.S. GDP (chained 2012 dollars)

---

## ⚙️ How to Run Locally

### 📦 1. Clone this repository:
```bash
git clone https://github.com/yourusername/smart-budget-tracker.git
cd smart-budget-tracker
```

### 🧪 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### ▶️ 3. Run the app:
```bash
streamlit run app.py
```


---

## 🔐 API Keys Required
- **FMP (Financial Modeling Prep)**: [Get one here](https://financialmodelingprep.com/developer/docs)
- **FRED (Federal Reserve Economic Data)**: [Register here](https://fred.stlouisfed.org/docs/api/fred/)

Place them in `app.py` under:
```python
FMP_API_KEY = "your_fmp_api_key"
FRED_API_KEY = "your_fred_api_key"
```

---

## 📁 Project Structure
```
smart-budget-tracker/
├── app.py
├── requirements.txt
├── data/
│   └── transactions.csv (created automatically)
└── README.md
```

---

## 🌍 Deploy on Streamlit Cloud
1. Push this repo to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click **New App** and select your repo & `app.py`
4. Done! 🎉 Share your app URL

---

## 👩‍💻 Built With
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/python/)
- [FMP API](https://financialmodelingprep.com/)
- [FRED API](https://fred.stlouisfed.org/)

---

## 📬 Contact
Created by Emily Huddleston for an Advanced Financial Modeling project.
Feel free to reach out with questions or ideas!