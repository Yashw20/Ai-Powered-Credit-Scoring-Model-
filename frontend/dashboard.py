"""
AI Credit Scoring — Streamlit Dashboard
Redesigned: editorial light theme, sidebar-driven inputs, tabbed results.
Same prediction parameters and API contract as the original.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

import plotly.graph_objects as go
import requests
import streamlit as st

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
API_TIMEOUT = float(os.getenv("API_TIMEOUT", "15"))

FIELDS = [
    ("loan_amnt", "Loan amount", "USD", 1000.0, 1_000_000.0, 15000.0, 500.0),
    ("annual_inc", "Annual income", "USD", 0.0, 10_000_000.0, 75000.0, 1000.0),
    ("int_rate", "Interest rate", "%", 0.0, 50.0, 12.5, 0.1),
    ("dti", "Debt-to-income", "%", 0.0, 100.0, 18.0, 0.5),
    ("total_acc", "Total credit accounts", "#", 0.0, 200.0, 12.0, 1.0),
    ("mort_acc", "Mortgage accounts", "#", 0.0, 50.0, 1.0, 1.0),
    ("pub_rec_bankruptcies", "Public bankruptcies", "#", 0.0, 20.0, 0.0, 1.0),
]

st.set_page_config(
    page_title="Lumen · Credit Scoring",
    page_icon="◐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Styling — editorial / serif / muted-paper aesthetic (opposite of prior dark)
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,500;9..144,700&family=Inter:wght@400;500;600&display=swap');

:root {
  --paper: #f6f3ec;
  --paper-2: #efeadf;
  --ink: #1c1a17;
  --ink-soft: #4a463f;
  --muted: #8a8478;
  --rule: #d9d3c4;
  --accent: #b4532a;
  --good: #3f7d4e;
  --warn: #c08a2a;
  --bad: #a33a2a;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: var(--paper); color: var(--ink); }

#MainMenu, footer, header { visibility: hidden; }

section[data-testid="stSidebar"] {
  background: var(--paper-2);
  border-right: 1px solid var(--rule);
}
section[data-testid="stSidebar"] * { color: var(--ink) !important; }

h1, h2, h3, .display { font-family: 'Fraunces', serif; font-weight: 500; letter-spacing: -0.01em; color: var(--ink); }

.masthead {
  display:flex; align-items:flex-end; justify-content:space-between;
  border-bottom: 1px solid var(--rule); padding-bottom: 14px; margin-bottom: 28px;
}
.masthead .brand { font-family: 'Fraunces', serif; font-size: 34px; font-weight: 500; letter-spacing: -0.02em; }
.masthead .brand .dot { color: var(--accent); }
.masthead .kicker { font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--muted); }

.pill { display:inline-flex; align-items:center; gap:8px; padding:4px 10px; border:1px solid var(--rule); border-radius: 999px; font-size:12px; color: var(--ink-soft); background: var(--paper); }
.pill .dotled { width:6px; height:6px; border-radius:50%; background: var(--muted); }
.pill.ok .dotled { background: var(--good); }
.pill.err .dotled { background: var(--bad); }

.section-label { font-size: 11px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--muted); margin-bottom: 10px; }

.card {
  background: var(--paper);
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 22px 24px;
}
.card.tinted { background: var(--paper-2); }

.score-hero {
  display:flex; align-items:baseline; gap:18px;
  border-bottom: 1px solid var(--rule); padding-bottom: 18px; margin-bottom: 18px;
}
.score-hero .num { font-family:'Fraunces',serif; font-size: 96px; line-height: 1; font-weight: 500; }
.score-hero .meta { color: var(--ink-soft); }
.score-hero .meta strong { font-weight: 600; }

.verdict { display:inline-block; padding: 6px 12px; border-radius: 2px; font-size: 12px; letter-spacing: 0.14em; text-transform: uppercase; }
.verdict.low { background: rgba(63,125,78,.12); color: var(--good); border: 1px solid rgba(63,125,78,.3); }
.verdict.med { background: rgba(192,138,42,.12); color: var(--warn); border: 1px solid rgba(192,138,42,.3); }
.verdict.high { background: rgba(163,58,42,.12); color: var(--bad); border: 1px solid rgba(163,58,42,.3); }

.kv { display:grid; grid-template-columns: 1fr auto; gap:6px 12px; font-size: 13px; }
.kv .k { color: var(--muted); }
.kv .v { color: var(--ink); font-variant-numeric: tabular-nums; }

.row { display:flex; align-items:center; justify-content:space-between; padding: 10px 0; border-bottom: 1px dashed var(--rule); }
.row:last-child { border-bottom: none; }
.row .lbl { color: var(--ink-soft); font-size: 13px; }
.row .val { font-family:'Fraunces',serif; font-size: 18px; }

.note { font-size: 13px; color: var(--ink-soft); line-height: 1.65; }

.stButton > button {
  background: var(--ink); color: var(--paper); border: none; border-radius: 2px;
  padding: 10px 18px; font-weight: 500; letter-spacing: 0.04em;
}
.stButton > button:hover { background: var(--accent); color: white; }

.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid var(--rule); }
.stTabs [data-baseweb="tab"] { background: transparent; color: var(--muted); font-size: 13px; letter-spacing: 0.08em; text-transform: uppercase; }
.stTabs [aria-selected="true"] { color: var(--ink) !important; border-bottom: 2px solid var(--accent) !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
@st.cache_data(ttl=20)
def check_api() -> tuple[bool, str]:
    try:
        r = requests.get(f"{API_URL}/", timeout=3)
        return (r.status_code < 500, f"{r.status_code}")
    except Exception as e:  # noqa: BLE001
        return (False, type(e).__name__)


def validate(d: dict[str, float]) -> list[str]:
    errs = []
    if d["annual_inc"] > 0 and d["loan_amnt"] > 10 * d["annual_inc"]:
        errs.append("Loan amount exceeds 10× annual income.")
    if d["mort_acc"] > d["total_acc"]:
        errs.append("Mortgage accounts cannot exceed total accounts.")
    if not (0 <= d["int_rate"] <= 50):
        errs.append("Interest rate must be between 0 and 50%.")
    if not (0 <= d["dti"] <= 100):
        errs.append("DTI must be between 0 and 100%.")
    return errs


def call_predict(payload: dict[str, float]) -> dict[str, Any]:
    r = requests.post(f"{API_URL}/predict", json=payload, timeout=API_TIMEOUT)
    r.raise_for_status()
    return r.json()


def risk_class(level: str) -> str:
    l = (level or "").strip().lower()
    if "low" in l: return "low"
    if "high" in l: return "high"
    return "med"


def gauge(score: float) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(score),
        number={"font": {"family": "Fraunces", "size": 38, "color": "#1c1a17"}},
        gauge={
            "axis": {"range": [300, 850], "tickcolor": "#8a8478", "tickfont": {"color": "#8a8478", "size": 11}},
            "bar": {"color": "#1c1a17", "thickness": 0.18},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [300, 580], "color": "rgba(163,58,42,.18)"},
                {"range": [580, 670], "color": "rgba(192,138,42,.18)"},
                {"range": [670, 740], "color": "rgba(63,125,78,.14)"},
                {"range": [740, 850], "color": "rgba(63,125,78,.28)"},
            ],
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=260, margin=dict(l=10, r=10, t=10, b=10),
    )
    return fig


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
ss = st.session_state
ss.setdefault("result", None)
ss.setdefault("inputs", None)
ss.setdefault("error", None)
ss.setdefault("history", [])

# ---------------------------------------------------------------------------
# Sidebar — inputs
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="section-label">Applicant File</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="margin:0 0 14px 0; font-size:22px;">New Assessment</h2>', unsafe_allow_html=True)

    with st.form("applicant_form", clear_on_submit=False):
        values: dict[str, float] = {}
        for key, label, unit, lo, hi, default, step in FIELDS:
            values[key] = st.number_input(
                f"{label} ({unit})",
                min_value=lo, max_value=hi, value=float(default), step=step,
                key=f"in_{key}",
            )
        c1, c2 = st.columns([1, 1])
        submitted = c1.form_submit_button("Score", use_container_width=True)
        reset = c2.form_submit_button("Reset", use_container_width=True)

    if reset:
        for key, *_ in FIELDS:
            ss.pop(f"in_{key}", None)
        ss.result = ss.inputs = ss.error = None
        st.rerun()

    st.markdown("<hr style='border-color:var(--rule); margin: 18px 0;'/>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">API</div>', unsafe_allow_html=True)
    st.text_input("Endpoint", value=API_URL, disabled=True, label_visibility="collapsed")
    ok, info = check_api()
    cls = "ok" if ok else "err"
    st.markdown(f'<span class="pill {cls}"><span class="dotled"></span>{"Online" if ok else "Offline"} · {info}</span>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    f"""
