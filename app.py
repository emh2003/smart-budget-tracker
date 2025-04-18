import streamlit as st 
import pandas as pd
import os
import requests
import plotly.express as px
os.makedirs("data", exist_ok=True)

FMP_API_KEY = os.getenv("FMP_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")


# Set page config
st.set_page_config(page_title="Smart Budgeting Tool", layout="centered")
st.title("💸 Smart Budgeting and Expense Tracker")

# Sidebar navigation
menu = ["Home", "Add Transaction", "View Summary", "Settings"]
choice = st.sidebar.radio("Navigate to:", menu)

# File path for storing transactions
file_path = "data/transactions.csv"

# Home page
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

# Add Transaction page
elif choice == "Add Transaction":
    st.subheader("Add a New Transaction")

    # --- Category selection (outside form for dynamic response) ---
    category = st.selectbox("Category", ["Income", "Rent", "Groceries", "Utilities", "Entertainment", "Other"])

    if category == "Other":
        transaction_type = st.radio("Is this an income or expense?", ["Expense", "Income"])
    else:
        transaction_type = "Income" if category == "Income" else "Expense"

    # --- Manual Entry Form ---
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        date = col1.date_input("Date")

        if transaction_type == "Expense":
            amount = col2.number_input("Amount (positive number)", min_value=0.0, format="%.2f")
            amount = -amount  # Store as negative
        else:
            amount = col2.number_input("Amount", min_value=0.0, format="%.2f")

        description = st.text_input("Description")

        submitted = st.form_submit_button("Add Transaction")

        if submitted:
            new_data = {
                "Date": [date],
                "Amount": [amount],
                "Category": [category],
                "Description": [description]
            }

            new_df = pd.DataFrame(new_data)

            if os.path.exists(file_path):
                new_df.to_csv(file_path, mode='a', header=False, index=False)
            else:
                new_df.to_csv(file_path, index=False)

            st.success("Transaction added successfully!")

    # --- CSV Upload Section ---
    st.markdown("---")
    st.subheader("📁 Upload Transactions from CSV")

    with st.expander("📌 CSV Upload Instructions"):
        st.markdown("""
        Your CSV file must contain the following **columns**:  
        - `Date` (format: YYYY-MM-DD)  
        - `Amount` (positive for income, negative for expenses)  
        - `Category` (e.g., Income, Rent, Groceries)  
        - `Description` (optional text)

        **Example:**

        ```
        Date,Amount,Category,Description  
        2024-12-01,1200,Income,Paycheck  
        2024-12-05,-80,Groceries,Trader Joe's  
        ```
        """)

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)
            expected_cols = {"Date", "Amount", "Category", "Description"}
            if not expected_cols.issubset(uploaded_df.columns):
                st.error(f"CSV file must contain the following columns: {expected_cols}")
            else:
                uploaded_df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
                st.success("Transactions imported successfully!")
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

