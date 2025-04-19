# 💸 Smart Budgeting & Expense Tracker

An interactive personal finance dashboard built with **Streamlit**, designed to help users:

- 🧾 Track income and spending
- 🎯 Set savings goals and monitor progress
- 📊 Visualize spending trends and budgeting compliance
- 🌍 Explore real-time market insights and economic indicators

---

## 🚀 Live App

👉 [Launch the Streamlit App] (https://smart-budget-tracker-dyjcxnhxmq34zdn5eytner.streamlit.app/) 

---

## 🧩 Features

### 💰 Budget Tracking
- Add income and expense transactions manually
- Upload transactions via CSV
- Categorize expenses for visual analysis

### 📈 Financial Summary Dashboard
- Monthly income vs. net savings line chart
- Spending by category pie chart
- Monthly expenses bar chart
- Savings goal progress tracker
- Monthly budget compliance check
- Export all data as CSV

### 🌍 Market Insights
Powered by [Financial Modeling Prep](https://financialmodelingprep.com) and [FRED](https://fred.stlouisfed.org/):
- 📊 Stock quotes for AAPL, MSFT, WMT
- 📈 U.S. CPI (Inflation)
- 🏦 Fed Funds Rate
- 📉 Unemployment Rate
- 🧠 Real U.S. GDP (chained 2012 dollars)

### ⚙️ Settings Page
- Set session-based default budget and savings goal
- Reset all data with a single click

---

## 🗂️ CSV Format for Upload
Make sure your file includes the following columns:

```csv
Date,Amount,Category,Description
2024-12-01,1200,Income,Paycheck
2024-12-05,-80,Groceries,Trader Joe's
```

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/emh2003/smart-budget-tracker.git
cd smart-budget-tracker

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 🔐 API Keys (FMP & FRED)
Store your API keys in `.streamlit/secrets.toml` like this:

```toml
FMP_API_KEY = "your_fmp_key"
FRED_API_KEY = "your_fred_key"
```

You can get free keys from:
- [FMP API](https://financialmodelingprep.com/developer)
- [FRED API](https://fred.stlouisfed.org/docs/api/api_key.html)

---

## ☁️ Deploy to Streamlit Cloud

1. Push your repo to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repo
4. Set your API keys in **Settings > Secrets**
5. Deploy and share the app link

---

## 🧑‍💻 Built With

- [Streamlit](https://streamlit.io)
- [Plotly](https://plotly.com/python/)
- [Pandas](https://pandas.pydata.org/)
- [Financial Modeling Prep API](https://financialmodelingprep.com)
- [FRED API](https://fred.stlouisfed.org/)

---

## 📘 License

MIT License. Free to use and adapt.
---

## 📬 Contact
Created by Emily Huddleston for an Advanced Financial Modeling project.
Feel free to reach out with questions or ideas!