<div class="masthead">
  <div>
    <div class="kicker">Vol. {datetime.now():%Y · %m · %d}</div>
    <div class="brand">Lumen<span class="dot">.</span> Credit Review</div>
  </div>
  <div class="kicker">Underwriting Desk · Confidential</div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Submit handling
# ---------------------------------------------------------------------------
if submitted:
    ss.error = None
    errs = validate(values)
    if errs:
        ss.error = " · ".join(errs)
        ss.result = None
    else:
        try:
            with st.spinner("Scoring applicant…"):
                ss.result = call_predict(values)
                ss.inputs = values
                ss.history.insert(0, {
                    "at": datetime.now().strftime("%H:%M:%S"),
                    "inputs": values, "result": ss.result,
                })
                ss.history = ss.history[:10]
        except requests.ConnectionError:
            ss.error = "Cannot reach the prediction API. Confirm the server is running."
        except requests.Timeout:
            ss.error = f"Request timed out after {API_TIMEOUT}s."
        except requests.HTTPError as e:
            body = ""
            try: body = e.response.text[:300]
            except Exception: pass
            ss.error = f"API returned {e.response.status_code}. {body}"
        except (ValueError, json.JSONDecodeError):
            ss.error = "API returned an invalid JSON response."
        except Exception as e:  # noqa: BLE001
            ss.error = f"Unexpected error: {e}"

