# app.py — Smart Budgeting and Expense Tracker (Final Version with Market Insights page)

import streamlit as st 
import pandas as pd
import os
import requests
import plotly.express as px

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# API keys from environment variables
FMP_API_KEY = os.getenv("FMP_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")

# Set page config
st.set_page_config(page_title="Smart Budgeting Tool", layout="centered")
st.title("💸 Smart Budgeting and Expense Tracker")

# Sidebar navigation
menu = ["Home", "Add Transaction", "View Summary", "Market Insights", "Settings"]
choice = st.sidebar.radio("Navigate to:", menu)

# File path for transactions
file_path = "data/transactions.csv"

# --- HOME ---
if choice == "Home":
    st.markdown("## 👋 Welcome to the Smart Budgeting & Expense Tracker")
    st.markdown("""
    This interactive dashboard helps you:
    - 🧾 Track income and expenses
    - 🎯 Set and monitor savings goals
    - 📊 Visualize your spending and budgeting
    - 🌍 Explore real economic indicators

    Use the sidebar to get started! ⬅️
    """)

# --- ADD TRANSACTION ---
elif choice == "Add Transaction":
    st.subheader("Add a New Transaction")
    category = st.selectbox("Category", ["Income", "Rent", "Groceries", "Utilities", "Entertainment", "Other"])

    if category == "Other":
        transaction_type = st.radio("Is this an income or expense?", ["Expense", "Income"])
    else:
        transaction_type = "Income" if category == "Income" else "Expense"

    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        date = col1.date_input("Date")
        amount = col2.number_input("Amount", min_value=0.0, format="%.2f")
        if transaction_type == "Expense":
            amount = -amount
        description = st.text_input("Description")
        submitted = st.form_submit_button("Add Transaction")

        if submitted:
            new_data = pd.DataFrame([[date, amount, category, description]],
                                    columns=["Date", "Amount", "Category", "Description"])
            if os.path.exists(file_path):
                new_data.to_csv(file_path, mode='a', header=False, index=False)
            else:
                new_data.to_csv(file_path, index=False)
            st.success("Transaction added successfully!")

    st.markdown("---")
    st.subheader("📁 Upload Transactions from CSV")
    with st.expander("📌 CSV Upload Instructions"):
        st.markdown("""
        Your CSV file must contain the following **columns**:  
        - `Date` (YYYY-MM-DD)  
        - `Amount` (positive for income, negative for expenses)  
        - `Category` (e.g., Income, Rent)  
        - `Description` (optional)
        """)

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)
            expected_cols = {"Date", "Amount", "Category", "Description"}
            if expected_cols.issubset(uploaded_df.columns):
                uploaded_df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
                st.success("Transactions imported successfully!")
            else:
                st.error(f"CSV file must contain columns: {expected_cols}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- VIEW SUMMARY ---
elif choice == "View Summary":
    st.subheader("Financial Summary")

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])

        # ✅ Normalize category labels
        df['Category'] = df['Category'].str.strip().str.title()

        # ✅ View categories for debugging
        st.write("Categories in data:", df['Category'].unique())

        with st.expander("📄 View Raw Transactions"):
            st.dataframe(df)

        # Summary metrics
        total_income = df[df['Category'] == 'Income']['Amount'].sum()
        total_expenses = df[df['Category'] != 'Income']['Amount'].abs().sum()
        net_savings = total_income - total_expenses

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income", f"${total_income:,.2f}")
        col2.metric("Total Expenses", f"${total_expenses:,.2f}")
        col3.metric("Net Savings", f"${net_savings:,.2f}")

        st.markdown("---")
        st.subheader("🎯 Savings Goal Tracker")
        savings_goal = st.number_input("Enter your savings goal ($)", min_value=0.0, step=100.0, format="%.2f")
        if savings_goal > 0:
            percent_achieved = (net_savings / savings_goal) * 100
            st.progress(min(percent_achieved / 100, 1.0))
            st.write(f"**{percent_achieved:.2f}%** of your goal achieved.")

        st.markdown("---")
        st.subheader("📊 Spending by Category")
        expense_df = df[df['Category'] != 'Income']
        if not expense_df.empty:
            expense_summary = expense_df.groupby('Category')['Amount'].sum().abs().sort_values(ascending=False)
            pie_chart = px.pie(
                names=expense_summary.index,
                values=expense_summary.values,
                title="Spending Distribution by Category",
                hole=0.4
            )
            st.plotly_chart(pie_chart)
        else:
            st.info("No expenses to summarize yet.")

        # ✅ Format months for grouping
        df['YearMonth'] = df['Date'].dt.strftime("%Y-%m")

        # ✅ Pivot table
        summary_monthly = df.pivot_table(
            index='YearMonth',
            columns='Category',
            values='Amount',
            aggfunc='sum'
        ).fillna(0)

        # ✅ Show debug output
        st.write("Monthly Summary Table:", summary_monthly)

        # ✅ Calculate net savings per month
        if 'Income' in summary_monthly.columns:
            summary_monthly['Net'] = summary_monthly['Income'] - summary_monthly.drop('Income', axis=1).sum(axis=1)
        else:
            summary_monthly['Net'] = -summary_monthly.sum(axis=1)

        # ✅ Ensure correct index format for plotting
        summary_monthly.index = summary_monthly.index.astype(str)
        summary_monthly = summary_monthly.sort_index()

        st.markdown("---")
        st.subheader("📈 Monthly Income vs. Net Savings")
        with st.expander("📈 View Monthly Income and Net Savings Chart", expanded=True):
            line_chart = px.line(
                summary_monthly,
                x=summary_monthly.index,
                y=["Income", "Net"],
                title="Monthly Income and Net Savings",
                markers=True,
                labels={"x": "Month", "value": "Amount ($)", "variable": "Metric"},
                hover_data={"Income": ":.2f", "Net": ":.2f"}
            )
            line_chart.update_layout(xaxis_title="Month", yaxis_title="Amount ($)")
            st.plotly_chart(line_chart)

        st.subheader("📅 Monthly Expenses Breakdown")
        monthly_exp = df[df['Category'] != 'Income']
        monthly_exp['YearMonth'] = monthly_exp['Date'].dt.strftime("%b %Y")
        bar_data = monthly_exp.groupby('YearMonth')['Amount'].sum().abs().reset_index()
        with st.expander("📊 View Monthly Expenses Chart", expanded=False):
            bar_chart = px.bar(
                bar_data,
                x=bar_data["YearMonth"].astype(str),
                y="Amount",
                text_auto=True,
                title="Monthly Expenses",
                labels={"YearMonth": "Month", "Amount": "Expenses ($)"},
                hover_data={"Amount": ":.2f"}
            )
            bar_chart.update_layout(xaxis_title="Month", yaxis_title="Amount ($)")
            st.plotly_chart(bar_chart)

        st.markdown("---")
        st.subheader("📤 Export Transactions")
        if not df.empty:
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Transactions as CSV", csv, "transactions.csv", "text/csv")
        else:
            st.info("No data available to export.")

