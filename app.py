
import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Loan EMI Calculator",
    page_icon="💰",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
}
.main-title {
    text-align: center;
    color: #312e81;
    font-size: 40px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #475569;
    font-size: 17px;
}
.metric-card {
    background: white;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #dbeafe;
    text-align: center;
}
.metric-label {
    color: #64748b;
    font-size: 15px;
}
.metric-value {
    color: #312e81;
    font-size: 25px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">💰 Loan EMI Calculator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Calculate your monthly installments '
    'and plan your loan repayment easily.</div>',
    unsafe_allow_html=True
)

st.write("")
st.divider()

# ---------------- LOAN INPUTS ----------------
st.subheader("📝 Enter Your Loan Details")

with st.form("loan_form"):
    col1, col2 = st.columns(2)

    with col1:
        loan_amount = st.number_input(
            "Loan Amount (₹)",
            min_value=1000,
            max_value=100000000,
            value=500000,
            step=10000
        )

        interest_rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            max_value=50.0,
            value=8.5,
            step=0.1
        )

    with col2:
        tenure_years = st.number_input(
            "Loan Tenure (Years)",
            min_value=1,
            max_value=40,
            value=5,
            step=1
        )

        st.info(
            "Enter your loan amount, interest rate, and tenure. "
            "Click Calculate EMI to view your results."
        )

    calculate = st.form_submit_button(
        "🧮 Calculate EMI",
        use_container_width=True
    )

# ---------------- EMI CALCULATION ----------------
# Results appear after the Calculate EMI button is clicked.

if calculate:
    months = int(tenure_years * 12)
    monthly_rate = interest_rate / (12 * 100)

    if monthly_rate == 0:
        emi = loan_amount / months
    else:
        emi = (
            loan_amount
            * monthly_rate
            * (1 + monthly_rate) ** months
            / ((1 + monthly_rate) ** months - 1)
        )

    total_payment = emi * months
    total_interest = total_payment - loan_amount

    # ---------------- RESULTS ----------------
    st.divider()
    st.subheader("📊 Your Loan Summary")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""<div class="metric-card">
            <div class="metric-label">Monthly EMI</div>
            <div class="metric-value">₹{emi:,.2f}</div>
            </div>""",
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""<div class="metric-card">
            <div class="metric-label">Total Interest</div>
            <div class="metric-value">₹{total_interest:,.2f}</div>
            </div>""",
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""<div class="metric-card">
            <div class="metric-label">Total Repayment</div>
            <div class="metric-value">₹{total_payment:,.2f}</div>
            </div>""",
            unsafe_allow_html=True
        )

    st.write("")

    st.success(
        f"Your estimated monthly EMI is ₹{emi:,.2f} "
        f"for {months} months."
    )

    # ---------------- PAYMENT BREAKDOWN ----------------
    st.divider()
    st.subheader("📈 Principal vs Interest")

    chart_data = pd.DataFrame({
        "Component": ["Loan Principal", "Total Interest"],
        "Amount (₹)": [loan_amount, max(total_interest, 0)]
    })

    st.bar_chart(
        chart_data.set_index("Component"),
        y="Amount (₹)"
    )

    # ---------------- AMORTIZATION SCHEDULE ----------------
    st.divider()
    st.subheader("📅 Monthly Repayment Schedule")

    balance = float(loan_amount)
    schedule = []

    for month in range(1, months + 1):
        interest_component = balance * monthly_rate

        # Make the last payment clear the remaining balance.
        if month == months:
            principal_component = balance
        else:
            principal_component = min(
                emi - interest_component,
                balance
            )

        actual_payment = principal_component + interest_component
        balance = max(0.0, balance - principal_component)

        schedule.append({
            "Month": month,
            "EMI (₹)": round(actual_payment, 2),
            "Principal (₹)": round(principal_component, 2),
            "Interest (₹)": round(interest_component, 2),
            "Remaining Balance (₹)": round(balance, 2)
        })

    schedule_df = pd.DataFrame(schedule)

    st.dataframe(
        schedule_df,
        use_container_width=True,
        hide_index=True
    )

    # ---------------- DOWNLOAD REPORT ----------------
    csv_data = schedule_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Repayment Schedule (CSV)",
        data=csv_data,
        file_name="loan_repayment_schedule.csv",
        mime="text/csv"
    )

    # ---------------- FOOTER ----------------
    st.divider()

    st.caption(
        "Note: This calculator provides estimates. Actual EMI and "
        "repayment amounts may vary due to lender fees, taxes, "
        "rate changes, and repayment terms."
    )

    st.markdown(
        "<center>Built with Python and Streamlit 💙</center>",
        unsafe_allow_html=True
    )

