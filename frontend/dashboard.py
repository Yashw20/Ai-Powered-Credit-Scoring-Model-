import streamlit as st
import requests
import os
from datetime import datetime
import plotly.graph_objects as go

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="CreditIQ — AI Credit Scoring",
    page_icon="◈",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --bg:       #080a0f;
    --bg2:      #0d1018;
    --surface:  #111420;
    --surface2: #161923;
    --border:   rgba(255,255,255,0.06);
    --border2:  rgba(255,255,255,0.1);
    --accent:   #c8f135;
    --accent2:  #7b61ff;
    --accent3:  #00e5c3;
    --red:      #ff4d6d;
    --orange:   #ff9f1c;
    --text:     #f0f2f8;
    --muted:    #5a6175;
    --muted2:   #8892a4;
}

* { box-sizing: border-box; }

.stApp {
    background: var(--bg) !important;
    font-family: 'Syne', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

/* ── top bar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 0 32px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 40px;
}
.logo { display: flex; align-items: center; gap: 12px; }
.logo-mark {
    width: 38px; height: 38px;
    background: var(--accent);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; font-weight: 800; color: #000;
    font-family: 'Syne', sans-serif;
}
.logo-text { font-size: 20px; font-weight: 800; color: var(--text); letter-spacing: -0.5px; }
.logo-text span { color: var(--accent); }
.nav-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; color: var(--muted2);
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 5px 12px; border-radius: 20px;
    letter-spacing: 0.05em;
}

/* ── section labels ── */
.sec-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; font-weight: 500;
    letter-spacing: 0.15em; text-transform: uppercase;
    color: var(--muted); margin-bottom: 16px;
    display: flex; align-items: center; gap: 8px;
}
.sec-label::before {
    content: ''; display: inline-block;
    width: 16px; height: 1px; background: var(--accent);
}

/* ── input card titles ── */
.input-card-title {
    font-size: 13px; font-weight: 700;
    color: var(--text); letter-spacing: 0.02em;
    margin-bottom: 20px;
    display: flex; align-items: center; gap: 8px;
}
.tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    background: rgba(200,241,53,0.12);
    color: var(--accent);
    padding: 2px 8px; border-radius: 4px; font-weight: 400;
}

/* ── number inputs ── */
div[data-testid="stNumberInput"] input {
    background: var(--bg2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 15px !important;
    font-weight: 400 !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(200,241,53,0.1) !important;
}
div[data-testid="stNumberInput"] button {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--muted2) !important;
    border-radius: 8px !important;
}
div[data-testid="stNumberInput"] button:hover {
    background: var(--border2) !important;
    color: var(--text) !important;
}

/* ── labels ── */
label {
    color: var(--muted2) !important;
    font-size: 11px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* ── sliders ── */
div[data-testid="stSlider"] > div > div > div {
    background: var(--accent) !important;
}
div[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: var(--accent) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 500 !important;
}

/* ── divider ── */
hr { border-color: var(--border) !important; margin: 32px 0 !important; }

/* ── predict button ── */
div[data-testid="stButton"] > button {
    background: var(--accent) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 14px !important;
    font-weight: 800 !important;
    padding: 16px 0 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    width: 100% !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(200,241,53,0.25) !important;
}

/* ── metrics ── */
div[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 20px !important;
}
div[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
}
div[data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 30px !important;
    font-weight: 800 !important;
}

/* ── alerts ── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── result banner ── */
.result-banner {
    padding: 20px 24px; border-radius: 14px;
    margin: 24px 0; display: flex; align-items: center; gap: 16px;
}
.result-banner.low  { background: rgba(0,229,195,0.08); border: 1px solid rgba(0,229,195,0.2); }
.result-banner.med  { background: rgba(255,159,28,0.08); border: 1px solid rgba(255,159,28,0.2); }
.result-banner.high { background: rgba(255,77,109,0.08); border: 1px solid rgba(255,77,109,0.2); }
.rb-icon { font-size: 28px; }
.rb-title { font-size: 16px; font-weight: 700; color: var(--text); }
.rb-sub   { font-size: 13px; color: var(--muted2); margin-top: 2px; }

/* ── report ── */
.report-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 32px; margin-top: 32px;
    position: relative; overflow: hidden;
}
.report-wrap::before {
    content: 'REPORT';
    position: absolute; top: 20px; right: 24px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 0.2em;
    color: var(--border2); font-weight: 500;
}
.report-head {
    display: flex; align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 28px; padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
}
.report-title  { font-size: 22px; font-weight: 800; color: var(--text); letter-spacing: -0.5px; }
.report-date   { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--muted); margin-top: 4px; }
.score-pill    { padding: 8px 20px; border-radius: 40px; font-size: 14px; font-weight: 700; }
.pill-low      { background: rgba(0,229,195,0.15); color: var(--accent3); border: 1px solid rgba(0,229,195,0.3); }
.pill-med      { background: rgba(255,159,28,0.15); color: var(--orange); border: 1px solid rgba(255,159,28,0.3); }
.pill-high     { background: rgba(255,77,109,0.15); color: var(--red); border: 1px solid rgba(255,77,109,0.3); }

