import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="FICO Credit Score Dashboard", page_icon="💳", layout="wide")

st.title("💳 FICO Credit Score Simulator & Smart Dashboard")
st.markdown("""
Use this interactive dashboard to **simulate, visualize, and analyze your FICO-style credit score**  
based on the five major scoring factors.  
Get personalized insights and track how your score changes across simulations.
""")

st.divider()

# --- INPUT SECTION ---
col1, col2 = st.columns(2)

with col1:
    st.header("📥 Input Your Credit Factors (0–100)")
    payment_history = st.slider("Payment History (35%)", 0, 100, 85)
    credit_utilization = st.slider("Credit Utilization (30%)", 0, 100, 70)
    length_credit_history = st.slider("Length of Credit History (15%)", 0, 100, 65)
    credit_mix = st.slider("Credit Mix (10%)", 0, 100, 75)
    new_credit = st.slider("New Credit (10%)", 0, 100, 60)

# --- CALCULATE FICO SCORE ---
weighted_score = (
    (payment_history / 100) * 0.35 +
    (credit_utilization / 100) * 0.30 +
    (length_credit_history / 100) * 0.15 +
    (credit_mix / 100) * 0.10 +
    (new_credit / 100) * 0.10
)

fico_score = round(300 + (weighted_score * 550))

# --- SCORE CATEGORY ---
if fico_score < 580:
    category = "❌ Poor"
    color = "red"
elif 580 <= fico_score < 670:
    category = "⚠️ Fair"
    color = "orange"
elif 670 <= fico_score < 740:
    category = "✅ Good"
    color = "green"
elif 740 <= fico_score < 800:
    category = "💎 Very Good"
    color = "blue"
else:
    category = "🏆 Excellent"
    color = "purple"

# --- DISPLAY RESULTS ---
with col2:
    st.header("📊 Your Score Result")
    st.metric(label="Estimated FICO Credit Score", value=fico_score)
    st.markdown(f"### Category: <span style='color:{color}'>{category}</span>", unsafe_allow_html=True)
    st.progress(min(fico_score / 850, 1.0))

# --- RADAR CHART ---
factors = ['Payment History', 'Credit Utilization', 'Credit Length', 'Credit Mix', 'New Credit']
scores = [payment_history, credit_utilization, length_credit_history, credit_mix, new_credit]

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=scores + [scores[0]],
    theta=factors + [factors[0]],
    fill='toself',
    name='Your Credit Factors',
    line_color='royalblue'
))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=False,
    margin=dict(l=40, r=40, t=40, b=40),
    height=400
)

st.divider()
st.header("📈 Credit Factor Visualization")
st.plotly_chart(fig_radar, use_container_width=True)

# --- RECOMMENDATIONS ---
st.header("💡 Personalized Recommendations")

recommendations = []
if payment_history < 80:
    recommendations.append("✅ Improve **payment history** by making all payments on time.")
if credit_utilization > 30:
    recommendations.append("📉 Reduce **credit utilization** below 30% of available credit.")
if length_credit_history < 70:
    recommendations.append("🕒 Keep older credit accounts open to build **longer history**.")
if credit_mix < 60:
    recommendations.append("💳 Add different credit types (e.g., installment + revolving).")
if new_credit < 60:
    recommendations.append("🧾 Limit **new credit applications**; too many inquiries can lower your score.")

if not recommendations:
    st.success("🌟 Excellent! Your credit profile looks balanced and strong.")
else:
    for rec in recommendations:
        st.write(rec)

# --- SCORE HISTORY TRACKER ---
st.divider()
st.header("📜 Score History & Trends")

if "score_history" not in st.session_state:
    st.session_state.score_history = []

if st.button("💾 Save This Simulation"):
    st.session_state.score_history.append({
        "Score": fico_score,
        "Category": category,
        "Payment History": payment_history,
        "Credit Utilization": credit_utilization,
        "Length History": length_credit_history,
        "Credit Mix": credit_mix,
        "New Credit": new_credit
    })

if st.session_state.score_history:
    df = pd.DataFrame(st.session_state.score_history)
    st.dataframe(df, use_container_width=True)

    # --- Line Chart Trend ---
    st.subheader("📊 Score Trend Over Time")
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        y=df["Score"],
        x=list(range(1, len(df) + 1)),
        mode="lines+markers",
        line=dict(color="royalblue", width=3),
        marker=dict(size=8),
        name="Credit Score"
    ))
    fig_line.update_layout(
        yaxis=dict(title="FICO Score", range=[300, 850]),
        xaxis=dict(title="Simulation Run"),
        height=400
    )
    st.plotly_chart(fig_line, use_container_width=True)

# --- AI-STYLE ANALYSIS ---
st.divider()
st.header("🤖 AI Insight Summary")

analysis = []

if fico_score >= 800:
    analysis.append("Your credit profile is **exceptional**, reflecting strong payment consistency and responsible borrowing habits.")
elif fico_score >= 740:
    analysis.append("You have a **very good credit profile**. Continue maintaining low credit utilization and a long credit history.")
elif fico_score >= 670:
    analysis.append("Your credit is in the **good range** — improving payment history or reducing utilization could elevate it further.")
elif fico_score >= 580:
    analysis.append("Your credit is **fair**. Focus on consistent on-time payments and lowering your debt ratio to move upward.")
