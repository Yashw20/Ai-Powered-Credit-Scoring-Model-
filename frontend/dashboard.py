import streamlit as st
import requests
import os
from datetime import datetime
import plotly.graph_objects as go

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

/* ── Report card ── */
.report-card {
    background: #1a1d27;
    border: 0.5px solid #2a2d3e;
    border-radius: 14px;
    padding: 24px 28px;
    margin-top: 24px;
}
.report-title {
    font-size: 16px;
    font-weight: 700;
    color: #e8eaf6;
    margin-bottom: 4px;
}
.report-subtitle {
    font-size: 12px;
    color: #8b90a7;
    margin-bottom: 20px;
}
.report-section {
    margin-bottom: 20px;
}
.report-section-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6c63ff;
    margin-bottom: 10px;
    border-bottom: 0.5px solid #2a2d3e;
    padding-bottom: 6px;
}
.report-row {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    font-size: 13px;
    border-bottom: 0.5px solid #1e2130;
}
.report-row .label { color: #8b90a7; }
.report-row .value { color: #e8eaf6; font-weight: 500; }
.report-row .value.flag { color: #ff6b6b; }
.report-row .value.good { color: #00c9a7; }
.report-row .value.warn { color: #ffa94d; }
.score-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    margin-top: 8px;
}
.score-low  { background: rgba(0,201,167,0.15); color: #00c9a7; border: 0.5px solid rgba(0,201,167,0.4); }
.score-med  { background: rgba(255,169,77,0.15); color: #ffa94d; border: 0.5px solid rgba(255,169,77,0.4); }
.score-high { background: rgba(255,107,107,0.15); color: #ff6b6b; border: 0.5px solid rgba(255,107,107,0.4); }
.factor-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 0;
    font-size: 13px;
    border-bottom: 0.5px solid #1e2130;
}
.factor-icon { font-size: 15px; }
.factor-label { color: #8b90a7; flex: 1; }
.factor-impact { font-weight: 500; }
.impact-neg { color: #ff6b6b; }
.impact-pos { color: #00c9a7; }
.impact-neu { color: #ffa94d; }

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

        # ── Charts ──────────────────────────────────────────────────────────
        prob  = result["default_probability"]
        score = result["credit_score"]
        risk  = result["risk"]

        ch1, ch2, ch3 = st.columns(3)

        # 1. Credit Score Gauge
        with ch1:
            gauge_color = "#00c9a7" if score >= 750 else ("#ffa94d" if score >= 650 else "#ff6b6b")
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text": "Credit Score", "font": {"color": "#8b90a7", "size": 13}},
                number={"font": {"color": gauge_color, "size": 36}},
                gauge={
                    "axis": {"range": [300, 850], "tickcolor": "#8b90a7", "tickfont": {"color": "#8b90a7", "size": 10}},
                    "bar": {"color": gauge_color, "thickness": 0.3},
                    "bgcolor": "#12141e",
                    "bordercolor": "#2a2d3e",
                    "steps": [
                        {"range": [300, 650], "color": "rgba(255,107,107,0.15)"},
                        {"range": [650, 750], "color": "rgba(255,169,77,0.15)"},
                        {"range": [750, 850], "color": "rgba(0,201,167,0.15)"},
                    ],
                    "threshold": {"line": {"color": gauge_color, "width": 3}, "thickness": 0.75, "value": score}
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(26,29,39,1)",
                plot_bgcolor="rgba(26,29,39,1)",
                font={"color": "#e8eaf6"},
                height=220,
                margin=dict(l=20, r=20, t=40, b=10)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        # 2. Default Probability Bar
        with ch2:
            safe_pct  = round((1 - prob) * 100, 1)
            risk_pct  = round(prob * 100, 1)
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                name="Safe",
                x=["Probability"],
                y=[safe_pct],
                marker_color="#00c9a7",
                marker_line_width=0,
                width=0.4
            ))
            fig_bar.add_trace(go.Bar(
                name="Default Risk",
                x=["Probability"],
                y=[risk_pct],
                marker_color="#ff6b6b",
                marker_line_width=0,
                width=0.4
            ))
            fig_bar.update_layout(
                barmode="stack",
                title={"text": "Default Probability", "font": {"color": "#8b90a7", "size": 13}, "x": 0.5},
                paper_bgcolor="rgba(26,29,39,1)",
                plot_bgcolor="rgba(26,29,39,1)",
                font={"color": "#e8eaf6"},
                height=220,
                margin=dict(l=20, r=20, t=40, b=10),
                legend={"font": {"size": 11}, "bgcolor": "rgba(0,0,0,0)"},
                yaxis={"range": [0, 100], "ticksuffix": "%", "gridcolor": "#2a2d3e", "tickfont": {"color": "#8b90a7"}},
                xaxis={"tickfont": {"color": "#8b90a7"}}
            )
            fig_bar.add_annotation(
                x=0, y=risk_pct/2,
                text=f"{risk_pct}%",
                showarrow=False,
                font={"color": "#fff", "size": 14, "family": "Arial Black"}
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # 3. Radar Chart
        with ch3:
            def norm(val, lo, hi):
                return max(0, min(1, (val - lo) / (hi - lo)))

            # Invert bad factors so higher = better on radar
            r_income   = norm(annual_inc, 20000, 150000)
            r_accounts = norm(total_acc, 0, 40)
            r_mortgage = norm(mort_acc, 0, 5)
            r_rate     = 1 - norm(int_rate, 0, 30)
            r_dti      = 1 - norm(dti, 0, 50)
            r_bk       = 1 - norm(pub_rec_bankruptcies, 0, 3)

            categories = ["Income", "Accounts", "Mortgage", "Low Rate", "Low DTI", "No Bankrupt"]
            values     = [r_income, r_accounts, r_mortgage, r_rate, r_dti, r_bk]
            values_pct = [round(v * 100) for v in values]

            fig_radar = go.Figure(go.Scatterpolar(
                r=values_pct + [values_pct[0]],
                theta=categories + [categories[0]],
                fill="toself",
                fillcolor="rgba(108,99,255,0.2)",
                line={"color": "#6c63ff", "width": 2},
                marker={"color": "#6c63ff", "size": 5}
            ))
            fig_radar.update_layout(
                polar={
                    "radialaxis": {"visible": True, "range": [0, 100], "gridcolor": "#2a2d3e", "tickfont": {"color": "#8b90a7", "size": 9}},
                    "angularaxis": {"tickfont": {"color": "#8b90a7", "size": 10}, "gridcolor": "#2a2d3e"},
                    "bgcolor": "rgba(18,20,30,1)"
                },
                title={"text": "Risk Factor Radar", "font": {"color": "#8b90a7", "size": 13}, "x": 0.5},
                paper_bgcolor="rgba(26,29,39,1)",
                font={"color": "#e8eaf6"},
                height=220,
                margin=dict(l=30, r=30, t=40, b=10),
                showlegend=False
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # ── Risk Report ─────────────────────────────────────────────────────
        prob       = result["default_probability"]
        score      = result["credit_score"]
        risk       = result["risk"]
        now        = datetime.now().strftime("%d %B %Y, %I:%M %p")

        if risk == "Low":
            badge_cls  = "score-low"
            badge_icon = "✅"
            recommendation = "This applicant presents a strong credit profile. Loan approval is recommended with standard terms."
        elif risk == "Medium":
            badge_cls  = "score-med"
            badge_icon = "⚠️"
            recommendation = "This applicant presents moderate risk. Consider approval with higher interest rate or reduced loan amount. Request additional documentation."
        else:
            badge_cls  = "score-high"
            badge_icon = "❌"
            recommendation = "This applicant presents significant default risk. Loan approval is not recommended. If proceeding, require collateral and co-signer."

        bk_color = "#ff6b6b" if pub_rec_bankruptcies > 0 else "#00c9a7"

        def rate_factor(label, value, low_thresh, high_thresh, higher_is_bad=True):
            if higher_is_bad:
                if value <= low_thresh:
                    cls, icon, impact = "impact-pos", "✅", "Low impact"
                elif value <= high_thresh:
                    cls, icon, impact = "impact-neu", "⚠️", "Moderate impact"
                else:
                    cls, icon, impact = "impact-neg", "🔴", "High impact"
            else:
                if value >= high_thresh:
                    cls, icon, impact = "impact-pos", "✅", "Positive factor"
                elif value >= low_thresh:
                    cls, icon, impact = "impact-neu", "⚠️", "Moderate factor"
                else:
                    cls, icon, impact = "impact-neg", "🔴", "Weak factor"
            return (
                "<div class=\"factor-row\">"
                "<span class=\"factor-icon\">" + icon + "</span>"
                "<span class=\"factor-label\">" + label + " — <b style=\"color:#e8eaf6\">" + str(value) + "</b></span>"
                "<span class=\"factor-impact " + cls + "\">" + impact + "</span>"
                "</div>"
            )

        factors_html = (
            rate_factor("Interest Rate", int_rate, 10, 20, higher_is_bad=True) +
            rate_factor("Debt-to-Income Ratio", dti, 15, 30, higher_is_bad=True) +
            rate_factor("Loan-to-Income Ratio", round(loan_amnt/annual_inc, 2), 0.2, 0.5, higher_is_bad=True) +
            rate_factor("Total Accounts", total_acc, 10, 20, higher_is_bad=False) +
            rate_factor("Mortgage Accounts", mort_acc, 1, 3, higher_is_bad=False) +
            rate_factor("Past Bankruptcies", pub_rec_bankruptcies, 0, 0, higher_is_bad=True)
        )

        report_html = (
            "<div class=\"report-card\">"
            "<div class=\"report-title\">📋 Credit Risk Report</div>"
            "<div class=\"report-subtitle\">Generated on " + now + "</div>"

            "<div class=\"report-section\">"
            "<div class=\"report-section-title\">Summary</div>"
            "<div class=\"report-row\"><span class=\"label\">Credit Score</span><span class=\"value\">" + str(score) + " / 850</span></div>"
            "<div class=\"report-row\"><span class=\"label\">Default Probability</span><span class=\"value\">" + str(round(prob*100,1)) + "%</span></div>"
            "<div class=\"report-row\"><span class=\"label\">Risk Classification</span>"
            "<span class=\"score-badge " + badge_cls + "\">" + badge_icon + " " + risk + " Risk</span></div>"
            "</div>"

            "<div class=\"report-section\">"
            "<div class=\"report-section-title\">Applicant Data</div>"
            "<div class=\"report-row\"><span class=\"label\">Loan Amount</span><span class=\"value\">$" + "{:,}".format(loan_amnt) + "</span></div>"
            "<div class=\"report-row\"><span class=\"label\">Annual Income</span><span class=\"value\">$" + "{:,}".format(annual_inc) + "</span></div>"
            "<div class=\"report-row\"><span class=\"label\">Interest Rate</span><span class=\"value\">" + str(int_rate) + "%</span></div>"
            "<div class=\"report-row\"><span class=\"label\">Debt-to-Income Ratio</span><span class=\"value\">" + str(dti) + "</span></div>"
            "<div class=\"report-row\"><span class=\"label\">Total Accounts</span><span class=\"value\">" + str(total_acc) + "</span></div>"
            "<div class=\"report-row\"><span class=\"label\">Mortgage Accounts</span><span class=\"value\">" + str(mort_acc) + "</span></div>"
            "<div class=\"report-row\"><span class=\"label\">Past Bankruptcies</span>"
            "<span class=\"value\" style=\"color:" + bk_color + "\">" + str(pub_rec_bankruptcies) + "</span></div>"
            "</div>"

            "<div class=\"report-section\">"
            "<div class=\"report-section-title\">Factor Analysis</div>"
            + factors_html +
            "</div>"

            "<div class=\"report-section\">"
            "<div class=\"report-section-title\">How the Score was Calculated</div>"
            "<div class=\"report-row\"><span class=\"label\">Base Score</span><span class=\"value\">300</span></div>"
            "<div class=\"report-row\"><span class=\"label\">ML Model Adjustment</span><span class=\"value\">+" + str(score-300) + " pts (default prob " + str(round(prob*100,1)) + "%)</span></div>"
            "<div class=\"report-row\"><span class=\"label\">Formula</span><span class=\"value\">300 + (1 - " + str(round(prob,3)) + ") x 550</span></div>"
            "<div class=\"report-row\"><span class=\"label\">Final Score</span><span class=\"value good\">" + str(score) + "</span></div>"
            "</div>"

            "<div class=\"report-section\" style=\"margin-bottom:0\">"
            "<div class=\"report-section-title\">Recommendation</div>"
            "<p style=\"color:#c8cad8; font-size:13px; line-height:1.6; margin:0\">" + recommendation + "</p>"
            "</div>"
            "</div>"
        )

        st.markdown(report_html, unsafe_allow_html=True)

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the prediction API — make sure your FastAPI server is running.")