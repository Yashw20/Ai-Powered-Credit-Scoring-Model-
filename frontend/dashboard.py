import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="AI Credit Scoring",
    page_icon="💳",
    layout="wide"
)

st.markdown("""
<style>

/* ── Base & Background ── */
.stApp {
    background: linear-gradient(135deg, #0f1117 0%, #12151f 50%, #0d1020 100%);
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Dashboard Header ── */
.dash-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 8px;
}
.dash-icon {
    width: 52px; height: 52px;
    border-radius: 14px;
    background: linear-gradient(135deg, #6c63ff, #00c9a7);
    display: flex; align-items: center; justify-content: center;
    font-size: 26px;
}
.dash-title {
    font-size: 28px;
    font-weight: 700;
    color: #e8eaf6;
    margin: 0;
}
.dash-subtitle {
    font-size: 14px;
    color: #8b90a7;
    margin: 2px 0 0;
}
.glow-bar {
    height: 2px;
    border-radius: 1px;
    background: linear-gradient(90deg, #6c63ff, #00c9a7);
    margin: 18px 0 28px;
    opacity: 0.7;
}

/* ── Section Cards ── */
.section-card {
    background: #1a1d27;
    border: 0.5px solid #2a2d3e;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 20px;
}
.section-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8b90a7;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6c63ff, #00c9a7);
    display: inline-block;
}

/* ── Number inputs ── */
div[data-testid="stNumberInput"] input {
    background: #12141e !important;
    border: 0.5px solid #2a2d3e !important;
    border-radius: 8px !important;
    color: #e8eaf6 !important;
    font-size: 15px !important;
    font-weight: 500 !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 2px rgba(108,99,255,0.2) !important;
}
div[data-testid="stNumberInput"] button {
    background: #1a1d27 !important;
    border: 0.5px solid #2a2d3e !important;
    color: #8b90a7 !important;
    border-radius: 6px !important;
}
div[data-testid="stNumberInput"] button:hover {
    background: #2a2d3e !important;
    color: #e8eaf6 !important;
}

/* ── Labels ── */
label, .stSlider label, .stNumberInput label {
    color: #8b90a7 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
}

/* ── Sliders ── */
div[data-testid="stSlider"] > div > div > div {
    background: linear-gradient(90deg, #6c63ff, #00c9a7) !important;
}
div[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: #6c63ff !important;
    font-weight: 600 !important;
}

/* ── Divider ── */
hr {
    border-color: #2a2d3e !important;
    margin: 24px 0 !important;
}

/* ── Predict Button ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #6c63ff 0%, #845ef7 50%, #00c9a7 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 14px 0 !important;
    letter-spacing: 0.04em !important;
    transition: opacity 0.15s, transform 0.12s !important;
    width: 100% !important;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Metric cards ── */
div[data-testid="stMetric"] {
    background: #12141e !important;
    border: 0.5px solid #2a2d3e !important;
    border-radius: 10px !important;
    padding: 16px !important;
}
div[data-testid="stMetricLabel"] {
    color: #8b90a7 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
div[data-testid="stMetricValue"] {
    color: #00c9a7 !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}

/* ── Alerts ── */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: 0.5px solid !important;
}

/* ── Subheader ── */
h3 {
    color: #e8eaf6 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}

/* ── Column gap ── */
div[data-testid="stHorizontalBlock"] {
    gap: 20px !important;
}

</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <div class="dash-icon">💳</div>
  <div>
    <p class="dash-title">AI Credit Scoring</p>
    <p class="dash-subtitle">Loan default risk prediction using machine learning</p>
  </div>
</div>
<div class="glow-bar"></div>
""", unsafe_allow_html=True)

# ── Input columns ────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
    <div class="section-title">
      <span class="dot"></span> Applicant Information
    </div>
    """, unsafe_allow_html=True)

    loan_amnt = st.number_input("Loan Amount ($)", value=15000, step=500, min_value=1000)
    annual_inc = st.number_input("Annual Income ($)", value=65000, step=1000, min_value=10000)
    int_rate = st.slider("Interest Rate (%)", 0.0, 30.0, 11.5, step=0.1)
    dti = st.slider("Debt-To-Income Ratio", 0.0, 50.0, 18.2, step=0.1)

with col2:
    st.markdown("""
    <div class="section-title">
      <span class="dot"></span> Credit Details
    </div>
    """, unsafe_allow_html=True)

    total_acc = st.number_input("Total Accounts", value=22, step=1, min_value=0)
    mort_acc = st.number_input("Mortgage Accounts", value=2, step=1, min_value=0)
    pub_rec_bankruptcies = st.number_input("Past Bankruptcies", value=0, step=1, min_value=0)

st.divider()

# ── Predict button ───────────────────────────────────────────────────────────
if st.button("⚡  Predict Credit Score", use_container_width=True):

    data = {
        "loan_amnt": loan_amnt,
        "int_rate": int_rate,
        "annual_inc": annual_inc,
        "dti": dti,
        "total_acc": total_acc,
        "mort_acc": mort_acc,
        "pub_rec_bankruptcies": pub_rec_bankruptcies,
    }

    try:
        response = requests.post(f"{API_URL}/predict", json=data, timeout=10)
        result = response.json()

        st.markdown("""
        <div class="section-title" style="margin-top:8px">
          <span class="dot"></span> Prediction Results
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Default Probability", f"{result['default_probability'] * 100:.1f}%")
        with c2:
            st.metric("Credit Score", result["credit_score"])
        with c3:
            st.metric("Risk Level", result["risk"])

        if result["risk"] == "Low":
            st.success("✅  Low risk applicant — strong credit profile.")
        elif result["risk"] == "Medium":
            st.warning("⚠️  Moderate risk applicant — review carefully.")
        else:
            st.error("❌  High risk applicant — significant default indicators detected.")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the prediction API — make sure your FastAPI server is running.")