# --- MARKET INSIGHTS ---
elif choice == "Market Insights":
    st.subheader("🌍 Market Insights")

    def fetch_fred_data(series_id):
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                observations = response.json()["observations"]
                latest = observations[-1]
                return latest["date"], latest["value"]
            else:
                st.error(f"FRED API Error: {response.status_code}")
                return None, None
        except Exception as e:
            st.error(f"FRED request failed: {e}")
            return None, None

    def fetch_fmp_quote(tickers):
        url = f"https://financialmodelingprep.com/api/v3/quote/{tickers}?apikey={FMP_API_KEY}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"FMP Quote Error: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"FMP request failed: {e}")
            return None

    st.markdown("### 📊 Stock Quotes")
    quotes = fetch_fmp_quote("AAPL,MSFT,WMT")
    if quotes:
        for stock in quotes:
            st.metric(stock["name"], f"${stock['price']:.2f}", f"{stock['changesPercentage']:.2f}%")

    date, inflation = fetch_fred_data("CPIAUCSL")
    if inflation:
        st.subheader("📈 U.S. Inflation (CPI)")
        st.write(f"**As of {date}**, CPI index value is **{inflation}**")

    date, fed_rate = fetch_fred_data("FEDFUNDS")
    if fed_rate:
        st.subheader("🏦 Federal Funds Rate")
        st.write(f"**As of {date}**, Fed Funds Rate is **{fed_rate}%**")

    date, unemployment = fetch_fred_data("UNRATE")
    if unemployment:
        st.subheader("📉 U.S. Unemployment Rate")
        st.write(f"**As of {date}**, Unemployment Rate is **{unemployment}%**")

    date, gdp = fetch_fred_data("GDPC1")
    if gdp:
        st.subheader("📊 Real U.S. GDP (Chained 2012 $)")
        st.write(f"**As of {date}**, Real GDP is **${float(gdp):,.2f} Billion**")

# --- SETTINGS ---
elif choice == "Settings":
    st.subheader("⚙️ App Settings")
    st.markdown("Use the options below to customize your experience.")
    default_budget = st.number_input("Set default monthly budget ($)", min_value=0.0, step=100.0, format="%.2f")
    default_goal = st.number_input("Set default savings goal ($)", min_value=0.0, step=100.0, format="%.2f")

    if st.button("Save Preferences"):
        st.session_state["default_budget"] = default_budget
        st.session_state["default_goal"] = default_goal
        st.success("Preferences saved for this session.")

    st.markdown("---")
    st.subheader("🗑️ Reset All Data")
    if st.button("Delete All Transactions"):
        if os.path.exists(file_path):
            os.remove(file_path)
            st.success("All transactions deleted.")
        else:
            st.info("No transactions file found to delete.")