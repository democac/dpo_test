# profit_optimizer.py

import streamlit as st
import pandas as pd

# === Load Data ===
data = pd.read_csv('dealer_data.csv')

# === Simulate logged-in dealer ===
logged_in_dealer = 'Best Auto'  # change to test different dealers

dealer_data = data[data['Dealer'] == logged_in_dealer].iloc[0]

# === App Header ===
st.title(f"🚗 Dealer Profit Optimizer")
st.subheader(f"👋 Welcome, {logged_in_dealer}!")

# === Performance Metrics ===
st.header("📊 Your Key Performance Metrics")

st.metric("Approval Rate", f"{dealer_data['ApprovalRate']}%")
st.metric("Early Default Rate", f"{dealer_data['EarlyDefaultRate']}%")
st.metric("Average Advance", f"${dealer_data['AdvanceAmount']:,}")
st.metric("Current Backend Profit", f"${dealer_data['BackendProfit']:,}")

# === Simulated trend comparison ===
st.header("📈 Last Month vs This Month")
# Just dummy static values for demo
st.write(f"Approval Rate last month: 70% → This month: {dealer_data['ApprovalRate']}% ✅")
st.write(f"Early Default last month: 14% → This month: {dealer_data['EarlyDefaultRate']}% ✅")

# === Dealer Trust Score ===
st.header("🔒 Dealer Trust Score")
trust_score = 100
if dealer_data['EarlyDefaultRate'] > 10:
    trust_score -= 10
if dealer_data['ApprovalRate'] < 75:
    trust_score -= 10
st.metric("Trust Score", trust_score)

st.caption("Your Trust Score affects your advance % and backend payouts. Keep it high!")

# === Explain metrics section ===
st.header("ℹ️ What This Means")
if st.button("Explain Approval Rate"):
    st.info("Approval Rate is the % of your apps that get funded. Higher approvals mean more cars sold and faster funding.")

if st.button("Explain Early Default Rate"):
    st.info("Early Default Rate is the % of loans that default in the first 90 days. Lower is better — it means better loan quality and more backend profit.")

# === Profit Impact Calculator ===
st.header("💰 Profit Impact")
early_default = dealer_data['EarlyDefaultRate']
loss_perc = early_default - 7  # assume 7% is the healthy benchmark
monthly_loss = loss_perc * 500 if loss_perc > 0 else 0
annual_loss = monthly_loss * 12

st.write(f"Your current early default rate of {early_default}% may cost you about **${monthly_loss}/month**, or **${annual_loss}/year** in lost backend profit.")

# === What-If Simulator ===
st.header("🔄 What-If Simulator")
target_default = st.slider("Target Early Default Rate", 5, 15, int(early_default))

savings = (early_default - target_default) * 500 if early_default > target_default else 0
annual_savings = savings * 12

if savings > 0:
    st.success(f"If you reduce Early Default to {target_default}%, you could gain an extra **${annual_savings}/year** in backend profit.")
else:
    st.info("Great job! You're already at or below your target default rate.")

# === Next Best Action ===
st.header("✅ Next Best Action")
if early_default > 10:
    st.write("🔑 **Tip:** Focus on verifying income and job stability for subprime buyers. Use the Income Verification Checklist to catch risky deals early.")
elif dealer_data['ApprovalRate'] < 75:
    st.write("📄 **Tip:** Review your doc accuracy and deal structuring. Use the Pre-Funding Checklist to improve approval rates.")
else:
    st.write("🎉 Excellent work! Your portfolio is on track — maintain strong screening and document checks.")

# === Footer ===
st.caption("Built with ❤️ using Streamlit | Demo for Credit Acceptance Hackathon")
