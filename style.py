import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Spectral:wght@500;600&display=swap');

:root {
  --ink: #16181A; --muted: #6B7280; --line: #E4E1DA; --paper: #FFFFFF; --bg: #FBFAF7;
  --teal: #14564F; --teal-06: rgba(20, 86, 79, 0.06); --teal-12: rgba(20, 86, 79, 0.12);
  --terracotta: #9A4A32;
}

html, body, .stApp, .stMarkdown, p, li, label, input, textarea, button, .stDataFrame {
  font-family: 'Inter', sans-serif;
}
.stApp { background: var(--bg); color: var(--ink); }
.stMarkdown p, .stMarkdown li { line-height: 1.65; }

h1, h2, h3, h4, .tb-serif {
  font-family: 'Spectral', Georgia, serif !important;
  font-weight: 500 !important; color: var(--ink); letter-spacing: -0.01em;
}
h1 { font-size: 2.1rem !important; }
h2 { font-size: 1.45rem !important; }
h3 { font-size: 1.15rem !important; }

/* Bordered containers look like sheets of paper */
[data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stVerticalBlock"][class*="border"] {
  background: var(--paper); border-color: var(--line) !important; border-radius: 4px; box-shadow: none;
}

[data-testid="stSidebar"] { border-right: 1px solid var(--line); }
[data-testid="stSidebar"] .tb-brand { font-family: 'Spectral', serif; font-size: 1.5rem; color: var(--ink); }

.stButton button, .stDownloadButton button, .stFormSubmitButton button { border-radius: 4px; font-weight: 500; }

/* Small text helpers */
.tb-muted { color: var(--muted); font-size: 0.88rem; }
.tb-label { color: var(--muted); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }
.tb-overdue { color: var(--terracotta); font-weight: 500; }
.tb-notice { color: var(--muted); font-size: 0.82rem; font-style: italic; }

/* Score badge: the number carries the meaning */
.tb-score { display: inline-block; min-width: 2.6rem; text-align: center; padding: 0.1rem 0.5rem;
  border-radius: 4px; font-weight: 600; font-variant-numeric: tabular-nums; font-size: 0.9rem; }
.tb-score.high { background: var(--teal-12); color: var(--teal); }
.tb-score.mid { border: 1px solid var(--line); color: var(--muted); }
.tb-score.low { color: var(--muted); }

.tb-tag { display: inline-block; background: var(--teal-06); color: var(--teal); border-radius: 4px;
  padding: 0.05rem 0.45rem; margin: 0 0.25rem 0.25rem 0; font-size: 0.78rem; }
.tb-status { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); font-weight: 600; }

.tb-col-head { border-left: 2px solid transparent; padding-left: 0.6rem; margin-bottom: 0.6rem; }
.tb-col-head.active { border-left-color: var(--teal); }

/* Maturity scale */
.tb-scale { display: flex; gap: 4px; margin: 0.2rem 0 0.4rem 0; }
.tb-scale div { flex: 1; height: 8px; border-radius: 2px; background: var(--line); }
.tb-scale div.in { background: var(--teal-12); box-shadow: inset 0 0 0 1px var(--teal); }
.tb-scale div.at { background: var(--teal); }

.tb-progress { height: 8px; border-radius: 2px; background: var(--line); overflow: hidden; }
.tb-progress div { height: 100%; background: var(--teal); }
.tb-progress.full div { background: var(--terracotta); }

.tb-hero { padding: 2.5rem 0 1rem 0; max-width: 46rem; }
.tb-hero h1 { font-size: 2.8rem !important; line-height: 1.15; }
.tb-hero p { font-size: 1.1rem; color: var(--muted); }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)