.report-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }
.report-block {
    background: var(--bg2); border: 1px solid var(--border);
    border-radius: 12px; padding: 20px;
}
.report-block-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 0.15em;
    text-transform: uppercase; color: var(--accent);
    margin-bottom: 14px; font-weight: 500;
}
.rrow {
    display: flex; justify-content: space-between;
    align-items: center; padding: 8px 0;
    border-bottom: 1px solid var(--border); font-size: 13px;
}
.rrow:last-child { border-bottom: none; }
.rl { color: var(--muted2); }
.rv { color: var(--text); font-weight: 600; font-family: 'JetBrains Mono', monospace; font-size: 13px; }
.rv.good { color: var(--accent3); }
.rv.warn { color: var(--orange); }
.rv.bad  { color: var(--red); }

.factor-item {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 0; border-bottom: 1px solid var(--border); font-size: 13px;
}
.factor-item:last-child { border-bottom: none; }
.fi-dot  { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.fi-label{ color: var(--muted2); flex: 1; }
.fi-val  { color: var(--text); font-family: 'JetBrains Mono', monospace; font-size: 12px; margin-right: 8px; }
.fi-tag  { font-size: 11px; font-weight: 600; padding: 2px 10px; border-radius: 4px; }
.fi-pos  { background: rgba(0,229,195,0.12); color: var(--accent3); }
.fi-neu  { background: rgba(255,159,28,0.12); color: var(--orange); }
.fi-neg  { background: rgba(255,77,109,0.12); color: var(--red); }

.rec-box {
    background: var(--bg2); border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 0 12px 12px 0; padding: 18px 20px; margin-top: 20px;
}
.rec-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 0.15em;
    color: var(--accent); text-transform: uppercase; margin-bottom: 8px;
}
.rec-text { font-size: 14px; color: var(--muted2); line-height: 1.7; }

div[data-testid="stHorizontalBlock"] { gap: 16px !important; }
</style>
""", unsafe_allow_html=True)

# ── Top Bar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="logo">
    <div class="logo-mark">◈</div>
    <div class="logo-text">Credit<span>IQ</span></div>
  </div>
  <div class="nav-badge">AI-POWERED RISK ASSESSMENT</div>
</div>
""", unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-label">Input Parameters</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="input-card-title">Applicant Information <span class="tag">FINANCIAL</span></div>', unsafe_allow_html=True)
    loan_amnt  = st.number_input("Loan Amount ($)", value=15000, step=500, min_value=1000)
    annual_inc = st.number_input("Annual Income ($)", value=65000, step=1000, min_value=10000)
    int_rate   = st.slider("Interest Rate (%)", 0.0, 30.0, 11.5, step=0.1)
    dti        = st.slider("Debt-To-Income Ratio", 0.0, 50.0, 18.2, step=0.1)

with col2:
    st.markdown('<div class="input-card-title">Credit Profile <span class="tag">HISTORY</span></div>', unsafe_allow_html=True)
    total_acc            = st.number_input("Total Accounts", value=22, step=1, min_value=0)
    mort_acc             = st.number_input("Mortgage Accounts", value=2, step=1, min_value=0)
    pub_rec_bankruptcies = st.number_input("Past Bankruptcies", value=0, step=1, min_value=0)

