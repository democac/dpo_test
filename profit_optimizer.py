# profit_optimizer.py
import streamlit as st
import pandas as pd

data = pd.read_csv('dealer_data.csv')

st.title("🚗 Dealer Profit Optimizer")

dealer_names = data['Dealer'].tolist()
selected_dealer = st.selectbox("Select Dealer", dealer_names)

dealer_data = data[data['Dealer'] == selected_dealer].iloc[0]

st.subheader("📊 Dealer Performance Metrics")
st.write(f"**Approval Rate:** {dealer_data['ApprovalRate']}%")
st.write(f"**Early Default Rate:** {dealer_data['EarlyDefaultRate']}%")
st.write(f"**Average Advance:** ${dealer_data['AdvanceAmount']:,}")
st.write(f"**Current Backend Profit:** ${dealer_data['BackendProfit']:,}")

st.subheader("ℹ️ Metric Explanation")
if st.button("Explain Approval Rate"):
    st.info("Approval Rate means the % of apps that get funded. Higher is better!")
if st.button("Explain Early Default Rate"):
    st.info("Higher early default rate reduces backend profit.")

st.subheader("💰 Profit Impact")
early_default = dealer_data['EarlyDefaultRate']
backend = dealer_data['BackendProfit']
loss_perc = early_default - 7
monthly_loss = loss_perc * 500 if loss_perc > 0 else 0
st.write(f"Estimated loss from early defaults: ${monthly_loss}/month")

st.subheader("🔄 What-If Simulator")
target_default = st.slider("Target Early Default Rate", 5, 15, int(early_default))
savings = (early_default - target_default) * 500 if early_default > target_default else 0
annual_savings = savings * 12
st.write(f"If you reduce Early Default to {target_default}%, you gain ~${annual_savings}/year backend profit.")

st.subheader("✅ Next Best Action")
if early_default > 10:
    st.write("Tip: Improve income verification for subprime customers.")
else:
    st.write("Great job! Keep up the good portfolio quality.")
