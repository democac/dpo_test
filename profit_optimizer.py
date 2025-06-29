# profit_optimizer.py

import streamlit as st
import pandas as pd

# === Load Data ===
data = pd.read_csv('dealer_data.csv')

# === Simulate logged-in dealer ===
logged_in_dealer = 'Best Auto'  # simulate logged-in dealer for demo
dealer_data = data[data['Dealer'] == logged_in_dealer].iloc[0]

# === Brand styling ===
st.markdown("""
    <style>
    .stApp { background-color: #f7f9fc; }
    .big-font { font-size:32px !important; }
    </style>
""", unsafe_allow_html=True)

# === Logo ===
st.image("https://www.creditacceptance.com/themes/creditacceptance/images/ca-logo.png", width=200)

# === App Header ===
st.markdown(f"<h1 class='big-font'>🚗 Dealer Profit Optimizer</h1>", unsafe_allow_html=True)
st.subheader(f"👋 Welcome, {logged_in_dealer}!")

# === Metrics ===
st.header("📊 Key Performance Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Approval Rate", f"{dealer_data['ApprovalRate']}%")
col2.metric("Early Default Rate", f"{dealer_data['EarlyDefaultRate']}%")
col3.metric("Backend Profit", f"${dealer_data['BackendProfit']:,}")

# === Trust Score ===
st.header("🔒 Dealer Trust Score")
trust_score = 100
if dealer_data['EarlyDefaultRate'] > 10:
    trust_score -= 10
if dealer_data['ApprovalRate'] < 75:
    trust_score -= 10
st.metric("Trust Score", f"{trust_score}/100")
st.progress(trust_score)

# === Trend Chart ===
st.header("📈 Performance Trend")

trend_data = pd.DataFrame({
    'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
    'Approval Rate': [70, 72, 74, dealer_data['ApprovalRate']],
    'Early Default Rate': [14, 13, 12, dealer_data['EarlyDefaultRate']],
}).set_index('Month')

st.line_chart(trend_data)

# === Profit Impact Calculator ===
st.header("💰 Profit Impact")
early_default = dealer_data['EarlyDefaultRate']
loss_perc = early_default - 7  # target benchmark
monthly_loss = loss_perc * 500 if loss_perc > 0 else 0
annual_loss = monthly_loss * 12

st.write(f"Your current early default rate of {early_default}% may cost about **${monthly_loss}/month**, or **${annual_loss}/year** in backend profit.")

# === What-If Simulator ===
st.header("🔄 What-If Scenario")
target_default = st.slider(
    "Target Early Default Rate",
    5, 15, int(early_default),
    key="slider_target_default"
)

savings = (early_default - target_default) * 500 if early_default > target_default else 0
annual_savings = savings * 12

if savings > 0:
    st.success(f"If you reduce your Early Default Rate to {target_default}%, you could gain ~${annual_savings}/year in backend profit.")
else:
    st.info("Great job! You're already at or below your target.")

# === Action Flow ===
st.header("✅ Next Best Action")
if early_default > 10:
    st.write("🔑 **Tip:** Focus on verifying income and job stability for subprime buyers.")
    st.download_button(
        "Download Income Verification Checklist",
        "Checklist: 1) Verify pay stubs\n2) Validate employer\n3) Reconfirm down payment."
    )
elif dealer_data['ApprovalRate'] < 75:
    st.write("📄 **Tip:** Review deal structure & doc accuracy. Use the Pre-Funding Checklist.")
else:
    st.write("🎉 Your portfolio is in good shape — keep it up!")

st.caption("Built with ❤️ for the Credit Acceptance Hackathon")
