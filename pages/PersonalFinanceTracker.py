import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize an empty list to store data
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'income' not in st.session_state:
    st.session_state.income = 0

# Set up Streamlit title and description with icons
# st.title("🚀 Personal Finance Tracker")
st.markdown(
    """
    <style>
        .responsive-title {
            text-align: center;
            font-size:50px !important;
        }
        @media (max-width: 600px) {
            .responsive-title {
            text-align: center;
            font-size:30px !important;
            }
        }
    </style>
    <h1 class="responsive-title">🚀Personal Finance Tracker</h1>
    """,
    unsafe_allow_html=True
)

st.sidebar.success("🌟Be Silent And let your success shout")
st.markdown("Track your income and expenses easily! 💰")

# Add Income (First Step)
if st.session_state.income == 0:  # Show income form if income is not added
    with st.form("income_form"):
        st.subheader("💸 Add Income")
        amount_income = st.number_input("Income Amount", min_value=0.0, step=0.01)
        category_income = st.text_input("Income Category (e.g., Salary, Bonus, etc.)")
        date_income = st.date_input("Income Date")
        submit_income_button = st.form_submit_button("Add Income 🚀")

        if submit_income_button:
            if amount_income > 0 and category_income:
                st.session_state.income = amount_income  # Store income in session state
                st.session_state.transactions.append({
                    'Date': date_income,
                    'Type': "Income",
                    'Amount': amount_income,
                    'Category': category_income
                })
                st.success(f"Income of {amount_income} added under {category_income} 💸")
            else:
                st.error("Please enter valid income details. ⚠️")

# Show income and balance after income is added
if st.session_state.income > 0:
    st.write(f"**Total Income:** {st.session_state.income:.2f} 💰")
    
    # Input form for expenses (this is now only available after income is added)
    with st.form("expense_form"):
        st.subheader("💳 Add Expense")
        amount_expense = st.number_input("Expense Amount", min_value=0.0, step=0.01)
        category_expense = st.text_input("Expense Category (e.g., Groceries, Bills, etc.)")
        date_expense = st.date_input("Expense Date")
        submit_expense_button = st.form_submit_button("Add Expense 🛒")

        if submit_expense_button:
            if amount_expense > 0 and category_expense:
                st.session_state.transactions.append({
                    'Date': date_expense,
                    'Type': "Expense",
                    'Amount': amount_expense,
                    'Category': category_expense
                })
                st.session_state.income -= amount_expense  # Subtract expense from income
                st.success(f"Expense of {amount_expense} added under {category_expense} 🛒")
            else:
                st.error("Please enter valid expense details. ⚠️")

    # Show updated balance
    if st.session_state.income >= 0:
        st.write(f"**Remaining Balance:** {st.session_state.income:.2f} 💵")
    else:
        st.write(f"**Balance is negative**: {st.session_state.income:.2f} ⚠️")

    # Create the DataFrame for transactions outside the income/expense logic
    df = pd.DataFrame(st.session_state.transactions)
    
    # Display transaction history
    st.subheader("📜 Transaction History")
    st.dataframe(df)

    # Pie chart for Income vs Expenses
    income = df[df['Type'] == "Income"]['Amount'].sum()
    expense = df[df['Type'] == "Expense"]['Amount'].sum()

    # Check if both income and expenses are available before plotting
    if income > 0 or expense > 0:
        st.subheader("📊 Income vs Expense")
        
        # Pie chart showing the actual values of income and expenses
        fig, ax = plt.subplots()
        ax.pie([income, expense], labels=["Income", "Expense"], autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff6666'])
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)

else:
    st.info("Please add your income first! 🏦")
