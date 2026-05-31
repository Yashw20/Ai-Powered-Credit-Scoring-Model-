"""
AI Credit Scoring — Streamlit Dashboard
Robust, dynamic UI with validation, error handling, session state,
caching, downloadable report, and graceful API failure modes.
"""

import json
import os
from datetime import datetime
from typing import Any

import plotly.graph_objects as go
import requests
import streamlit as st

# ──────────────────────────────────────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────────────────────────────────────
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
REQUEST_TIMEOUT = int(os.getenv("API_TIMEOUT", "15"))

st.set_page_config(
    page_title="AI Credit Scoring",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────────────────────
# Theme / CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
.stApp{background:linear-gradient(135deg,#0f1117 0%,#12151f 50%,#0d1020 100%);min-height:100vh}
#MainMenu,footer,header{visibility:hidden}

.dash-header{display:flex;align-items:center;gap:16px;margin-bottom:8px}
.dash-icon{width:52px;height:52px;border-radius:14px;background:linear-gradient(135deg,#6c63ff,#00c9a7);display:flex;align-items:center;justify-content:center;font-size:26px}
.dash-title{font-size:28px;font-weight:700;color:#e8eaf6;margin:0}
.dash-subtitle{font-size:14px;color:#8b90a7;margin:2px 0 0}
.glow-bar{height:2px;border-radius:1px;background:linear-gradient(90deg,#6c63ff,#00c9a7);margin:18px 0 28px;opacity:.7}

.api-pill{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:600;letter-spacing:.04em}
.api-ok{background:rgba(0,201,167,.12);color:#00c9a7;border:.5px solid rgba(0,201,167,.4)}
.api-bad{background:rgba(255,107,107,.12);color:#ff6b6b;border:.5px solid rgba(255,107,107,.4)}
.api-unk{background:rgba(139,144,167,.12);color:#8b90a7;border:.5px solid rgba(139,144,167,.4)}

.section-title{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#8b90a7;margin-bottom:18px;display:flex;align-items:center;gap:8px}
.section-title .dot{width:8px;height:8px;border-radius:50%;background:linear-gradient(135deg,#6c63ff,#00c9a7);display:inline-block}

.report-card{background:#1a1d27;border:.5px solid #2a2d3e;border-radius:14px;padding:24px 28px;margin-top:24px}
.report-title{font-size:16px;font-weight:700;color:#e8eaf6;margin-bottom:4px}
.report-subtitle{font-size:12px;color:#8b90a7;margin-bottom:20px}
.report-section{margin-bottom:20px}
.report-section-title{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6c63ff;margin-bottom:10px;border-bottom:.5px solid #2a2d3e;padding-bottom:6px}
.report-row{display:flex;justify-content:space-between;padding:6px 0;font-size:13px;border-bottom:.5px solid #1e2130}
.report-row .label{color:#8b90a7}
.report-row .value{color:#e8eaf6;font-weight:500}
.report-row .value.good{color:#00c9a7}
.report-row .value.warn{color:#ffa94d}
.report-row .value.flag{color:#ff6b6b}

.score-badge{display:inline-block;padding:6px 16px;border-radius:20px;font-size:13px;font-weight:600;margin-top:8px}
.score-low{background:rgba(0,201,167,.15);color:#00c9a7;border:.5px solid rgba(0,201,167,.4)}
.score-med{background:rgba(255,169,77,.15);color:#ffa94d;border:.5px solid rgba(255,169,77,.4)}
.score-high{background:rgba(255,107,107,.15);color:#ff6b6b;border:.5px solid rgba(255,107,107,.4)}

.factor-row{display:flex;align-items:center;gap:10px;padding:7px 0;font-size:13px;border-bottom:.5px solid #1e2130}
.factor-icon{font-size:15px}
.factor-label{color:#8b90a7;flex:1}
.factor-impact{font-weight:500}
.impact-neg{color:#ff6b6b}
.impact-pos{color:#00c9a7}
.impact-neu{color:#ffa94d}

div[data-testid="stNumberInput"] input{background:#12141e!important;border:.5px solid #2a2d3e!important;border-radius:8px!important;color:#e8eaf6!important;font-size:15px!important;font-weight:500!important}
div[data-testid="stNumberInput"] input:focus{border-color:#6c63ff!important;box-shadow:0 0 0 2px rgba(108,99,255,.2)!important}
div[data-testid="stNumberInput"] button{background:#1a1d27!important;border:.5px solid #2a2d3e!important;color:#8b90a7!important;border-radius:6px!important}
div[data-testid="stNumberInput"] button:hover{background:#2a2d3e!important;color:#e8eaf6!important}
label,.stSlider label,.stNumberInput label{color:#8b90a7!important;font-size:12px!important;font-weight:500!important;letter-spacing:.03em!important}
div[data-testid="stSlider"]>div>div>div{background:linear-gradient(90deg,#6c63ff,#00c9a7)!important}
div[data-testid="stSlider"] [data-testid="stThumbValue"]{color:#6c63ff!important;font-weight:600!important}
hr{border-color:#2a2d3e!important;margin:24px 0!important}

div[data-testid="stButton"]>button,div[data-testid="stFormSubmitButton"]>button{background:linear-gradient(135deg,#6c63ff 0%,#845ef7 50%,#00c9a7 100%)!important;color:#fff!important;border:none!important;border-radius:12px!important;font-size:15px!important;font-weight:600!important;padding:14px 0!important;letter-spacing:.04em!important;transition:opacity .15s,transform .12s!important;width:100%!important}
div[data-testid="stButton"]>button:hover,div[data-testid="stFormSubmitButton"]>button:hover{opacity:.88!important;transform:translateY(-1px)!important}
div[data-testid="stDownloadButton"]>button{background:#1a1d27!important;color:#e8eaf6!important;border:.5px solid #2a2d3e!important;border-radius:10px!important;font-weight:500!important}
div[data-testid="stDownloadButton"]>button:hover{border-color:#6c63ff!important;color:#fff!important}

div[data-testid="stMetric"]{background:#12141e!important;border:.5px solid #2a2d3e!important;border-radius:10px!important;padding:16px!important}
div[data-testid="stMetricLabel"]{color:#8b90a7!important;font-size:11px!important;text-transform:uppercase!important;letter-spacing:.06em!important}
div[data-testid="stMetricValue"]{color:#00c9a7!important;font-size:26px!important;font-weight:700!important}
div[data-testid="stAlert"]{border-radius:10px!important;border:.5px solid!important}
h3{color:#e8eaf6!important;font-size:14px!important;font-weight:600!important;letter-spacing:.04em!important;text-transform:uppercase!important}
div[data-testid="stHorizontalBlock"]{gap:20px!important}
</style>
""",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# Session state
# ──────────────────────────────────────────────────────────────────────────────
ss = st.session_state
ss.setdefault("result", None)         # last successful prediction payload
ss.setdefault("inputs", None)         # inputs used for the last prediction
ss.setdefault("history", [])          # list of past predictions (this session)
ss.setdefault("error", None)


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=30, show_spinner=False)
def check_api_health(base_url: str) -> tuple[bool, str]:
    """Lightweight health probe — cached so we don't hammer the API on rerun."""
    base = base_url.rstrip("/")
    for path in ("/health", "/docs", "/"):
        try:
            r = requests.get(base + path, timeout=3)
            if r.status_code < 500:
                return True, f"reachable ({r.status_code})"
        except requests.RequestException:
            continue
    return False, "unreachable"


def validate(inputs: dict[str, float | int]) -> list[str]:
    errors: list[str] = []
    if inputs["loan_amnt"] <= 0:
        errors.append("Loan amount must be greater than 0.")
    if inputs["annual_inc"] <= 0:
        errors.append("Annual income must be greater than 0.")
    if inputs["loan_amnt"] > inputs["annual_inc"] * 10:
        errors.append("Loan amount exceeds 10× annual income — please verify.")
    if inputs["mort_acc"] > inputs["total_acc"]:
        errors.append("Mortgage accounts cannot exceed total accounts.")
    if not 0 <= inputs["int_rate"] <= 50:
        errors.append("Interest rate looks out of range (0–50%).")
    if not 0 <= inputs["dti"] <= 100:
        errors.append("DTI looks out of range (0–100).")
    return errors


def call_predict(inputs: dict[str, Any]) -> dict[str, Any]:
    endpoint = f"{API_URL.rstrip('/')}/predict"
    r = requests.post(endpoint, json=inputs, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    data = r.json()
    for k in ("default_probability", "credit_score", "risk"):
        if k not in data:
            raise ValueError(f"API response missing required field: {k}")
    return data


def risk_styling(risk: str) -> tuple[str, str, str]:
    r = (risk or "").lower()
    if r.startswith("low"):
        return "score-low", "✅", "Low risk applicant — strong credit profile."
    if r.startswith("med") or r.startswith("mod"):
        return "score-med", "⚠️", "Moderate risk applicant — review carefully."
    return "score-high", "❌", "High risk applicant — significant default indicators detected."


def rate_factor(label: str, value, low: float, high: float, higher_is_bad: bool = True) -> str:
    if higher_is_bad:
        if value <= low:
            cls, icon, impact = "impact-pos", "✅", "Low impact"
        elif value <= high:
            cls, icon, impact = "impact-neu", "⚠️", "Moderate impact"
        else:
            cls, icon, impact = "impact-neg", "🔴", "High impact"
    else:
        if value >= high:
            cls, icon, impact = "impact-pos", "✅", "Positive factor"
        elif value >= low:
            cls, icon, impact = "impact-neu", "⚠️", "Moderate factor"
        else:
            cls, icon, impact = "impact-neg", "🔴", "Weak factor"
    return (
        f'<div class="factor-row">'
        f'<span class="factor-icon">{icon}</span>'
        f'<span class="factor-label">{label} — <b style="color:#e8eaf6">{value}</b></span>'
        f'<span class="factor-impact {cls}">{impact}</span>'
        f"</div>"
    )


# ──────────────────────────────────────────────────────────────────────────────
# Header + API status
# ──────────────────────────────────────────────────────────────────────────────
api_ok, api_msg = check_api_health(API_URL)
pill_cls = "api-ok" if api_ok else "api-bad"
pill_dot = "🟢" if api_ok else "🔴"

st.markdown(
    f"""
<div class="dash-header">
  <div class="dash-icon">💳</div>
  <div style="flex:1">
    <p class="dash-title">AI Credit Scoring</p>
    <p class="dash-subtitle">Loan default risk prediction using machine learning</p>
  </div>
  <span class="api-pill {pill_cls}">{pill_dot} API {api_msg}</span>
</div>
<div class="glow-bar"></div>
""",
    unsafe_allow_html=True,
)

if not api_ok:
    st.warning(
        f"Prediction API at `{API_URL}` is not reachable. "
        "Start your FastAPI server or set `API_URL` to the correct endpoint.",
        icon="⚠️",
    )

# ──────────────────────────────────────────────────────────────────────────────
# Input form (one rerun on submit instead of one per keystroke)
# ──────────────────────────────────────────────────────────────────────────────
with st.form("applicant_form", clear_on_submit=False):
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown(
            '<div class="section-title"><span class="dot"></span> Applicant Information</div>',
            unsafe_allow_html=True,
        )
        loan_amnt = st.number_input("Loan Amount ($)", value=15000, step=500, min_value=1000, max_value=1_000_000)
        annual_inc = st.number_input("Annual Income ($)", value=65000, step=1000, min_value=1000, max_value=10_000_000)
        int_rate = st.slider("Interest Rate (%)", 0.0, 30.0, 11.5, step=0.1)
        dti = st.slider("Debt-To-Income Ratio", 0.0, 50.0, 18.2, step=0.1)

    with col2:
        st.markdown(
            '<div class="section-title"><span class="dot"></span> Credit Details</div>',
            unsafe_allow_html=True,
        )
        total_acc = st.number_input("Total Accounts", value=22, step=1, min_value=0, max_value=200)
        mort_acc = st.number_input("Mortgage Accounts", value=2, step=1, min_value=0, max_value=50)
        pub_rec_bankruptcies = st.number_input("Past Bankruptcies", value=0, step=1, min_value=0, max_value=20)

    st.divider()
    btn_col1, btn_col2 = st.columns([3, 1])
    with btn_col1:
        submitted = st.form_submit_button("⚡   Predict Credit Score", use_container_width=True)
    with btn_col2:
        reset = st.form_submit_button("Reset", use_container_width=True)

if reset:
    ss.result = None
    ss.inputs = None
    ss.error = None
    st.rerun()

# ──────────────────────────────────────────────────────────────────────────────
# Submit handling
# ──────────────────────────────────────────────────────────────────────────────
if submitted:
    inputs = {
        "loan_amnt": float(loan_amnt),
        "int_rate": float(int_rate),
        "annual_inc": float(annual_inc),
        "dti": float(dti),
        "total_acc": int(total_acc),
        "mort_acc": int(mort_acc),
        "pub_rec_bankruptcies": int(pub_rec_bankruptcies),
    }
    errs = validate(inputs)
    if errs:
        ss.result = None
        ss.error = "  •  ".join(errs)
    else:
        ss.error = None
        try:
            with st.spinner("Scoring applicant…"):
                ss.result = call_predict(inputs)
                ss.inputs = inputs
                ss.history.append(
                    {
                        "ts": datetime.now().isoformat(timespec="seconds"),
                        "inputs": inputs,
                        "result": ss.result,
                    }
                )
                ss.history = ss.history[-10:]  # keep last 10
        except requests.exceptions.ConnectionError:
            ss.result = None
            ss.error = f"Could not connect to the prediction API at {API_URL}."
        except requests.exceptions.Timeout:
            ss.result = None
            ss.error = f"API timed out after {REQUEST_TIMEOUT}s. Try again."
        except requests.exceptions.HTTPError as e:
            ss.result = None
            body = ""
            try:
                body = e.response.text[:300] if e.response is not None else ""
            except Exception:
                pass
            ss.error = f"API error {e.response.status_code if e.response else ''}: {body or str(e)}"
        except (ValueError, json.JSONDecodeError) as e:
            ss.result = None
            ss.error = f"Invalid API response: {e}"

if ss.error:
    st.error(ss.error)

# ──────────────────────────────────────────────────────────────────────────────
# Results
# ──────────────────────────────────────────────────────────────────────────────
if ss.result and ss.inputs:
    result = ss.result
    inp = ss.inputs

    prob = float(result["default_probability"])
    score = int(result["credit_score"])
    risk = str(result["risk"])
    badge_cls, badge_icon, recommendation = risk_styling(risk)

    st.markdown(
        '<div class="section-title" style="margin-top:8px"><span class="dot"></span> Prediction Results</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Default Probability", f"{prob * 100:.1f}%")
    c2.metric("Credit Score", f"{score}")
    c3.metric("Risk Level", risk)

    {"Low": st.success, "Medium": st.warning}.get(risk, st.error)(
        f"{badge_icon}  {recommendation}"
    )

    # Charts
    ch1, ch2, ch3 = st.columns(3)

    with ch1:
        gauge_color = "#00c9a7" if score >= 750 else ("#ffa94d" if score >= 650 else "#ff6b6b")
        fig = go.Figure(
            go.Indicator(
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
                    "threshold": {"line": {"color": gauge_color, "width": 3}, "thickness": 0.75, "value": score},
                },
            )
        )
        fig.update_layout(
            paper_bgcolor="rgba(26,29,39,1)", plot_bgcolor="rgba(26,29,39,1)",
            font={"color": "#e8eaf6"}, height=220, margin=dict(l=20, r=20, t=40, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    with ch2:
        safe_pct = round((1 - prob) * 100, 1)
        risk_pct = round(prob * 100, 1)
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Safe", x=["Probability"], y=[safe_pct], marker_color="#00c9a7", width=0.4))
        fig.add_trace(go.Bar(name="Default Risk", x=["Probability"], y=[risk_pct], marker_color="#ff6b6b", width=0.4))
        fig.update_layout(
            barmode="stack",
            title={"text": "Default Probability", "font": {"color": "#8b90a7", "size": 13}, "x": 0.5},
            paper_bgcolor="rgba(26,29,39,1)", plot_bgcolor="rgba(26,29,39,1)",
            font={"color": "#e8eaf6"}, height=220, margin=dict(l=20, r=20, t=40, b=10),
            legend={"font": {"size": 11}, "bgcolor": "rgba(0,0,0,0)"},
            yaxis={"range": [0, 100], "ticksuffix": "%", "gridcolor": "#2a2d3e", "tickfont": {"color": "#8b90a7"}},
            xaxis={"tickfont": {"color": "#8b90a7"}},
        )
        fig.add_annotation(x=0, y=risk_pct / 2, text=f"{risk_pct}%", showarrow=False,
                           font={"color": "#fff", "size": 14, "family": "Arial Black"})
        st.plotly_chart(fig, use_container_width=True)

    with ch3:
        def norm(v, lo, hi):
            return max(0.0, min(1.0, (v - lo) / (hi - lo)))

        vals = [
            norm(inp["annual_inc"], 20000, 150000),
            norm(inp["total_acc"], 0, 40),
            norm(inp["mort_acc"], 0, 5),
            1 - norm(inp["int_rate"], 0, 30),
            1 - norm(inp["dti"], 0, 50),
            1 - norm(inp["pub_rec_bankruptcies"], 0, 3),
        ]
        cats = ["Income", "Accounts", "Mortgage", "Low Rate", "Low DTI", "No Bankrupt"]
        pct = [round(v * 100) for v in vals]
        fig = go.Figure(
            go.Scatterpolar(
                r=pct + [pct[0]], theta=cats + [cats[0]], fill="toself",
                fillcolor="rgba(108,99,255,0.2)",
                line={"color": "#6c63ff", "width": 2},
                marker={"color": "#6c63ff", "size": 5},
            )
        )
        fig.update_layout(
            polar={
                "radialaxis": {"visible": True, "range": [0, 100], "gridcolor": "#2a2d3e",
                               "tickfont": {"color": "#8b90a7", "size": 9}},
                "angularaxis": {"tickfont": {"color": "#8b90a7", "size": 10}, "gridcolor": "#2a2d3e"},
                "bgcolor": "rgba(18,20,30,1)",
            },
            title={"text": "Risk Factor Radar", "font": {"color": "#8b90a7", "size": 13}, "x": 0.5},
            paper_bgcolor="rgba(26,29,39,1)", font={"color": "#e8eaf6"},
            height=220, margin=dict(l=30, r=30, t=40, b=10), showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Report ────────────────────────────────────────────────────────────────
    now = datetime.now().strftime("%d %B %Y, %I:%M %p")
    bk_color = "#ff6b6b" if inp["pub_rec_bankruptcies"] > 0 else "#00c9a7"
    lti = round(inp["loan_amnt"] / inp["annual_inc"], 2) if inp["annual_inc"] else 0

    factors_html = (
        rate_factor("Interest Rate", inp["int_rate"], 10, 20, True)
        + rate_factor("Debt-to-Income Ratio", inp["dti"], 15, 30, True)
        + rate_factor("Loan-to-Income Ratio", lti, 0.2, 0.5, True)
        + rate_factor("Total Accounts", inp["total_acc"], 10, 20, False)
        + rate_factor("Mortgage Accounts", inp["mort_acc"], 1, 3, False)
        + rate_factor("Past Bankruptcies", inp["pub_rec_bankruptcies"], 0, 0, True)
    )

    report_html = f"""
<div class="report-card">
  <div class="report-title">📋 Credit Risk Report</div>
  <div class="report-subtitle">Generated on {now}</div>

  <div class="report-section">
    <div class="report-section-title">Summary</div>
    <div class="report-row"><span class="label">Credit Score</span><span class="value">{score} / 850</span></div>
    <div class="report-row"><span class="label">Default Probability</span><span class="value">{round(prob*100,1)}%</span></div>
    <div class="report-row"><span class="label">Risk Classification</span>
      <span class="score-badge {badge_cls}">{badge_icon} {risk} Risk</span></div>
  </div>

  <div class="report-section">
    <div class="report-section-title">Applicant Data</div>
    <div class="report-row"><span class="label">Loan Amount</span><span class="value">${inp['loan_amnt']:,.0f}</span></div>
    <div class="report-row"><span class="label">Annual Income</span><span class="value">${inp['annual_inc']:,.0f}</span></div>
    <div class="report-row"><span class="label">Interest Rate</span><span class="value">{inp['int_rate']}%</span></div>
    <div class="report-row"><span class="label">Debt-to-Income Ratio</span><span class="value">{inp['dti']}</span></div>
    <div class="report-row"><span class="label">Total Accounts</span><span class="value">{inp['total_acc']}</span></div>
    <div class="report-row"><span class="label">Mortgage Accounts</span><span class="value">{inp['mort_acc']}</span></div>
    <div class="report-row"><span class="label">Past Bankruptcies</span>
      <span class="value" style="color:{bk_color}">{inp['pub_rec_bankruptcies']}</span></div>
  </div>

  <div class="report-section">
    <div class="report-section-title">Factor Analysis</div>
    {factors_html}
  </div>

  <div class="report-section">
    <div class="report-section-title">How the Score was Calculated</div>
    <div class="report-row"><span class="label">Base Score</span><span class="value">300</span></div>
    <div class="report-row"><span class="label">ML Model Adjustment</span><span class="value">+{score-300} pts (default prob {round(prob*100,1)}%)</span></div>
    <div class="report-row"><span class="label">Formula</span><span class="value">300 + (1 - {round(prob,3)}) x 550</span></div>
    <div class="report-row"><span class="label">Final Score</span><span class="value good">{score}</span></div>
  </div>

  <div class="report-section" style="margin-bottom:0">
    <div class="report-section-title">Recommendation</div>
    <p style="color:#c8cad8;font-size:13px;line-height:1.6;margin:0">{recommendation}</p>
  </div>
</div>
"""
    st.markdown(report_html, unsafe_allow_html=True)

    # Downloads
    dl1, dl2 = st.columns(2)
    payload = {"generated_at": now, "inputs": inp, "result": result}
    dl1.download_button(
        "⬇️  Download JSON",
        data=json.dumps(payload, indent=2),
        file_name=f"credit_report_{datetime.now():%Y%m%d_%H%M%S}.json",
        mime="application/json",
        use_container_width=True,
    )
    dl2.download_button(
        "⬇️  Download HTML report",
        data=f"<html><head><meta charset='utf-8'><title>Credit Report</title></head><body style='background:#0f1117;padding:24px'>{report_html}</body></html>",
        file_name=f"credit_report_{datetime.now():%Y%m%d_%H%M%S}.html",
        mime="text/html",
        use_container_width=True,
    )

    # History
    if len(ss.history) > 1:
        with st.expander(f"Session history ({len(ss.history)} predictions)"):
            for i, h in enumerate(reversed(ss.history), 1):
                r = h["result"]
                st.markdown(
                    f"**{i}.** `{h['ts']}` — score **{r.get('credit_score','?')}**, "
                    f"risk **{r.get('risk','?')}**, "
                    f"prob **{float(r.get('default_probability',0))*100:.1f}%**"
                )
else:
    if not ss.error:
        st.info("Enter applicant details above and click **Predict Credit Score** to generate a report.", icon="💡")