# View Summary page
elif choice == "View Summary":
    st.subheader("Financial Summary")

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])

        with st.expander("📄 View Raw Transactions"):
            st.dataframe(df)

        # Key Financial Metrics
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

        st.markdown("---")
        st.subheader("📆 Monthly Budget Compliance")
        monthly_budget = st.number_input("Set your monthly budget ($)", min_value=0.0, step=100.0, format="%.2f")

        current_month = pd.to_datetime("today").month
        current_year = pd.to_datetime("today").year
        this_month_df = df[(df['Date'].dt.month == current_month) & (df['Date'].dt.year == current_year)]
        this_month_expenses = this_month_df[this_month_df['Category'] != 'Income']['Amount'].abs().sum()

        if monthly_budget > 0:
            budget_status = this_month_expenses <= monthly_budget
            status_icon = "✅" if budget_status else "⚠️"
            st.metric("This Month's Spending", f"${this_month_expenses:,.2f}",
                      delta=f"${monthly_budget - this_month_expenses:,.2f}")
            st.write(f"{status_icon} **You are {'within' if budget_status else 'over'} your budget!**")

        # Monthly Income vs. Net Savings
        st.markdown("---")
        st.subheader("📈 Monthly Income vs. Net Savings")
        df['YearMonth'] = df['Date'].dt.strftime("%Y-%m")
        summary_monthly = df.pivot_table(
            index='YearMonth',
            columns='Category',
            values='Amount',
            aggfunc='sum'
        ).fillna(0)


        if 'Income' in summary_monthly.columns:
            summary_monthly['Net'] = summary_monthly['Income'] - summary_monthly.drop('Income', axis=1).sum(axis=1)
        else:
            summary_monthly['Net'] = -summary_monthly.sum(axis=1)

        with st.expander("📈 View Monthly Income and Net Savings Chart", expanded=True):
            line_chart = px.line(
                summary_monthly.reset_index(),
                x="YearMonth",
                y=["Income", "Net"],
                title="Monthly Income and Net Savings",
                markers=True,
                labels={"Income": "Total Income", "Net": "Net Savings", "YearMonth": "Month"},
                hover_data={"Income": ":.2f", "Net": ":.2f"}
            )
            line_chart.update_layout(xaxis_title="Month", yaxis_title="Amount ($)")
            st.plotly_chart(line_chart)

        # Net Savings Over Time
        st.markdown("---")
        st.subheader("📉 Net Savings Over Time")
        net_trend = summary_monthly.reset_index()[['YearMonth', 'Net']]
        net_trend['YearMonth'] = pd.to_datetime(net_trend['YearMonth'])

        with st.expander("📉 View Net Savings Trend", expanded=False):
            net_line = px.line(
                net_trend,
                x="YearMonth",
                y="Net",
                markers=True,
                title="Net Savings Trend Over Time",
                labels={"YearMonth": "Month", "Net": "Net Savings"},
                hover_data={"Net": ":.2f"}
            )
            net_line.update_layout(xaxis_title="Month", yaxis_title="Amount ($)")
            st.plotly_chart(net_line)

        # Monthly Expenses Breakdown
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
        st.subheader("🗑️ Manage Transactions")
        df_display = df.copy()
        df_display["Index"] = df_display.index
        df_display = df_display[["Index", "Date", "Amount", "Category", "Description"]]

        selected_indices = st.multiselect(
            "Select transactions to delete:",
            df_display["Index"],
            format_func=lambda x: f"{df_display.loc[x, 'Date'].date()} - {df_display.loc[x, 'Description']} (${df_display.loc[x, 'Amount']})"
        )

        if selected_indices:
            if st.button("Delete Selected Transactions"):
                df = df.drop(index=selected_indices).reset_index(drop=True)
                df.to_csv(file_path, index=False)
                st.success(f"Deleted {len(selected_indices)} transaction(s).")
                try:
                    st.experimental_rerun()
                except:
                    st.warning("Please manually refresh the page to see the changes.")

        st.markdown("---")
        st.subheader("📤 Export Transactions")
        if not df.empty:
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Transactions as CSV",
                data=csv,
                file_name="transactions.csv",
                mime="text/csv"
            )
        else:
            st.info("No data available to export.")

        st.markdown("You can print this dashboard using **Ctrl+P** or your browser's print feature and save it as a PDF.")
        st.markdown("---")
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

        # --- Stock Quotes (AAPL, MSFT, WMT) ---
        st.markdown("### 📊 Stock Quotes")
        quotes = fetch_fmp_quote("AAPL,MSFT,WMT")
        if quotes:
            for stock in quotes:
                st.metric(stock["name"], f"${stock['price']:.2f}", f"{stock['changesPercentage']:.2f}%")

        # --- Inflation (CPI) ---
        date, inflation = fetch_fred_data("CPIAUCSL")
        if inflation:
            st.subheader("📈 U.S. Inflation (CPI)")
            st.write(f"**As of {date}**, CPI index value is **{inflation}**")

        # --- Fed Funds Rate ---
        date, fed_rate = fetch_fred_data("FEDFUNDS")
        if fed_rate:
            st.subheader("🏦 Federal Funds Rate")
            st.write(f"**As of {date}**, Fed Funds Rate is **{fed_rate}%**")

        # --- Unemployment Rate ---
        date, unemployment = fetch_fred_data("UNRATE")
        if unemployment:
            st.subheader("📉 U.S. Unemployment Rate")
            st.write(f"**As of {date}**, Unemployment Rate is **{unemployment}%**")

        # --- Real GDP (Chained 2012 Dollars) ---
        date, gdp = fetch_fred_data("GDPC1")
        if gdp:
            st.subheader("📊 Real U.S. GDP (Chained 2012 $)")
            st.write(f"**As of {date}**, Real GDP is **${float(gdp):,.2f} Billion**")

elif choice == "Settings":
    st.subheader("⚙️ App Settings")

    st.markdown("Use the options below to customize your experience.")

    # Default values (stored in session state)
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