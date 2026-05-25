FONTS = """<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=DM+Sans:wght@400;500&family=JetBrains+Mono&display=swap" rel="stylesheet">"""

CSS = """<style>
/* ── Base & Layout ── */
.stApp { background-color: #0F1117; }
.block-container { padding-top: 1rem !important; max-width: 1200px; }
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent !important; }
.stDeployButton { display: none; }
[data-testid="stIconMaterial"] { color: #EAEAF0 !important; }
[data-testid="stSidebar"] [data-testid="stIconMaterial"] { color: #6C63FF !important; }

/* ── Typography ── */
h1,h2,h3,h4 { font-family: 'Space Grotesk', sans-serif !important; color: #EAEAF0 !important; }
p, label, .stMarkdown { font-family: 'DM Sans', sans-serif; color: #8B8FA8; }
span { font-family: 'DM Sans', sans-serif; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] { background-color: #0D0F1A !important; border-right: 1px solid rgba(255,255,255,0.06) !important; }

/* ── Inputs ── */
.stSelectbox > div > div, .stNumberInput > div > div > input,
.stTextInput > div > div > input { background-color: #22263A !important; color: #EAEAF0 !important;
  border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 8px !important; }
.stSelectbox > div > div:focus-within, .stNumberInput > div > div > input:focus {
  border-color: #6C63FF !important; box-shadow: 0 0 0 2px rgba(108,99,255,0.25) !important; }
[data-baseweb="select"], [data-baseweb="popover"] { background-color: #22263A !important; }
.stSlider > div > div > div > div { background-color: #6C63FF !important; }

/* ── Tabs (pill style) ── */
.stTabs [data-baseweb="tab-list"] { gap: 8px; background: #1A1D27; border-radius: 12px; padding: 4px; }
.stTabs [data-baseweb="tab"] { background: transparent; border-radius: 10px; color: #8B8FA8;
  font-family: 'DM Sans', sans-serif; font-weight: 500; padding: 10px 24px; border: none; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #6C63FF, #00D9C0) !important; color: #fff !important; }
.stTabs [aria-selected="true"] span, .stTabs [aria-selected="true"] p { color: #fff !important; }
.stTabs [aria-selected="false"] span, .stTabs [aria-selected="false"] p { color: #EAEAF0 !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

/* ── Button ── */
.stButton > button { background: linear-gradient(135deg, #6C63FF, #00D9C0) !important; color: #fff !important;
  border: none !important; border-radius: 10px !important; height: 52px !important;
  font-size: 16px !important; font-weight: 600 !important; width: 100% !important;
  font-family: 'DM Sans', sans-serif !important; transition: all 0.3s ease !important; }
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 25px rgba(108,99,255,0.35) !important; }
.stButton > button span, .stButton > button p { color: #fff !important; }

/* ── Cards & Metrics ── */
[data-testid="stMetric"] { background: #1A1D27; border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px; padding: 16px; }
[data-testid="stMetricValue"] { font-family: 'Space Grotesk', sans-serif !important; color: #EAEAF0 !important; }
[data-testid="stMetricLabel"] { font-family: 'DM Sans', sans-serif !important; color: #8B8FA8 !important; }

/* ── Expander ── */
.streamlit-expanderHeader { background: #1A1D27 !important; border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 10px !important; color: #EAEAF0 !important; }
.streamlit-expanderContent { background: #1A1D27 !important; border: 1px solid rgba(255,255,255,0.08) !important;
  border-top: none !important; }

/* ── Radio pills ── */
.stRadio > div { display: flex; flex-direction: column; gap: 8px; }
.stRadio > div > label { background: #1A1D27 !important; border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px; padding: 10px 16px; transition: all 0.2s ease; }
.stRadio > div > label:hover { border-color: #6C63FF; background: #22263A !important; }

/* ── Hover card utility ── */
.hover-card { background: #1A1D27; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px;
  padding: 20px; transition: all 0.2s ease; }
.hover-card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.3); }
.card-accent { border-left: 3px solid #6C63FF !important; }

/* ── Progress bar ── */
.stProgress > div > div > div { border-radius: 10px; }

/* ── Plotly chart containers ── */
.stPlotlyChart { border-radius: 12px; overflow: hidden; }
</style>"""

# Reusable HTML fragments
HEADER_HTML = """
<div style="display:flex; justify-content:space-between; align-items:center; padding:16px 0 12px 0;">
  <div style="display:flex; align-items:center; gap:12px;">
    <span style="font-size:32px;">📊</span>
    <span style="font-family:'Space Grotesk',sans-serif; font-size:28px; font-weight:700; color:#EAEAF0;">ChurnGuard</span>
  </div>
  <span style="font-family:'DM Sans',sans-serif; font-size:12px; color:#8B8FA8; background:#1A1D27;
    padding:6px 14px; border-radius:20px; border:1px solid rgba(255,255,255,0.08);">
    Telco Dataset · 3 Models Active</span>
</div>
<div style="height:2px; background:linear-gradient(90deg,#6C63FF,#00D9C0); margin-bottom:1rem; border-radius:2px;"></div>
"""

FOOTER_HTML = """
<div style="text-align:center; padding:30px 20px 10px; color:#8B8FA8; font-size:12px; font-family:'DM Sans',sans-serif;">
  Built with Streamlit · Customer Churn Prediction · Telco Dataset
</div>
"""

def card_start(title, icon="📋"):
    return f"""<div class="hover-card card-accent" style="margin-bottom:16px;">
    <div style="font-family:'Space Grotesk',sans-serif; font-size:13px; font-weight:700;
      color:#6C63FF; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:14px;">
      {icon} {title}</div>"""

CARD_END = "</div>"