if ss.error:
    st.markdown(
        f'<div class="card" style="border-color: rgba(163,58,42,.5); color: var(--bad);">'
        f'<strong>Could not score.</strong> {ss.error}</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Empty state
# ---------------------------------------------------------------------------
if not ss.result:
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown(
            """
<div class="card tinted" style="padding:38px;">
  <div class="kicker" style="color:var(--muted); font-size:11px; letter-spacing:.22em; text-transform:uppercase;">Awaiting File</div>
  <h1 style="font-size:44px; line-height:1.05; margin:10px 0 14px 0;">A quiet, deliberate look at credit risk.</h1>
  <p class="note" style="max-width:52ch;">
    Enter the applicant's particulars in the sidebar and press <em>Score</em>. The desk will return a
    composite score, a risk band, and a short underwriter's note. No data leaves your machine beyond the
    configured API.
  </p>
</div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown('<div class="section-label">Fields Required</div>', unsafe_allow_html=True)
        rows = "".join(
            f'<div class="row"><span class="lbl">{label}</span><span class="val">{unit}</span></div>'
            for _, label, unit, *_ in FIELDS
        )
        st.markdown(f'<div class="card">{rows}</div>', unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
res = ss.result
score = float(res.get("credit_score", res.get("score", 0)))
risk = str(res.get("risk_level", res.get("risk", "Medium")))
recommendation = str(res.get("recommendation", res.get("note", "No recommendation provided.")))
rc = risk_class(risk)

tab_summary, tab_factors, tab_raw, tab_history = st.tabs(["Summary", "Factors", "Raw response", "Session log"])

with tab_summary:
    a, b = st.columns([1.3, 1])
    with a:
        st.markdown(
            f"""
<div class="card">
  <div class="section-label">Composite Score</div>
  <div class="score-hero">
    <div class="num">{int(round(score))}</div>
    <div class="meta">
      out of <strong>850</strong><br/>
      <span class="verdict {rc}">{risk} risk</span>
    </div>
  </div>
  <div class="note">{recommendation}</div>
</div>
            """,
            unsafe_allow_html=True,
        )
    with b:
        st.plotly_chart(gauge(score), use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Applicant Snapshot</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    inp = ss.inputs or {}
    pretty = [
        ("Loan", f"${inp.get('loan_amnt',0):,.0f}"),
        ("Income", f"${inp.get('annual_inc',0):,.0f}"),
        ("Rate", f"{inp.get('int_rate',0):.2f}%"),
        ("DTI", f"{inp.get('dti',0):.1f}%"),
        ("Accounts", f"{int(inp.get('total_acc',0))}"),
        ("Mortgages", f"{int(inp.get('mort_acc',0))}"),
        ("Bankruptcies", f"{int(inp.get('pub_rec_bankruptcies',0))}"),
        ("Loan / Income", f"{(inp.get('loan_amnt',0)/inp.get('annual_inc',1) if inp.get('annual_inc') else 0):.2f}×"),
    ]
    for i, (k, v) in enumerate(pretty):
        with cols[i % 4]:
            st.markdown(
                f'<div class="card" style="padding:14px 16px;">'
                f'<div class="lbl" style="font-size:11px; letter-spacing:.18em; text-transform:uppercase; color:var(--muted);">{k}</div>'
                f'<div class="val" style="font-size:22px; margin-top:6px;">{v}</div></div>',
                unsafe_allow_html=True,
            )

with tab_factors:
    st.markdown('<div class="section-label">Indicative Factor Read</div>', unsafe_allow_html=True)
    inp = ss.inputs or {}
    factors = [
        ("Interest rate", inp.get("int_rate", 0), 8, 18, "lower is better"),
        ("Debt-to-income", inp.get("dti", 0), 15, 35, "lower is better"),
        ("Bankruptcies", inp.get("pub_rec_bankruptcies", 0), 0, 1, "lower is better"),
        ("Mortgage accounts", inp.get("mort_acc", 0), 0, 3, "higher signals stability"),
        ("Total accounts", inp.get("total_acc", 0), 5, 25, "moderate is best"),
    ]
    for name, val, good, bad, hint in factors:
        if good <= bad:
            pct = max(0.0, min(1.0, (float(val) - good) / max(1e-9, (bad - good))))
        else:
            pct = max(0.0, min(1.0, (good - float(val)) / max(1e-9, (good - bad))))
        color = "var(--good)" if pct < 0.34 else "var(--warn)" if pct < 0.67 else "var(--bad)"
        st.markdown(
            f"""
<div class="card" style="margin-bottom:10px;">
  <div style="display:flex; justify-content:space-between; align-items:baseline;">
    <div><strong>{name}</strong> <span class="lbl" style="color:var(--muted); font-size:12px; margin-left:8px;">{hint}</span></div>
    <div class="val">{val}</div>
  </div>
  <div style="height:6px; background:var(--paper-2); border-radius:2px; margin-top:10px; overflow:hidden;">
    <div style="height:100%; width:{pct*100:.0f}%; background:{color};"></div>
  </div>
</div>
            """,
            unsafe_allow_html=True,
        )

with tab_raw:
    st.markdown('<div class="section-label">API Response</div>', unsafe_allow_html=True)
    st.code(json.dumps(res, indent=2), language="json")
    st.download_button(
        "Download JSON",
        data=json.dumps({"inputs": ss.inputs, "result": res, "at": datetime.now().isoformat()}, indent=2),
        file_name=f"credit_score_{datetime.now():%Y%m%d_%H%M%S}.json",
        mime="application/json",
    )

with tab_history:
    if not ss.history:
        st.markdown('<div class="note">No prior runs in this session.</div>', unsafe_allow_html=True)
    else:
        for h in ss.history:
            r = h["result"]; s = float(r.get("credit_score", r.get("score", 0)))
            lv = str(r.get("risk_level", r.get("risk", "—")))
            st.markdown(
                f'<div class="row"><span class="lbl">{h["at"]} · loan ${h["inputs"]["loan_amnt"]:,.0f} · dti {h["inputs"]["dti"]:.1f}%</span>'
                f'<span class="val">{int(round(s))} · <span class="verdict {risk_class(lv)}">{lv}</span></span></div>',
                unsafe_allow_html=True,
            )