st.divider()

# ── Predict ───────────────────────────────────────────────────────────────────
if st.button("◈  RUN CREDIT ASSESSMENT", use_container_width=True):

    data = {
        "loan_amnt":            float(loan_amnt),
        "int_rate":             float(int_rate),
        "annual_inc":           float(annual_inc),
        "dti":                  float(dti),
        "total_acc":            int(total_acc),
        "mort_acc":             int(mort_acc),
        "pub_rec_bankruptcies": int(pub_rec_bankruptcies),
    }

    try:
        endpoint_url = f"{API_URL.rstrip('/')}/predict"
        response = requests.post(endpoint_url, json=data, timeout=15)

        if response.status_code != 200:
            st.error(f"API Server Error {response.status_code}: {response.text}")
            st.stop()

        result = response.json()
        prob  = result["default_probability"]
        score = result["credit_score"]
        risk  = result["risk"]
        now   = datetime.now().strftime("%d %B %Y  •  %I:%M %p")

        # ── Banner ───────────────────────────────────────────────────────────
        if risk == "Low":
            b_cls, b_icon, b_title = "low", "🟢", "Low Risk Applicant"
            b_sub = "Strong credit profile — approve with standard terms."
            pill_cls = "pill-low"
            rec = "This applicant demonstrates a strong financial profile with manageable debt levels and solid credit history. Standard loan terms are appropriate. No additional documentation required."
        elif risk == "Medium":
            b_cls, b_icon, b_title = "med", "🟡", "Moderate Risk Applicant"
            b_sub = "Review carefully — consider adjusted terms or additional verification."
            pill_cls = "pill-med"
            rec = "This applicant presents moderate risk indicators. Consider approval with a slightly higher interest rate or reduced loan amount. Request additional income documentation or a co-signer for amounts above $20,000."
        else:
            b_cls, b_icon, b_title = "high", "🔴", "High Risk Applicant"
            b_sub = "Significant default indicators — approval not recommended."
            pill_cls = "pill-high"
            rec = "This applicant presents significant default risk. Loan approval is not recommended under standard terms. If proceeding, require collateral, a co-signer, and a substantially reduced loan amount."

        st.markdown(
            "<div class='result-banner " + b_cls + "'>"
            "<div class='rb-icon'>" + b_icon + "</div>"
            "<div><div class='rb-title'>" + b_title + "</div>"
            "<div class='rb-sub'>" + b_sub + "</div></div>"
            "</div>",
            unsafe_allow_html=True
        )

        # ── Metrics ──────────────────────────────────────────────────────────
        st.markdown('<div class="sec-label">Assessment Results</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Credit Score", score)
        with c2: st.metric("Default Probability", f"{prob * 100:.1f}%")
        with c3: st.metric("Risk Level", risk)

        # ── Charts ───────────────────────────────────────────────────────────
        st.markdown('<div class="sec-label" style="margin-top:28px">Visual Analysis</div>', unsafe_allow_html=True)
        ch1, ch2, ch3 = st.columns(3)

        gauge_color = "#00e5c3" if score >= 750 else ("#ff9f1c" if score >= 650 else "#ff4d6d")

        with ch1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number", value=score,
                title={"text": "CREDIT SCORE", "font": {"color": "#5a6175", "size": 11, "family": "JetBrains Mono"}},
                number={"font": {"color": gauge_color, "size": 40, "family": "Syne"}},
                gauge={
                    "axis": {"range": [300, 850], "tickcolor": "#5a6175", "tickfont": {"color": "#5a6175", "size": 9}, "nticks": 6},
                    "bar": {"color": gauge_color, "thickness": 0.25},
                    "bgcolor": "#0d1018", "bordercolor": "rgba(255,255,255,0.06)",
                    "steps": [
                        {"range": [300, 650], "color": "rgba(255,77,109,0.12)"},
                        {"range": [650, 750], "color": "rgba(255,159,28,0.12)"},
                        {"range": [750, 850], "color": "rgba(0,229,195,0.12)"},
                    ],
                    "threshold": {"line": {"color": gauge_color, "width": 2}, "thickness": 0.8, "value": score}
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(17,20,32,1)",
                font={"color": "#f0f2f8", "family": "Syne"},
                height=230, margin=dict(l=20, r=20, t=50, b=10)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        with ch2:
            safe_pct = round((1 - prob) * 100, 1)
            risk_pct = round(prob * 100, 1)
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(name="Safe", x=[""], y=[safe_pct], marker_color="#00e5c3", marker_line_width=0, width=0.5))
            fig_bar.add_trace(go.Bar(name="Default Risk", x=[""], y=[risk_pct], marker_color="#ff4d6d", marker_line_width=0, width=0.5))
            fig_bar.update_layout(
                barmode="stack",
                title={"text": "DEFAULT PROBABILITY", "font": {"color": "#5a6175", "size": 11, "family": "JetBrains Mono"}, "x": 0.5},
                paper_bgcolor="rgba(17,20,32,1)", plot_bgcolor="rgba(17,20,32,1)",
                font={"color": "#f0f2f8", "family": "Syne"},
                height=230, margin=dict(l=20, r=20, t=50, b=10),
                legend={"font": {"size": 11, "family": "Syne"}, "bgcolor": "rgba(0,0,0,0)", "orientation": "h", "y": -0.15},
                yaxis={"range": [0, 100], "ticksuffix": "%", "gridcolor": "rgba(255,255,255,0.04)", "tickfont": {"color": "#5a6175", "family": "JetBrains Mono"}},
                xaxis={"tickfont": {"color": "#5a6175"}}
            )
            fig_bar.add_annotation(x=0, y=safe_pct + risk_pct/2, text=str(risk_pct)+"%",
                showarrow=False, font={"color": "#fff", "size": 16, "family": "Syne"})
            st.plotly_chart(fig_bar, use_container_width=True)

        with ch3:
            def norm(val, lo, hi):
                return max(0, min(1, (val - lo) / (hi - lo)))
            values_pct = [
                round(norm(annual_inc, 20000, 150000) * 100),
                round(norm(total_acc, 0, 40) * 100),
                round(norm(mort_acc, 0, 5) * 100),
                round((1 - norm(int_rate, 0, 30)) * 100),
                round((1 - norm(dti, 0, 50)) * 100),
                round((1 - norm(pub_rec_bankruptcies, 0, 3)) * 100),
            ]
            categories = ["Income", "Accounts", "Mortgage", "Rate", "DTI", "History"]
            fig_radar = go.Figure(go.Scatterpolar(
                r=values_pct + [values_pct[0]], theta=categories + [categories[0]],
                fill="toself", fillcolor="rgba(200,241,53,0.08)",
                line={"color": "#c8f135", "width": 2}, marker={"color": "#c8f135", "size": 5}
            ))
            fig_radar.update_layout(
                polar={
                    "radialaxis": {"visible": True, "range": [0, 100], "gridcolor": "rgba(255,255,255,0.05)", "tickfont": {"color": "#5a6175", "size": 9, "family": "JetBrains Mono"}},
                    "angularaxis": {"tickfont": {"color": "#8892a4", "size": 10, "family": "Syne"}, "gridcolor": "rgba(255,255,255,0.05)"},
                    "bgcolor": "rgba(13,16,24,1)"
                },
                title={"text": "RISK FACTOR RADAR", "font": {"color": "#5a6175", "size": 11, "family": "JetBrains Mono"}, "x": 0.5},
                paper_bgcolor="rgba(17,20,32,1)", font={"color": "#f0f2f8"},
                height=230, margin=dict(l=30, r=30, t=50, b=10), showlegend=False
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # ── Report ───────────────────────────────────────────────────────────
        bk_color = "#ff4d6d" if pub_rec_bankruptcies > 0 else "#00e5c3"

        def factor_row(label, value, low_t, high_t, bad=True):
            if bad:
                if value <= low_t:    cls, tag, dot = "fi-pos", "LOW",      "#00e5c3"
                elif value <= high_t: cls, tag, dot = "fi-neu", "MODERATE", "#ff9f1c"
                else:                 cls, tag, dot = "fi-neg", "HIGH",     "#ff4d6d"
            else:
                if value >= high_t:   cls, tag, dot = "fi-pos", "STRONG",   "#00e5c3"
                elif value >= low_t:  cls, tag, dot = "fi-neu", "MODERATE", "#ff9f1c"
                else:                 cls, tag, dot = "fi-neg", "WEAK",     "#ff4d6d"
            return (
                "<div class='factor-item'>"
                "<div class='fi-dot' style='background:" + dot + "'></div>"
                "<span class='fi-label'>" + label + "</span>"
                "<span class='fi-val'>" + str(value) + "</span>"
                "<span class='fi-tag " + cls + "'>" + tag + "</span>"
                "</div>"
            )

        factors = (
            factor_row("Interest Rate", int_rate, 10, 20, bad=True) +
            factor_row("Debt-to-Income", dti, 15, 30, bad=True) +
            factor_row("Loan / Income Ratio", round(loan_amnt/annual_inc, 2), 0.2, 0.5, bad=True) +
            factor_row("Total Accounts", total_acc, 10, 20, bad=False) +
            factor_row("Mortgage Accounts", mort_acc, 1, 3, bad=False) +
            factor_row("Past Bankruptcies", pub_rec_bankruptcies, 0, 0, bad=True)
        )

        prob_cls = "good" if prob < 0.2 else ("warn" if prob < 0.5 else "bad")

        report = (
            "<div class='report-wrap'>"

            "<div class='report-head'>"
            "<div>"
            "<div class='report-title'>Credit Risk Assessment</div>"
            "<div class='report-date'>Generated " + now + "</div>"
            "</div>"
            "<span class='score-pill " + pill_cls + "'>" + risk + " Risk</span>"
            "</div>"

            "<div class='report-grid'>"

            "<div class='report-block'>"
            "<div class='report-block-title'>Score Summary</div>"
            "<div class='rrow'><span class='rl'>Credit Score</span><span class='rv'>" + str(score) + " / 850</span></div>"
            "<div class='rrow'><span class='rl'>Default Probability</span><span class='rv " + prob_cls + "'>" + str(round(prob*100,1)) + "%</span></div>"
            "<div class='rrow'><span class='rl'>Risk Band</span><span class='rv'>" + risk + "</span></div>"
            "<div class='rrow'><span class='rl'>Base Score</span><span class='rv'>300</span></div>"
            "<div class='rrow'><span class='rl'>ML Adjustment</span><span class='rv'>+" + str(score-300) + " pts</span></div>"
            "<div class='rrow'><span class='rl'>Formula</span><span class='rv'>300 + (1−" + str(round(prob,3)) + ") × 550</span></div>"
            "</div>"

            "<div class='report-block'>"
            "<div class='report-block-title'>Applicant Data</div>"
            "<div class='rrow'><span class='rl'>Loan Amount</span><span class='rv'>$" + "{:,}".format(int(loan_amnt)) + "</span></div>"
            "<div class='rrow'><span class='rl'>Annual Income</span><span class='rv'>$" + "{:,}".format(int(annual_inc)) + "</span></div>"
            "<div class='rrow'><span class='rl'>Interest Rate</span><span class='rv'>" + str(int_rate) + "%</span></div>"
            "<div class='rrow'><span class='rl'>DTI Ratio</span><span class='rv'>" + str(dti) + "</span></div>"
            "<div class='rrow'><span class='rl'>Total Accounts</span><span class='rv'>" + str(int(total_acc)) + "</span></div>"
            "<div class='rrow'><span class='rl'>Mortgage Accounts</span><span class='rv'>" + str(int(mort_acc)) + "</span></div>"
            "<div class='rrow'><span class='rl'>Bankruptcies</span><span class='rv' style='color:" + bk_color + "'>" + str(int(pub_rec_bankruptcies)) + "</span></div>"
            "</div>"

            "</div>"

            "<div class='report-block' style='margin-bottom:20px'>"
            "<div class='report-block-title'>Factor Analysis</div>"
            + factors +
            "</div>"

            "<div class='rec-box'>"
            "<div class='rec-label'>Recommendation</div>"
            "<div class='rec-text'>" + rec + "</div>"
            "</div>"

            "</div>"
        )

        st.markdown(report, unsafe_allow_html=True)

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the prediction API — make sure your FastAPI server is running and accessible.")