else:
    analysis.append("Your score is **poor**, indicating several risk factors. Immediate focus on timely payments and reducing debt will help most.")

if credit_utilization > 50:
    analysis.append("Your **credit utilization is high**, which may signal over-reliance on credit — aim for below 30%.")
if payment_history < 70:
    analysis.append("Your **payment history** shows missed or late payments — prioritize consistency to gain major improvements.")
if length_credit_history < 50:
    analysis.append("A **short credit history** limits your score. Keeping older accounts active can help.")
if new_credit > 80:
    analysis.append("Opening new accounts responsibly shows growth, but too many at once may slightly lower your score temporarily.")

st.write(" ".join(analysis))
st.caption("⚠️ *Generated using simple rule-based AI logic for educational purposes — not financial advice.*")if credit_utilization > 50:
    analysis.append("Your **credit utilization is high**, which may signal over-reliance on credit — aim for below 30%.")
if payment_history < 70:
    analysis.append("Your **payment history** shows missed or late payments — prioritize consistency to gain major improvements.")
if length_credit_history < 50:
    analysis.append("A **short credit history** limits your score. Keeping older accounts active can help.")
if new_credit > 80:
    analysis.append("Opening new accounts responsibly shows growth, but too many at once may slightly lower your score temporarily.")

st.write(" ".join(analysis))
st.caption("⚠️ *Generated using simple rule-based AI logic for educational purposes — not financial advice.*")    recommendations.append("💳 Add different credit types (e.g., installment + revolving).")
if new_credit < 60:
    recommendations.append("🧾 Limit **new credit applications**; too many inquiries can lower your score.")

if not recommendations:
    st.success("🌟 Excellent! Your credit profile looks balanced and strong.")
else:
    for rec in recommendations:
        st.write(rec)

# --- SCORE HISTORY TRACKER ---
st.divider()
st.header("📜 Score History & Trends")

if "score_history" not in st.session_state:
    st.session_state.score_history = []

if st.button("💾 Save This Simulation"):
    st.session_state.score_history.append({
        "Score": fico_score,
        "Category": category,
        "Payment History": payment_history,
        "Credit Utilization": credit_utilization,
        "Length History": length_credit_history,
        "Credit Mix": credit_mix,
        "New Credit": new_credit
    })

if st.session_state.score_history:
    df = pd.DataFrame(st.session_state.score_history)
    st.dataframe(df, use_container_width=True)

    # --- Line Chart Trend ---
    st.subheader("📊 Score Trend Over Time")
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        y=df["Score"],
        x=list(range(1, len(df) + 1)),
        mode="lines+markers",
        line=dict(color="royalblue", width=3),
        marker=dict(size=8),
        name="Credit Score"
    ))
    fig_line.update_layout(
        yaxis=dict(title="FICO Score", range=[300, 850]),
        xaxis=dict(title="Simulation Run"),
        height=400
    )
    st.plotly_chart(fig_line, use_container_width=True)

# --- AI-STYLE ANALYSIS ---
st.divider()
st.header("🤖 AI Insight Summary")

# Generate a dynamic narrative based on score and key factors
analysis = []

if fico_score >= 800:
    analysis.append("Your credit profile is **exceptional**, reflecting strong payment consistency and responsible borrowing habits.")
elif fico_score >= 740:
    analysis.append("You have a **very good credit profile**. Continue maintaining low credit utilization and a long credit history.")
elif fico_score >= 670:
    analysis.append("Your credit is in the **good range** — improving payment history or reducing utilization could elevate it further.")
elif fico_score >= 580:
    analysis.append("Your credit is **fair**. Focus on consistent on-time payments and lowering your debt ratio to move upward.")
else:
    analysis.append("Your score is **poor**, indicating several risk factors. Immediate focus on timely payments and reducing debt will help most.")

if credit_utilization > 50:
    analysis.append("Your **credit utilization is high**, which may signal over-reliance on credit — aim for below 30%.")
if payment_history < 70:
    analysis.append("Your **payment history** shows missed or late payments — prioritize consistency to gain major improvements.")
if length_credit_history < 50:
    analysis.append("A **short credit history** limits your score. Keeping older accounts active can help.")
if new_credit > 80:
    analysis.append("Opening new accounts responsibly shows growth, but too many at once may slightly lower your score temporarily.")

st.write(" ".join(analysis))
st.caption("⚠️ *Generated using simple rule-based AI logic for educational purposes — not financial advice.*")    recommendations.append("💳 Add different credit types (e.g., installment + revolving).")
if new_credit < 60:
    recommendations.append("🧾 Limit **new credit applications**; too many inquiries can lower your score.")

if not recommendations:
    st.success("🌟 Excellent! Your credit profile looks balanced and strong.")
else:
    for rec in recommendations:
        st.write(rec)

# --- SCORE HISTORY TRACKER ---
if "score_history" not in st.session_state:
    st.session_state.score_history = []

if st.button("Save This Simulation"):
    st.session_state.score_history.append({"Score": fico_score, "Category": category})

if st.session_state.score_history:
    st.write("### 📜 Score History (This Session)")
    df = pd.DataFrame(st.session_state.score_history)
    st.dataframe(df, use_container_width=True)
