import streamlit as st

# Two themes, one stylesheet. Every colour is a CSS variable; a theme is just a different set of values.
#   warm  : Forest Exhale (light): Deep Teal #0F3F3F, Celadon #B6D298, Beige #DCE2C8
#   azure : Dark Azure #00638E, Light Azure #BFD8E3, Paper White, Onyx #000 / #141414, Charcoal #2B2B2B,
#           branding gradient #000000 > #004A6B > #00638E > #8CB9CC (dark)
# Principle: calm. One focus per screen, quiet surfaces, one accent colour for what matters.

THEMES = {
    "warm": """
:root {
  /* Forest Exhale: Deep Teal #0F3F3F, Celadon #B6D298, Beige #DCE2C8 (+ tints of them). No orange anywhere. */
  --accent: #0F3F3F; --accent-deep: #0A2E2E; --accent-soft: rgba(182,210,152,0.50); --accent-2: #5F8F45; --accent-ink: #0F3F3F; --on-accent: #FFFFFF; --alert: #0F3F3F;
  --canvas: #EEF1E0; --surface: #FFFFFF; --surface-2: #F3F6E8; --surface-3: #E6EBD6; --border: #D9E0C4; --border-2: #BFC9A6;
  --text: #0F2E2E; --text-2: #2B4743; --muted: #4A625C;
  --strong: #0F3F3F; --on-strong: #FFFFFF; --dock-text: rgba(255,255,255,0.88); --dock-hover: rgba(255,255,255,0.12); --dock-border: transparent;
  --seg-active: #0F3F3F; --seg-active-text: #FFFFFF;
  --hi-bg: linear-gradient(135deg, #0F3F3F, #1E5A50); --hi-text: #FFFFFF; --hi-sub: rgba(255,255,255,0.78); --hi-unit: #B6D298;
  --hero-bg: radial-gradient(34rem 24rem at 0% 115%, #B6D298 0%, rgba(182,210,152,0.55) 40%, transparent 72%), linear-gradient(180deg, #DCE2C8 0%, #E6EBD6 100%);
  --hero-text: #0F3F3F; --hero-sub: #2B4743; --hero-pill: rgba(255,255,255,0.6); --hero-pill-text: #0F3F3F;
  --shadow: 0 1px 2px rgba(15,63,63,0.06), 0 6px 18px rgba(15,63,63,0.06);
  --shadow-hover: 0 2px 4px rgba(15,63,63,0.08), 0 12px 28px rgba(15,63,63,0.12);
  --menu-shadow: 0 16px 40px rgba(15,63,63,0.18);
  --canvas-bg: radial-gradient(38rem 30rem at 6% 8%, rgba(182,210,152,0.85), transparent 62%), radial-gradient(34rem 28rem at 96% 8%, rgba(220,226,200,0.95), transparent 60%), radial-gradient(40rem 32rem at 84% 96%, rgba(150,190,150,0.55), transparent 62%), radial-gradient(34rem 28rem at 2% 94%, rgba(200,218,180,0.85), transparent 60%), linear-gradient(135deg, #F1F4E4 0%, #E4EBD2 50%, #DCE2C8 100%);
  --glass-a: rgba(251,253,246,0.92); --glass-b: rgba(244,248,234,0.80); --glass-rim: rgba(255,255,255,0.9); --glass-hi: rgba(255,255,255,0.95);
  --ph-fade-a: rgba(247,250,238,0.55); --ph-fade-b: rgba(247,250,238,0.92); --ph-solid: #F7FAEE; --ph-tint: linear-gradient(rgba(255,255,255,0),rgba(255,255,255,0)); --btn-bg: #FFFFFF; --btn-grad: linear-gradient(180deg, #FFFFFF 0%, #EEF2E2 100%); --btn-grad-h: linear-gradient(180deg, #FFFFFF 0%, #E4EBD2 100%); --pbtn-grad: linear-gradient(180deg, #1B5757 0%, #0F3F3F 55%, #0A3232 100%); --pbtn-grad-h: linear-gradient(180deg, #226464 0%, #134949 55%, #0D3A3A 100%); --row-bg: #EDF1DF; --lg-top: rgba(255,255,255,0.95); --lg-bot: rgba(255,255,255,1); --lg-glow: rgba(255,255,255,0.55); --lg-drop: rgba(15,63,63,0.16);
  --dock-bg: rgba(15,63,63,0.96); --dock-act: #B6D298; --dock-act-text: #0F3F3F; --pbtn-bg: #0F3F3F; --pbtn-text: #FFFFFF; --pbtn-hover: #0A2E2E;
  --art-sky-top: #DCE2C8; --art-sky-bottom: #B6D298; --art-glow: #F1F4E4; --art-ridge: #86A88A; --art-lit: #9DBB86; --art-shade: #2F6A55; --art-snow: #FFFFFF; --art-cloud: #FFFFFF; --art-star: #FFFFFF; --art-sun: #F1F4E4; --art-tower: #DCE2C8; --art-h1: #86A88A; --art-h2: #3F7A62; --art-h3: #0F3F3F;
  --sc-sky-top: #DCE2C8; --sc-sky-mid: #C9DDB0; --sc-sky-bottom: #B6D298; --sc-sun: #F1F4E4; --sc-mist: #EEF3E0; --sc-cloud: #FFFFFF; --sc-m1: #A9C59B; --sc-m2: #86A88A; --sc-cliff-hi: #2F6A55; --sc-cliff: #0F3F3F; --sc-fol1: #14473F; --sc-fol2: #1E5A50; --sc-fol3: #2F6A55; --sc-lit: #B6D298; --sc-fig: #0A2E2E;
  --h-dark: #0F3F3F; --h-g1: #1E5A50; --h-g2: #4A7F3A; --h-sub: #1F3F3A; --peek-bg: rgba(15,63,63,0.66); --home-filter: none; --home-tint: rgba(110,150,125,0.55); --home-blend: color;
  --band-bg: #0F3F3F; --band-glow: radial-gradient(42rem 18rem at 18% -12%, rgba(182,210,152,0.34), transparent 62%), radial-gradient(34rem 16rem at 90% 0%, rgba(220,226,200,0.16), transparent 60%); --on-scene: #FFFFFF; --scene-glass: rgba(255,255,255,0.55);
  --poster-bg: #0F3F3F; --poster-text: #F1F4E4; --photo-tint: #4F7F66; --pin-hi: #B6D298;
  --bm-hi: linear-gradient(105deg, #0A2E2E 0%, #1E5A50 60%, #4D8A5E 100%); --bm-mid: linear-gradient(105deg, #14383A 0%, #2E6B63 60%, #5E9A8A 100%); --bm-lo: linear-gradient(105deg, #14201F 0%, #26362F 70%, #3A4D43 100%);
}
""",
    "azure": """
:root {
  --accent: #2559E0; --accent-deep: #1A47C0; --accent-ink: #A9C4FF; --accent-soft: rgba(47,107,255,0.28); --accent-2: #8FB1FF; --on-accent: #FFFFFF; --alert: #C9DAFF; --dock-act: #2559E0; --dock-act-text: #FFFFFF; --photo-tint: #3560D8; --pin-hi: #4C86FF; --home-blend: normal;
  --bm-hi: linear-gradient(105deg, #12307A 0%, #2559E0 60%, #4C86FF 100%); --bm-mid: linear-gradient(105deg, #0F2250 0%, #27428F 60%, #5B7FD0 100%); --bm-lo: linear-gradient(105deg, #0E1630 0%, #1D2B52 70%, #2D3E70 100%);
  --canvas: #070D22;
  --canvas-bg: radial-gradient(38rem 30rem at 8% 6%, rgba(70,110,230,0.55), transparent 62%), radial-gradient(34rem 28rem at 96% 10%, rgba(120,100,230,0.40), transparent 60%), radial-gradient(40rem 32rem at 80% 96%, rgba(60,110,220,0.45), transparent 62%), linear-gradient(160deg, #070D22 0%, #0C1838 55%, #13265A 100%);
  --surface: #121F45; --surface-2: #1A2A58; --surface-3: #22346C; --border: rgba(165,190,255,0.22); --border-2: rgba(165,190,255,0.36);
  --text: #FFFFFF; --text-2: #DDE7FF; --muted: rgba(221,231,255,0.78);
  --strong: #1A2A58; --on-strong: #FFFFFF; --dock-text: rgba(255,255,255,0.88); --dock-hover: rgba(255,255,255,0.10); --dock-border: rgba(165,190,255,0.30);
  --seg-active: #2F6BFF; --seg-active-text: #FFFFFF;
  --glass-a: rgba(16,30,74,0.90); --glass-b: rgba(14,26,66,0.78); --ph-fade-a: rgba(16,30,74,0.55); --ph-fade-b: rgba(16,30,74,0.93); --ph-solid: #10204A; --ph-tint: linear-gradient(rgba(10,26,80,0.35),rgba(10,26,80,0.35)); --btn-bg: #1C2E66; --btn-grad: linear-gradient(180deg, #274088 0%, #1C2E66 100%); --btn-grad-h: linear-gradient(180deg, #2F4A9C 0%, #213673 100%); --pbtn-grad: linear-gradient(180deg, #3B74F0 0%, #2559E0 55%, #1D49C0 100%); --pbtn-grad-h: linear-gradient(180deg, #4A82FF 0%, #2B63EE 55%, #2250CC 100%); --row-bg: #1E3272; --lg-top: rgba(150,185,255,0.45); --lg-bot: rgba(205,222,255,0.70); --lg-glow: rgba(120,160,255,0.16); --lg-drop: rgba(0,4,24,0.55); --dock-bg: rgba(8,16,44,0.94); --glass-rim: rgba(170,195,255,0.35); --glass-hi: rgba(200,218,255,0.45); --pbtn-bg: #2559E0; --pbtn-text: #FFFFFF; --pbtn-hover: #1D49C0; --lime: #B6D298;
  --hi-bg: linear-gradient(135deg, #2F6BFF 0%, #1A3FB8 100%); --hi-text: #FFFFFF; --hi-sub: rgba(255,255,255,0.84); --hi-unit: #D3E1FF;
  --hero-bg: linear-gradient(135deg, #060C22, #1B46C8); --hero-text: #FFFFFF; --hero-sub: rgba(255,255,255,0.84); --hero-pill: rgba(255,255,255,0.14); --hero-pill-text: #FFFFFF;
  --shadow: 0 1px 2px rgba(0,0,0,0.35), 0 10px 28px rgba(2,6,24,0.45);
  --shadow-hover: 0 2px 4px rgba(0,0,0,0.45), 0 16px 36px rgba(2,6,24,0.6);
  --menu-shadow: 0 16px 40px rgba(2,6,24,0.7);
  --sc-sky-top: #050B24; --sc-sky-mid: #10308C; --sc-sky-bottom: #5C86E0; --sc-sun: #9DBBFF; --sc-mist: #7FA3EE; --sc-cloud: #C9D8FF;
  --sc-m1: #3A63C8; --sc-m2: #20409A; --sc-cliff-hi: #0F1E4A; --sc-cliff: #050B1E; --sc-fol1: #0A1740; --sc-fol2: #132760; --sc-fol3: #1E3A86; --sc-lit: #8FB1FF; --sc-fig: #FFFFFF;
  --h-dark: #FFFFFF; --h-g1: #E3ECFF; --h-g2: #BCD0FF; --peek-bg: rgba(10,18,48,0.66); --band-bg: #050A1E; --band-glow: radial-gradient(42rem 18rem at 20% -12%, rgba(47,107,255,0.45), transparent 62%), radial-gradient(34rem 16rem at 88% 0%, rgba(120,90,220,0.28), transparent 60%);
  --home-filter: saturate(0.55) brightness(0.62) contrast(1.05); --home-tint: linear-gradient(180deg, rgba(6,14,60,0.66) 0%, rgba(24,60,170,0.44) 55%, rgba(8,18,60,0.62) 100%); --h-sub: rgba(255,255,255,0.86); --on-scene: #FFFFFF; --scene-glass: rgba(14,26,62,0.58);
  --art-sky-top: #0B1E6B; --art-sky-bottom: #6E97F0; --art-glow: #BFD3FF; --art-ridge: #1C3A96; --art-lit: #4C79E0; --art-shade: #1B3688; --art-snow: #FFFFFF; --art-cloud: #EEF3FF; --art-star: #FFFFFF;
}
""",
}

# Native Streamlit widgets take their colours from the Streamlit theme (light). In the dark theme they have to be told.
DARK_OVERRIDES = """
/* blue theme: photos are re-toned to a blue monochrome (luminosity of the photo, hue of the blue) so no orange survives */
.tb-photo, .tb-bm-img { background-color: #3560D8; background-blend-mode: luminosity; }

/* Streamlit paints its own widgets with the (orange) config primary colour; in the blue theme re-hue them to the blue accent */
[data-testid="stCheckbox"], [data-testid="stRadio"], [data-testid="stSlider"], [data-testid="stToggle"], [data-testid="stDateInput"] [data-baseweb] { filter: hue-rotate(42deg) saturate(1.7) brightness(2.7); }
[data-testid="stCheckbox"] p, [data-testid="stRadio"] p, [data-testid="stSlider"] p { filter: none; }
[data-baseweb="tab-highlight"] { background-color: var(--accent) !important; display: block !important; height: 2px !important; }
.stApp a { color: var(--accent-2) !important; }
.stApp [data-baseweb="input"]:focus-within, .stApp [data-baseweb="textarea"]:focus-within, .stApp [data-baseweb="select"] > div:focus-within { border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-soft) !important; }
.tb-overdue { color: var(--alert) !important; text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 3px; }

.stApp, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp li, .stApp label, .stApp summary,
.stApp [data-testid="stWidgetLabel"] p, .stApp [data-testid="stMarkdownContainer"] p { color: var(--text) !important; }
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea, [data-baseweb="select"] div, [data-baseweb="select"] span,
[data-baseweb="menu"] li, [data-baseweb="menu"] div, [data-baseweb="popover"] div { color: var(--text) !important; }
[data-baseweb="input"] input::placeholder, [data-baseweb="textarea"] textarea::placeholder { color: var(--muted) !important; }
[data-baseweb="select"] svg, [data-baseweb="input"] svg { fill: var(--text-2) !important; }
[data-baseweb="select"] > div, [data-baseweb="select"] > div > div, [data-baseweb="input"] > div { background: var(--surface-2) !important; }
[data-testid="stDataFrame"] { filter: invert(0.92) hue-rotate(180deg); }
[data-baseweb="menu"] li:hover, [data-baseweb="menu"] [aria-selected="true"] { background: rgba(255,255,255,0.10) !important; }
"""

CSS = """
<style>
:root { --radius: 20px; --radius-sm: 12px; }

/* Apple system font (SF Pro on Apple devices). Icon fonts excluded so Streamlit's Material icons keep working. */
:root { --font: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", system-ui, "Helvetica Neue", Arial, sans-serif; }
html, body, .stApp, .stApp *:not([data-testid="stIconMaterial"]):not(.material-icons):not([class*="material-symbols"]),
.stApp svg text, [data-baseweb] *, [data-baseweb="popover"] * { font-family: var(--font) !important; }
.stApp [data-testid="stIconMaterial"], .stApp .material-icons, .stApp [class*="material-symbols"] { font-family: "Material Symbols Rounded", "Material Icons" !important; }
.stApp { background: var(--canvas-bg) !important; background-attachment: fixed !important; color: var(--text); -webkit-font-smoothing: antialiased; }
.stMarkdown p, .stMarkdown li { line-height: 1.55; }
.block-container { max-width: 62rem; padding-top: 6rem !important; padding-bottom: 7rem !important; }

h1, h2, h3, h4, .tb-serif { font-weight: 600 !important; color: var(--text); letter-spacing: -0.03em; line-height: 1.12; }
h1 { font-size: 2.2rem !important; font-weight: 700 !important; letter-spacing: -0.04em; }
h2 { font-size: 1.5rem !important; }
h3 { font-size: 1.1rem !important; letter-spacing: -0.02em; }
[data-testid="stCaptionContainer"] { color: var(--muted); }
[data-testid="stHeaderActionElements"] { display: none; }
[data-testid="stHeader"] { background: transparent; }

/* ---------- Shell ---------- */
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] { display: none !important; }
.st-key-topbar, .st-key-bottomnav { position: fixed; left: 50%; transform: translateX(-50%); z-index: 990; border-radius: 999px; }
.st-key-topbar { top: 0.9rem; width: min(94vw, 62rem); padding: 0.4rem 1rem; background: var(--surface); border: 1px solid var(--border); box-shadow: var(--shadow); }
.st-key-bottomnav { bottom: 1.1rem; width: min(92vw, 36rem); padding: 0.35rem 0.45rem; background: var(--strong); border: 1px solid var(--dock-border); box-shadow: 0 10px 30px rgba(0,0,0,0.28); }
.st-key-topbar [data-testid="stHorizontalBlock"], .st-key-bottomnav [data-testid="stHorizontalBlock"] { align-items: center; flex-wrap: nowrap; }
.st-key-topbar [data-testid="stMarkdownContainer"] p, .st-key-topbar [data-testid="stMarkdownContainer"] { margin: 0 !important; }
.st-key-topbar [data-testid="stElementContainer"] { display: flex; align-items: center; width: 100%; }
.st-key-topbar [data-testid="stElementContainer"] > [data-testid="stMarkdown"], .st-key-topbar [data-testid="stMarkdownContainer"] { width: 100%; }
.tb-who { display: flex; align-items: center; gap: 0.65rem; height: 2.4rem; }
.tb-av2 { width: 2.3rem; height: 2.3rem; border-radius: 50%; background: var(--accent); color: var(--on-accent); display: flex; align-items: center; justify-content: center; font-weight: 600; }
.tb-wl { font-size: 0.68rem; color: var(--muted); line-height: 1; }
.tb-wn { font-size: 0.98rem; font-weight: 600; letter-spacing: -0.02em; line-height: 1.25; }
.tb-topc { display: flex; align-items: center; justify-content: center; width: 100%; height: 2.4rem; text-align: center; }
.tb-topc b { display: inline-flex; align-items: center; gap: 0.25rem; font-size: 1.25rem; line-height: 1; font-weight: 700; letter-spacing: -0.04em; color: var(--text); }
.tb-topc b::after { content: ''; width: 0.42rem; height: 0.42rem; border-radius: 50%; background: var(--accent-2); margin-top: 0.35rem; }
[data-testid="stPopover"] { display: flex; justify-content: flex-end; }
.st-key-topbar [data-testid="stButtonGroup"] { margin-left: auto; }
[data-testid="stPopover"] button, .st-key-themebtn button { border-radius: 999px; background: var(--surface-2); border: 1px solid var(--border); padding: 0.4rem 0.6rem; color: var(--text); }
.st-key-themebtn button { width: 2.4rem; height: 2.4rem; padding: 0; display: flex; align-items: center; justify-content: center; margin-left: auto; }
.st-key-bottomnav [data-testid="stElementContainer"], .st-key-bottomnav [data-testid="stPageLink"] { width: 100% !important; }
.st-key-bottomnav [data-testid="stPageLink-NavLink"] { display: flex; width: 100%; justify-content: center; align-items: center; text-align: center;
  border-radius: 999px; padding: 0.6rem 0.4rem; white-space: nowrap; }
.st-key-bottomnav [data-testid="stPageLink-NavLink"] > span, .st-key-bottomnav [data-testid="stPageLink-NavLink"] [data-testid="stMarkdownContainer"] { width: 100%; text-align: center; justify-content: center; }
.st-key-bottomnav [data-testid="stPageLink-NavLink"] p { font-size: 0.9rem; font-weight: 500; margin: 0; text-align: center; width: 100%; color: var(--dock-text) !important; }
.st-key-bottomnav [data-testid="stPageLink-NavLink"]:hover { background: var(--dock-hover); }
@media (max-width: 800px) { .tb-wl { display: none; } .st-key-topbar { padding: 0.35rem 0.7rem; } }

/* ---------- Buttons: quiet by default, accent for the one main action ---------- */
.stButton button, .stDownloadButton button, .stFormSubmitButton button {
  border-radius: 999px; font-weight: 600; padding: 0.55rem 1.1rem; white-space: nowrap; color: var(--text);
  background: var(--surface); border: 1px solid var(--border-2); box-shadow: none; transition: background .15s ease, border-color .15s ease, transform .1s ease;
}
.stButton button:hover, .stDownloadButton button:hover, .stFormSubmitButton button:hover { background: var(--surface-3); border-color: var(--border-2); color: var(--text); }
.stButton button:active { transform: scale(0.98); }
.stButton button[kind="primary"], .stFormSubmitButton button[kind="primaryFormSubmit"] { background: var(--pbtn-bg); color: var(--pbtn-text); border-color: var(--pbtn-bg); }
.stButton button[kind="primary"] p, .stFormSubmitButton button[kind="primaryFormSubmit"] p { color: var(--pbtn-text) !important; }
.stButton button[kind="primary"]:hover, .stFormSubmitButton button[kind="primaryFormSubmit"]:hover { background: var(--pbtn-hover); border-color: var(--pbtn-hover); color: var(--pbtn-text); }
.stButton button:disabled { opacity: 0.4; }

/* ---------- Inputs, filters, menus ---------- */
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div { background: var(--surface) !important; border: 1px solid var(--border-2) !important; box-shadow: none; }
[data-baseweb="select"] > div { border-radius: 999px !important; }
[data-baseweb="input"], [data-baseweb="textarea"] { border-radius: var(--radius-sm) !important; }
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea { background: transparent !important; }
[data-baseweb="input"]:focus-within, [data-baseweb="textarea"]:focus-within, [data-baseweb="select"] > div:focus-within { border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-soft) !important; }
[data-baseweb="tag"] { background: var(--strong) !important; border-radius: 999px !important; }
[data-baseweb="tag"] * { color: var(--on-strong) !important; }
[data-baseweb="popover"] > div, [data-baseweb="menu"] { background: var(--surface) !important; border: 1px solid var(--border); border-radius: 16px; box-shadow: var(--menu-shadow); }

/* Segmented controls and tabs */
[data-testid="stButtonGroup"], [data-baseweb="tab-list"] { background: var(--surface-3); border-radius: 999px; padding: 3px; gap: 2px; width: fit-content; }
[data-testid="stButtonGroup"] button, [data-baseweb="tab"] { border-radius: 999px !important; border: none !important; background: transparent !important; box-shadow: none !important; color: var(--text-2); font-weight: 500; }
[data-testid="stButtonGroup"] button[kind="segmented_controlActive"], [data-testid="stButtonGroup"] button[aria-checked="true"], [data-baseweb="tab"][aria-selected="true"] {
  background: var(--seg-active) !important; color: var(--seg-active-text) !important; }
[data-testid="stButtonGroup"] button[kind="segmented_controlActive"] *, [data-testid="stButtonGroup"] button[aria-checked="true"] *, [data-baseweb="tab"][aria-selected="true"] * { color: var(--seg-active-text) !important; }
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] { display: none; }

/* ---------- Surfaces: hairline + soft shadow ---------- */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]),
.tb-tile, .tb-dark, [data-testid="stMetric"], [data-testid="stExpander"], [data-testid="stDataFrame"] {
  background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: var(--radius) !important; box-shadow: var(--shadow) !important; }
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) { padding: 1rem 1.1rem 1.2rem 1.1rem; transition: box-shadow .2s ease; }
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]):hover { box-shadow: var(--shadow-hover) !important; }
[data-testid="stDataFrame"] { overflow: hidden; }
[data-testid="stExpander"] details, [data-testid="stExpander"] summary { background: transparent !important; }
hr { border-color: var(--border) !important; }

/* ---------- Text helpers ---------- */
.tb-muted { color: var(--muted); font-size: 0.9rem; }
.tb-label { color: var(--muted); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.09em; font-weight: 600; }
.tb-overdue { color: var(--alert); font-weight: 600; }
.tb-note { background: var(--accent-soft); border-left: 3px solid var(--accent-2); color: var(--text); padding: 0.8rem 1.1rem; border-radius: var(--radius-sm); margin: 0.4rem 0 0.8rem 0; }
.tb-notice { color: var(--muted); font-size: 0.82rem; }
.tb-section { margin: 2rem 0 0.8rem 0; display: flex; justify-content: space-between; align-items: baseline; }
.tb-section b { font-size: 1.15rem; font-weight: 600; letter-spacing: -0.02em; }

.tb-score { display: inline-block; min-width: 2.7rem; text-align: center; padding: 0.12rem 0.7rem; border-radius: 999px; font-weight: 600; font-variant-numeric: tabular-nums; font-size: 0.9rem; }
.tb-score.high { background: var(--accent); color: var(--on-accent); }
.tb-score.mid { background: var(--surface-3); color: var(--text); }
.tb-score.low { color: var(--muted); }
.tb-tag { display: inline-block; background: var(--surface-3); color: var(--text-2); border-radius: 999px; padding: 0.1rem 0.7rem; margin: 0 0.3rem 0.3rem 0; font-size: 0.8rem; font-weight: 500; }
.tb-status { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.09em; color: var(--muted); font-weight: 600; }

.tb-scale { display: flex; gap: 4px; margin: 0.3rem 0 0.5rem 0; }
.tb-scale div { flex: 1; height: 6px; border-radius: 999px; background: var(--surface-3); }
.tb-scale div.in { background: var(--border-2); }
.tb-scale div.at { background: var(--accent-2); }
.tb-progress { height: 6px; border-radius: 999px; background: var(--surface-3); overflow: hidden; }
.tb-progress div { height: 100%; background: var(--accent-2); border-radius: 999px; }

/* ---------- Stat tiles: label, one big number ---------- */
.tb-tile { padding: 1.2rem 1.3rem; min-height: 8rem; display: flex; flex-direction: column; justify-content: space-between; }
.tb-tile .tb-ico, .tb-tile .tb-go { display: none; }
.tb-tile .tb-tname { font-size: 0.86rem; font-weight: 500; color: var(--muted); }
.tb-tile .tb-num { font-size: 3rem; font-weight: 300; letter-spacing: -0.05em; line-height: 1; font-variant-numeric: tabular-nums; margin-top: 0.8rem; color: var(--text); }
.tb-tile .tb-num small { font-size: 0.95rem; letter-spacing: 0; color: var(--muted); margin-left: 0.35rem; font-weight: 500; }
.tb-tile .tb-sub { font-size: 0.78rem; color: var(--muted); margin-top: 0.35rem; }
.tb-tile.dark { background: var(--hi-bg) !important; border-color: transparent !important; }
.tb-tile.dark .tb-tname, .tb-tile.dark .tb-sub { color: var(--hi-sub); }
.tb-tile.dark .tb-num { color: var(--hi-text); }
.tb-tile.dark .tb-num small { color: var(--hi-unit); }

/* List panels */
.tb-dark { padding: 1.4rem 1.5rem; }
.tb-dark .tb-dh { font-size: 1.05rem; font-weight: 600; margin: 0 0 0.8rem 0; letter-spacing: -0.02em; }
.tb-dark .tb-row { display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0; border-top: 1px solid var(--border); }
.tb-dark .tb-row:first-of-type { border-top: none; }
.tb-dark .tb-n { font-size: 1.25rem; font-weight: 500; font-variant-numeric: tabular-nums; }
.tb-dark .tb-n.zero { color: var(--border-2); }
.tb-dark .tb-bar { height: 4px; border-radius: 99px; background: var(--surface-3); flex: 1; margin: 0 1rem; overflow: hidden; }
.tb-dark .tb-bar div { height: 100%; background: var(--accent-2); border-radius: 99px; }
.tb-dark .tb-item { padding: 0.7rem 0; border-top: 1px solid var(--border); }
.tb-dark .tb-item:first-of-type { border-top: none; }

/* Gauge + match ring */
.tb-gauge { text-align: center; }
.tb-gauge svg { width: 100%; max-width: 12rem; }
.tb-gauge .g-trk { stroke: var(--surface-3); } .tb-gauge .g-arc { stroke: var(--accent-2); } .tb-gauge .g-dot { fill: var(--surface); stroke: var(--accent-2); }
.tb-gauge .tb-gnum { font-size: 2.2rem; font-weight: 300; letter-spacing: -0.04em; line-height: 1; margin-top: -2.8rem; }
.tb-ring { position: relative; width: 6.6rem; height: 6.6rem; margin: 0 auto; }
.tb-ring svg { width: 100%; height: 100%; transform: rotate(-90deg); }
.tb-ring .trk { stroke: var(--surface-3); }
.tb-ring .arc { stroke: var(--accent-2); stroke-linecap: round; animation: tbDraw 1s cubic-bezier(.2,.7,.2,1) both; }
.tb-ring.mid .arc { stroke: var(--text-2); } .tb-ring.low .arc { stroke: var(--border-2); }
@keyframes tbDraw { from { stroke-dashoffset: 264; } }
.tb-ring .tb-rc { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.tb-ring .tb-rn { font-size: 1.7rem; font-weight: 300; letter-spacing: -0.04em; line-height: 1; font-variant-numeric: tabular-nums; }
.tb-ring .tb-rn small { font-size: 0.75rem; color: var(--muted); }
.tb-ring .tb-rl { font-size: 0.64rem; color: var(--muted); margin-top: 0.15rem; }
.tb-bigscore { font-size: 3.4rem; font-weight: 300; letter-spacing: -0.05em; line-height: 1; font-variant-numeric: tabular-nums; }
.tb-bigscore.mid, .tb-bigscore.low { color: var(--muted); }
.tb-bigscore small { font-size: 0.85rem; letter-spacing: 0; color: var(--muted); font-weight: 500; margin-left: 0.4rem; }

/* ---------- Landing hero: the brand gradient, one message, two doors ---------- */
.tb-hero { position: relative; overflow: hidden; border-radius: 32px; padding: 3.2rem 3rem 3.4rem 3rem; margin-bottom: 1.2rem; background: var(--hero-bg); }
.tb-hero .tb-pill { margin-bottom: 1.2rem; }
.tb-hero h1 { color: var(--hero-text) !important; font-size: 3rem !important; line-height: 1.04; letter-spacing: -0.045em; font-weight: 600 !important; max-width: 34rem; margin: 0 0 1rem 0; }
.tb-hero p { color: var(--hero-sub) !important; font-size: 1.1rem; max-width: 30rem; margin: 0; }
.tb-pill { display: inline-block; background: var(--hero-pill); border-radius: 999px; padding: 0.3rem 0.9rem; font-size: 0.78rem; font-weight: 500; color: var(--hero-pill-text); }
.tb-mark { color: var(--accent); }
.tb-steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1.4rem; }
.tb-step { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.2rem 1.3rem; }
.tb-step i { font-style: normal; display: inline-flex; width: 1.7rem; height: 1.7rem; border-radius: 50%; background: var(--accent); color: var(--on-accent); align-items: center; justify-content: center; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.7rem; }
.tb-step b { display: block; font-size: 1.02rem; margin-bottom: 0.3rem; letter-spacing: -0.02em; }
.tb-step span { color: var(--muted); font-size: 0.9rem; line-height: 1.5; }
@media (max-width: 800px) { .tb-hero { padding: 2rem 1.5rem; } .tb-hero h1 { font-size: 2.1rem !important; } .tb-steps { grid-template-columns: 1fr; } }

/* ---------- Card layout (My cards, match detail, browse) ---------- */
.tb-ch { display: flex; align-items: center; gap: 0.9rem; margin-bottom: 0.8rem; }
.tb-avl { width: 2.8rem; height: 2.8rem; flex: none; border-radius: 50%; background: var(--strong); color: var(--on-strong); display: flex; align-items: center; justify-content: center; font-size: 1.1rem; font-weight: 600; }
.tb-chm { flex: 1; min-width: 0; }
.tb-ct { font-size: 1.2rem; font-weight: 600; letter-spacing: -0.025em; line-height: 1.2; margin: 0.1rem 0; }
.tb-chips { margin-bottom: 0.4rem; }
.tb-blocks { display: grid; grid-template-columns: 1fr 1fr; gap: 0.7rem; margin-top: 0.8rem; }
.tb-block, .tb-fact { background: var(--surface-2); border-radius: 14px; padding: 0.8rem 1rem; }
.tb-block { font-size: 0.92rem; line-height: 1.5; color: var(--text-2); }
.tb-block.wide { grid-column: 1 / -1; }
.tb-block .tb-label { margin-bottom: 0.3rem; }
.tb-block ul { margin: 0; padding-left: 1.1rem; }
.tb-facts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.7rem; margin-top: 0.8rem; }
.tb-facts.three { grid-template-columns: repeat(3, 1fr); }
.tb-fv { font-size: 1.1rem; font-weight: 600; letter-spacing: -0.02em; margin-top: 0.2rem; font-variant-numeric: tabular-nums; }
@media (max-width: 800px) { .tb-blocks, .tb-facts, .tb-facts.three { grid-template-columns: 1fr 1fr; } }

/* ---------- Pipeline: one quiet progress line + a plain list ---------- */
.tb-flow { padding-bottom: 0.4rem; display: grid; grid-template-columns: repeat(5, 1fr); position: relative; padding-top: 0.2rem; }
.tb-flow::before { content: ''; position: absolute; left: 10%; right: 10%; top: 2.05rem; height: 2px; background: var(--border-2); }
.tb-sf { position: relative; text-align: center; }
.tb-sf b { position: relative; display: inline-flex; align-items: center; justify-content: center; width: 2.6rem; height: 2.6rem; border-radius: 50%;
  background: var(--surface); border: 1px solid var(--border-2); font-weight: 500; font-size: 1.05rem; color: var(--muted); font-variant-numeric: tabular-nums; }
.tb-sf.on b { background: var(--accent); color: var(--on-accent); border-color: var(--accent); }
.tb-sf span { display: block; font-size: 0.76rem; color: var(--muted); margin-top: 0.45rem; }
.tb-sf.on span { color: var(--text); font-weight: 500; }

@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
/* ---------- Poster card (My cards): peak above clouds, glass chips, white pill + round arrow ---------- */
.tb-poster { position: relative; height: 33rem; border-radius: 28px; overflow: hidden; color: #fff; background: #0B1E6B;
  box-shadow: 0 2px 4px rgba(0,0,0,0.10), 0 18px 40px rgba(0,0,0,0.20); transition: transform .3s ease, box-shadow .3s ease; }
.tb-poster:hover { transform: translateY(-4px); box-shadow: 0 4px 8px rgba(0,0,0,0.12), 0 26px 52px rgba(0,0,0,0.30); }
.tb-photo { position: absolute; inset: 0; background-size: cover; background-position: center; transition: transform 1.1s cubic-bezier(.2,.7,.2,1); }
.tb-poster:hover .tb-photo { transform: scale(1.08); }
.tb-poster { background: #1C2430; }
.tb-pshade { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(6,10,24,0.38) 0%, rgba(6,10,24,0) 26%, rgba(6,10,24,0) 52%, rgba(6,10,24,0.55) 100%); }
.tb-ptop { position: absolute; z-index: 2; top: 1.1rem; left: 1.3rem; right: 1.2rem; display: flex; justify-content: space-between; align-items: flex-start; }
.tb-pk { font-size: 0.8rem; font-weight: 600; letter-spacing: 0.01em; text-shadow: 0 1px 10px rgba(0,0,0,0.35); }
.tb-steps5 { display: flex; gap: 4px; margin-top: 0.45rem; }
.tb-steps5 i { width: 1.15rem; height: 4px; border-radius: 99px; background: rgba(255,255,255,0.35); }
.tb-steps5 i.on { background: #fff; }
.tb-pchip { font-size: 0.74rem; padding: 0.32rem 0.8rem; border-radius: 999px; background: rgba(255,255,255,0.22); border: 1px solid rgba(255,255,255,0.4);
  -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px); text-transform: capitalize; white-space: nowrap; }
.tb-pbot { position: absolute; z-index: 2; left: 0.8rem; right: 0.8rem; bottom: 0.8rem; }
.tb-glass { padding: 1.05rem 1.15rem 1rem 1.15rem; border-radius: 22px; background: rgba(14,20,34,0.46); border: 1px solid rgba(255,255,255,0.22);
  -webkit-backdrop-filter: blur(18px) saturate(150%); backdrop-filter: blur(18px) saturate(150%); box-shadow: inset 0 1px 0 rgba(255,255,255,0.22); }
.tb-sp { width: 0.7rem; height: 0.7rem; fill: #fff; margin-right: 0.45rem; vertical-align: -1px; }
.tb-pstage { font-size: 0.78rem; color: rgba(255,255,255,0.82); margin-bottom: 0.3rem; }
.tb-ptitle { font-size: 1.5rem; line-height: 1.08; letter-spacing: -0.03em; font-weight: 600; text-shadow: 0 2px 18px rgba(0,0,0,0.35); }
.tb-psub { margin-top: 0.5rem; font-size: 0.84rem; line-height: 1.45; color: rgba(255,255,255,0.80); }
.tb-psec { margin-top: 0.8rem; display: flex; gap: 0.4rem; flex-wrap: wrap; }
.tb-psec span { font-size: 0.72rem; padding: 0.25rem 0.7rem; border-radius: 999px; background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.32); -webkit-backdrop-filter: blur(8px); backdrop-filter: blur(8px); }
.tb-pfoot { margin-top: 0.9rem; font-size: 0.76rem; color: rgba(255,255,255,0.7); }
.tb-pcta { height: 3.7rem; }
.tb-parrow { position: absolute; right: 0.2rem; bottom: 0.2rem; width: 2.9rem; height: 2.9rem; border-radius: 50%; background: rgba(10,14,32,0.9); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 1.15rem; transition: transform .25s ease, background .25s ease; }
.tb-poster:hover .tb-parrow { transform: rotate(45deg); background: #fff; color: #0A1636; }
/* The real Edit button sits on the card, bottom-left, as the white pill from the reference */
[class*="st-key-poster_edit_"] { position: relative; z-index: 5; margin-top: -3.86rem; margin-left: 1.3rem; margin-bottom: 1.6rem; width: fit-content !important; }
[class*="st-key-poster_edit_"] button { background: #fff !important; color: #0A1636 !important; border: none !important; padding: 0.7rem 2.3rem !important; box-shadow: 0 6px 18px rgba(0,0,0,0.25) !important; }
.stApp [class*="st-key-poster_edit_"] button p, .stApp [class*="st-key-poster_edit_"] button { color: #0A1636 !important; }
[class*="st-key-poster_edit_"] button:hover { background: #EEF2FF !important; }

/* ---------- Home: full-bleed bridge scene, two-tone headline, text and doors floating on the picture ---------- */
[data-testid="stMain"] { overflow-x: clip; }
.tb-home { position: relative; width: 100vw; left: 50%; transform: translateX(-50%); margin-top: -11rem; height: min(96vh, 56rem); min-height: 40rem; overflow: hidden; color: var(--on-scene); }
.tb-home-bg { position: absolute; inset: 0; background: url(/app/static/bridge.jpg) center 64% / cover no-repeat; filter: var(--home-filter); }
.tb-home-tint { position: absolute; inset: 0; background: var(--home-tint); mix-blend-mode: var(--home-blend, normal); }
.tb-home-fade { position: absolute; left: 0; right: 0; bottom: 0; height: 12%; background: linear-gradient(180deg, transparent, var(--canvas)); }
.tb-home-copy { position: absolute; left: 0; right: 0; top: 14%; text-align: center; padding: 0 1.5rem; }
.tb-home-copy h1 { font-size: clamp(2.4rem, 5.4vw, 4.7rem) !important; line-height: 1.1; letter-spacing: -0.045em; font-weight: 400 !important; margin: 0 auto; max-width: 62rem; color: var(--h-dark) !important; }
.tb-home-copy h1 em { font-style: normal; display: inline-block; background: linear-gradient(90deg, var(--h-g1) 0%, var(--h-g2) 100%); -webkit-background-clip: text; background-clip: text; color: transparent; -webkit-text-fill-color: transparent; }
.tb-home-copy p { margin: 1.3rem auto 0 auto; max-width: 30rem; font-size: 1.05rem; line-height: 1.45; color: var(--h-sub) !important; }
.tb-home-left { position: absolute; left: max(1.5rem, calc(50% - 31rem)); bottom: 12.6rem; max-width: 24rem; color: var(--on-scene); }
.tb-home-left .tb-tagline { display: flex; align-items: center; gap: 0.55rem; font-size: 0.9rem; font-weight: 500; margin-bottom: 0.7rem; }
.tb-home-left .tb-dots { width: 1.05rem; height: 1.05rem; border-radius: 50%; border: 2px dotted currentColor; }
.tb-home-left p { font-size: 0.92rem; line-height: 1.5; color: rgba(255,255,255,0.88) !important; margin: 0; text-shadow: 0 1px 14px rgba(0,0,0,0.35); }
.tb-home-right { position: absolute; right: max(1.5rem, calc(50% - 31rem)); bottom: 11rem; }
.tb-peek { display: block; width: 13.5rem; padding: 0.9rem 1rem; border-radius: 22px; text-decoration: none !important; color: var(--on-scene) !important;
  background: var(--scene-glass); -webkit-backdrop-filter: blur(18px) saturate(160%); backdrop-filter: blur(18px) saturate(160%); border: 1px solid rgba(255,255,255,0.35); transition: transform .25s ease; }
.tb-peek:hover { transform: translateY(-3px); }
.tb-peek b { display: flex; align-items: center; gap: 0.6rem; font-size: 0.92rem; font-weight: 500; }
.tb-peek b i { font-style: normal; width: 1.7rem; height: 1.7rem; border-radius: 50%; background: rgba(255,255,255,0.9); color: #222; display: inline-flex; align-items: center; justify-content: center; font-size: 0.8rem; }
.tb-peek span { display: block; margin-top: 0.4rem; font-size: 0.75rem; color: rgba(255,255,255,0.8); }
.st-key-herobtns { position: relative; z-index: 5; margin-top: -10.6rem; margin-bottom: 7.6rem; }
.st-key-herobtns .stButton button { background: rgba(255,255,255,0.92); color: #26282B; border: none; padding: 0.7rem 1rem; font-size: 0.9rem; font-weight: 600; box-shadow: 0 6px 20px rgba(0,0,0,0.18); }
.st-key-herobtns .stButton button p { color: #26282B !important; }
.st-key-herobtns .stButton button:hover { background: #fff; }
.st-key-herobtns .stButton:nth-of-type(2) button, .st-key-herobtns [data-testid="stColumn"]:nth-child(2) button { background: rgba(24,26,29,0.5); -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px); color: #fff; box-shadow: none; border: 1px solid rgba(255,255,255,0.45); }
.st-key-herobtns [data-testid="stColumn"]:nth-child(2) button p { color: #fff !important; }
.st-key-herobtns [data-testid="stColumn"]:nth-child(2) button:hover { background: rgba(24,26,29,0.7); }
.tb-section-title { text-align: center; font-size: 1.6rem; font-weight: 600; letter-spacing: -0.03em; margin: 1rem 0 0.2rem 0; }
@media (max-width: 800px) { .tb-home-left, .tb-home-right { display: none; } .st-key-herobtns { margin-top: -4rem; } }
/* ---------- Alliance: infinite logo marquee on a dark band (hover pauses it) ---------- */
.tb-alliance { position: relative; width: 100vw; left: 50%; transform: translateX(-50%); margin: 2rem 0 2.6rem 0; padding: 3.4rem 0 2.8rem 0; overflow: hidden; text-align: center; color: #fff;
  background: var(--band-glow), var(--band-bg); }
.tb-alliance::before { content: ''; position: absolute; left: 50%; top: 62%; width: 90rem; height: 90rem; transform: translate(-50%, -50%); border-radius: 50%; pointer-events: none;
  background: repeating-radial-gradient(circle, transparent 0 7rem, rgba(255,255,255,0.045) 7rem calc(7rem + 1px)); }
.tb-alliance-head { position: relative; padding: 0 1.5rem; }
.tb-alliance-head b { display: block; font-size: 1.9rem; font-weight: 700; letter-spacing: -0.03em; color: #fff; }
.tb-alliance-head span { display: block; margin: 0.6rem auto 0 auto; max-width: 34rem; font-size: 0.95rem; color: rgba(255,255,255,0.66); }
.tb-marquee { position: relative; margin-top: 2.6rem; overflow: hidden;
  -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 12%, #000 88%, transparent 100%); mask-image: linear-gradient(90deg, transparent 0, #000 12%, #000 88%, transparent 100%); }
.tb-track { display: flex; width: max-content; animation: tbMarquee 55s linear infinite; }
.tb-marquee:hover .tb-track { animation-play-state: paused; }
@keyframes tbMarquee { to { transform: translateX(-50%); } }
.tb-pt { flex: none; width: 15rem; padding: 0 1.4rem; display: flex; flex-direction: column; align-items: center; justify-content: center; opacity: 0.94; transition: opacity .25s ease, transform .25s ease; }
.tb-pt:hover { opacity: 1; transform: translateY(-3px); }
.tb-pt-logo { height: 4.7rem; display: flex; align-items: center; justify-content: center; }
.tb-pt-logo img { width: auto; max-width: 100%; object-fit: contain; display: block; }
.tb-pt-name { margin-top: 0.9rem; min-height: 1.6rem; font-size: 0.62rem; letter-spacing: 0.1em; text-transform: uppercase; line-height: 1.35; color: rgba(255,255,255,0.62); }
/* ---------- Dashboard: stats hero (greeting, big number, score strip, gradient cards, white KPI cards, chart) ---------- */
.tb-hey { margin-top: -1rem; }
.tb-hey h1 { padding: 0 !important; font-size: 2.7rem !important; font-weight: 500 !important; letter-spacing: -0.04em; line-height: 1.04; margin: 0; }
.tb-hey h1.soft { color: var(--muted) !important; font-weight: 400 !important; }
.st-key-bt_hero [data-testid="stSelectbox"] { width: fit-content; min-width: 14rem; max-width: 24rem; margin: 1rem 0 0.4rem 0; }
.tb-score-hero { display: flex; align-items: flex-end; gap: 1.1rem; margin-top: 1.4rem; }
.tb-sh-n { font-size: 7rem; font-weight: 300; letter-spacing: -0.07em; line-height: 0.85; font-variant-numeric: tabular-nums; }
.tb-sh-side { display: flex; flex-direction: column; gap: 0.1rem; padding-bottom: 0.4rem; font-size: 0.8rem; color: var(--muted); }
.tb-sh-side b { font-size: 0.95rem; color: var(--text); font-weight: 600; }
.tb-bg { margin: 1.4rem 0 1.8rem 0; padding: 0 0.3rem; }
.tb-bg-zones { position: relative; height: 3.1rem; display: flex; gap: 6px; }
.tb-bg-zones .z1, .tb-bg-zones .z2, .tb-bg-zones .z3 { height: 100%; border-radius: 14px; }
.tb-bg-zones .z1 { width: 50%; background: var(--surface-3); }
.tb-bg-zones .z2 { width: 25%; background: var(--border-2); }
.tb-bg-zones .z3 { width: 25%; background: var(--accent-soft); box-shadow: inset 0 0 0 1px var(--accent-2); }
.tb-bg-zones i { position: absolute; width: 7px; height: 7px; border-radius: 50%; background: var(--text); opacity: .75; transform: translateX(-50%); }
.tb-bg-mark { position: absolute; top: -0.9rem; bottom: -0.3rem; width: 0; transform: translateX(-50%); }
.tb-bg-mark span { position: absolute; top: 0; left: 50%; transform: translateX(-50%); font-size: 0.6rem; color: var(--accent); }
.tb-bg-mark b { position: absolute; top: 0.7rem; bottom: 0; left: 0; width: 2px; background: var(--accent); transform: translateX(-50%); }
.tb-bg-val { position: absolute; top: calc(100% + 0.3rem); background: var(--canvas-solid, transparent); transform: translateX(-50%); font-size: 0.72rem; font-weight: 600; }
.tb-bg-axis { position: relative; height: 1.2rem; margin-top: 1.5rem; font-size: 0.7rem; color: var(--muted); }
.tb-bg-axis span { position: absolute; transform: translateX(-50%); }
.tb-bg-axis span:first-child { transform: none; } .tb-bg-axis span:last-child { transform: translateX(-100%); }

/* gradient match cards */
[class*="st-key-dcard_"] { position: relative; }
[class*="st-key-dbtn_"], [class*="st-key-dbtw_"] { position: absolute !important; top: 0.9rem; right: 0.9rem; z-index: 6; width: auto !important; }
[class*="st-key-dbtn_"] button, [class*="st-key-dbtw_"] button, [class*="st-key-dbtw_"] a { width: 2.5rem; height: 2.5rem; min-height: 0; padding: 0 !important; border-radius: 50% !important; display: flex; align-items: center; justify-content: center; font-size: 1.05rem; box-shadow: none !important; }
[class*="st-key-dbtn_"] button { background: #111 !important; color: #fff !important; border: none !important; }
[class*="st-key-dbtn_"] button p { color: #fff !important; }
[class*="st-key-dbtw_"] button, [class*="st-key-dbtw_"] a { background: var(--surface-3) !important; color: var(--text) !important; border: none !important; text-decoration: none !important; }
[class*="st-key-dbtw_"] p { color: var(--text) !important; margin: 0; }
.tb-gc2 { position: relative; overflow: hidden; border-radius: 28px; padding: 1.1rem 1.2rem 1.1rem 1.2rem; min-height: 14.2rem; display: flex; flex-direction: column; justify-content: space-between;
  box-shadow: 0 14px 34px rgba(30,30,20,0.20), inset 0 1px 0 rgba(255,255,255,0.35); }
.tb-gc2.hi { background: radial-gradient(14rem 10rem at 100% 100%, rgba(255,255,255,0.22), transparent 70%), linear-gradient(150deg, var(--accent-deep), var(--accent)); color: var(--on-accent); }
.tb-gc2.mid { background: linear-gradient(150deg, var(--strong), var(--surface-3)); color: var(--on-strong); }
.tb-gc2.lo { background: var(--surface-3); color: var(--text); box-shadow: var(--shadow); }
.tb-gc2.lo .tb-gc2-l, .tb-gc2.lo .tb-gc2-d, .tb-gc2.lo .tb-gc2-d * { color: var(--muted) !important; } .tb-gc2.lo .tb-gc2-ring, .tb-gc2.lo .tb-gc2-ring::after { border-color: var(--border-2); }
.tb-gc2-top { display: flex; align-items: center; gap: 0.7rem; padding-right: 3rem; }
.tb-gc2-ring { width: 2.1rem; height: 2.1rem; flex: none; border-radius: 50%; border: 2px solid rgba(255,255,255,0.7); position: relative; }
.tb-gc2-ring::after { content: ''; position: absolute; inset: 0.45rem; border-radius: 3px; border: 1.5px solid rgba(255,255,255,0.7); }
.tb-gc2-name { font-size: 1.05rem; font-weight: 600; line-height: 1.15; letter-spacing: -0.02em; }
.tb-gc2-row { display: flex; justify-content: space-between; align-items: flex-end; margin-top: 1rem; }
.tb-gc2-l { font-size: 0.68rem; color: rgba(255,255,255,0.72); }
.tb-gc2-n { font-size: 2.6rem; font-weight: 300; letter-spacing: -0.05em; line-height: 1; font-variant-numeric: tabular-nums; }
.tb-gc2-n small { font-size: 0.8rem; letter-spacing: 0; opacity: .7; margin-left: 0.2rem; }
.tb-gc2-r { text-align: right; } .tb-gc2-s { font-size: 0.95rem; font-weight: 500; }
.tb-gc2-dots { height: 1.1rem; margin: 0.7rem 0 0.5rem 0; opacity: .55; background-image: radial-gradient(circle, rgba(255,255,255,0.9) 1.2px, transparent 1.6px); background-size: 9px 9px; -webkit-mask-image: linear-gradient(90deg, #000, transparent 80%); mask-image: linear-gradient(90deg, #000, transparent 80%); }
.tb-gc2-foot { display: flex; flex-direction: column; align-items: flex-start; gap: 0.35rem; }
.tb-gc2-t { font-size: 0.82rem; font-weight: 500; }
.tb-gc2-d { font-size: 0.74rem; color: rgba(255,255,255,0.85); }
.tb-gc2-d * { color: rgba(255,255,255,0.9) !important; }

/* white KPI cards */
.tb-kp { position: relative; background: var(--surface); border: 1px solid var(--border); border-radius: 26px; padding: 1rem 1.1rem 1.1rem 1.1rem; min-height: 11rem; box-shadow: var(--shadow); display: flex; flex-direction: column; justify-content: space-between; }
.tb-kp-ico { width: 2.3rem; height: 2.3rem; border-radius: 50%; border: 1px solid var(--border-2); display: inline-flex; align-items: center; justify-content: center; font-size: 1.05rem; line-height: 1; color: var(--text-2); }
.tb-kp-l { font-size: 0.88rem; font-weight: 500; color: var(--text); margin-top: 1.8rem; }
.tb-kp-n { font-size: 2.4rem; font-weight: 400; letter-spacing: -0.05em; line-height: 1; font-variant-numeric: tabular-nums; }
.tb-kp-n small { font-size: 0.9rem; letter-spacing: 0; color: var(--muted); margin-left: 0.2rem; }
.tb-warn { position: absolute; top: 0.6rem; left: 2.6rem; width: 1.15rem; height: 1.15rem; border-radius: 5px; background: var(--accent); color: #fff; font-size: 0.7rem; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.tb-recent { padding-right: 4rem !important; display: flex; align-items: center; gap: 0.9rem; background: var(--surface); border: 1px solid var(--border); box-shadow: var(--shadow); border-radius: 22px; padding: 0.9rem 1.1rem; margin: 0.8rem 0; }
.tb-recent .tb-kp-l { margin: 0; } .tb-recent-t { font-weight: 600; font-size: 0.92rem; margin: 0.1rem 0; }
[class*="st-key-dcard_recent"] [class*="st-key-dbtw_"] { top: 50%; transform: translateY(-50%); right: 1rem; }
.tb-chart-head { display: flex; align-items: center; gap: 0.7rem; font-size: 0.95rem; }
.tb-chart { width: 100%; margin-top: 0.4rem; overflow: visible; }
.tb-chart .cg { stroke: var(--border); stroke-width: 1; } .tb-chart .ct { fill: var(--muted); font-size: 9px; }
.tb-chart .cl1 { fill: none; stroke: var(--text); stroke-width: 2.2; stroke-linecap: round; }
.tb-chart .cl2, .tb-chart .cl3 { fill: none; stroke-width: 1.4; opacity: .55; }
.tb-chart .cl2 { stroke: var(--text-2); } .tb-chart .cl3 { stroke: var(--accent-2); }
.tb-chart .cb { stroke: var(--text); stroke-width: 1; } .tb-chart .cm { fill: var(--text); }
.tb-chart .cbub { fill: var(--accent); } .tb-chart .cbt { fill: var(--on-accent); font-size: 11px; font-weight: 700; }
.tb-legend { display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 0.5rem; font-size: 0.72rem; color: var(--muted); }
.tb-legend i { display: inline-block; width: 6px; height: 6px; border-radius: 50%; margin-right: 0.35rem; vertical-align: 1px; }
.tb-legend .l1 { background: var(--text); } .tb-legend .l2 { background: var(--text-2); } .tb-legend .l3 { background: var(--accent-2); }
/* ---------- Browse: one full-bleed satellite map, everything floats on it ---------- */
.st-key-bmap { position: fixed !important; inset: 0; z-index: 1; width: 100vw !important; height: 100vh !important; margin: 0 !important; padding: 0 !important; overflow: hidden; background: #0B1424; }
.st-key-bmap > div, .st-key-bmap [data-testid="stElementContainer"], .st-key-bmap [data-testid="stPlotlyChart"] { width: 100vw !important; height: 100vh !important; max-width: none !important; }
.st-key-bmap [data-testid="stPlotlyChart"], .st-key-bmap .stPlotlyChart, .st-key-bmap .js-plotly-plot, .st-key-bmap .plot-container { height: 100vh !important; width: 100% !important; }
.st-key-bmap::after { content: ''; position: absolute; inset: 0; pointer-events: none; background: linear-gradient(180deg, rgba(6,12,28,0.55) 0%, rgba(6,12,28,0.0) 22%, rgba(6,12,28,0.0) 70%, rgba(6,12,28,0.55) 100%), linear-gradient(90deg, rgba(6,12,28,0) 55%, rgba(6,12,28,0.62) 100%); }
.st-key-brtop, .st-key-brpanel, .st-key-brleg { position: fixed; z-index: 900; color: #fff; }
.st-key-brtop { top: 5.2rem; left: 50%; transform: translateX(-50%); width: min(92vw, 40rem); padding: 0.4rem 0.5rem; border-radius: 999px;
  background: rgba(14,22,40,0.55); -webkit-backdrop-filter: blur(18px) saturate(150%); backdrop-filter: blur(18px) saturate(150%); border: 1px solid rgba(255,255,255,0.22); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
.st-key-brtop [data-baseweb="select"] > div, .st-key-brtop [data-baseweb="select"] > div > div { background: rgba(255,255,255,0.14) !important; border-color: rgba(255,255,255,0.24) !important; }
.st-key-brtop [data-baseweb="select"] * { color: #fff !important; }
.st-key-brtop button { background: rgba(255,255,255,0.14) !important; color: #fff !important; border: 1px solid rgba(255,255,255,0.22) !important; }
.st-key-brtop button p, .st-key-brtop button span { color: #fff !important; }
.tb-brcount { text-align: right; font-size: 0.85rem; color: rgba(255,255,255,0.8); padding-right: 0.8rem; } .tb-brcount b { font-size: 1.3rem; color: #fff; margin-right: 0.25rem; }
.st-key-brpanel { top: 9.6rem; right: max(1rem, calc(50vw - 47rem)); bottom: auto; max-height: calc(100vh - 16.4rem); width: 23.5rem; overflow-y: auto; padding: 1rem 0.9rem 1rem 0.9rem; border-radius: 28px;
  background: rgba(12,18,34,0.52); -webkit-backdrop-filter: blur(22px) saturate(150%); backdrop-filter: blur(22px) saturate(150%); border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 18px 50px rgba(0,0,0,0.38); scrollbar-width: none; }
.st-key-brpanel::-webkit-scrollbar { display: none; }
.st-key-brpanel .stButton button { background: rgba(255,255,255,0.14); color: #fff; border: 1px solid rgba(255,255,255,0.24); }
.st-key-brpanel .stButton button p { color: #fff !important; }
.tb-brh b { display: block; font-size: 1.5rem; letter-spacing: -0.035em; line-height: 1.1; } .tb-brh span { font-size: 0.78rem; color: rgba(255,255,255,0.7); }
.st-key-brleg { overflow: visible; min-height: 2.6rem; display: flex; align-items: center; width: fit-content !important; left: max(1rem, calc(50vw - 47rem)); bottom: 6.4rem; padding: 0.55rem 1rem; border-radius: 999px; background: rgba(14,22,40,0.55); -webkit-backdrop-filter: blur(16px); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.2); }
.tb-brleg { display: flex; gap: 1rem; align-items: center; font-size: 0.76rem; } .tb-brleg em { font-style: normal; color: rgba(255,255,255,0.65); }
.tb-brleg i { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 0.35rem; } .tb-brleg .hi { background: var(--pin-hi); } .tb-brleg .mid { background: #fff; } .tb-brleg .lo { background: #9AA3B2; }
/* match cards: name left, round picture right, gradient by strength (reference: Tennis / Gym / Badminton / Boxing tiles) */
[class*="st-key-bm_"] { position: relative; margin-top: 0.75rem; }
.tb-bm { position: relative; overflow: hidden; border-radius: 22px; min-height: 9.2rem; padding: 1.05rem 1.2rem 3.1rem 1.2rem; color: #fff; box-shadow: 0 8px 24px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.18); }
.tb-bm.hi { background: linear-gradient(105deg, #1F8A4C 0%, #35B06A 60%, #5BD08A 100%); }
.tb-bm.mid { background: linear-gradient(105deg, #1A2D44 0%, #3A6A8C 60%, #8EB7CE 100%); }
.tb-bm.lo { background: linear-gradient(105deg, #1A1C20 0%, #2A3138 70%, #3A4650 100%); }
.tb-bm-l { position: relative; z-index: 2; max-width: 56%; } .tb-bm-t { font-size: 1.25rem; font-weight: 500; line-height: 1.15; letter-spacing: -0.02em; } .tb-bm-s { margin-top: 0.4rem; font-size: 0.72rem; opacity: 0.78; }
.tb-bm-img { position: absolute; top: 0; right: 0; bottom: 0; width: 55%; background-size: cover; background-position: center; -webkit-mask-image: linear-gradient(90deg, transparent 0%, #000 55%); mask-image: linear-gradient(90deg, transparent 0%, #000 55%); transition: transform .7s ease; }
.tb-bm:hover .tb-bm-img { transform: scale(1.08); }
.tb-bm-sc { position: absolute; z-index: 2; top: 0.9rem; right: 1rem; min-width: 2.6rem; text-align: center; padding: 0.15rem 0.65rem; border-radius: 999px; background: rgba(255,255,255,0.9); color: #111; font-weight: 700; font-size: 0.9rem; }
[class*="st-key-bmb_"] { position: absolute !important; left: 1.1rem; bottom: 0.7rem; z-index: 5; width: auto !important; }
[class*="st-key-bmb_"] button { background: transparent !important; border: none !important; padding: 0.2rem 0 !important; min-height: 0; box-shadow: none !important; color: #fff !important; }
[class*="st-key-bmb_"] button p { font-size: 0.72rem; letter-spacing: 0.1em; font-weight: 600; color: #fff !important; }
[class*="st-key-bmb_"] button:hover p { text-decoration: underline; }
.st-key-consentlink [data-testid="stPageLink-NavLink"] { display: inline-flex; align-items: center; justify-content: center; height: 2.75rem; padding: 0 1.3rem; border-radius: 999px; background: var(--surface); border: 1px solid var(--border-2); text-decoration: none; }
.st-key-consentlink [data-testid="stPageLink-NavLink"]:hover { background: var(--surface-3); }
.st-key-consentlink p { margin: 0; font-weight: 600; font-size: 0.9rem; }
/* ---------- Pipeline: a glowing river on a dark glass panel, then a calm list ---------- */
.tb-river { position: relative; border-radius: 30px; padding: 1.2rem 1.4rem 0.9rem 1.4rem; margin-bottom: 0.4rem; overflow: hidden; color: #fff;
  background: radial-gradient(34rem 14rem at 50% 38%, rgba(70,110,200,0.28), transparent 70%), linear-gradient(160deg, #11172A 0%, #0A0E1C 100%);
  border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 18px 44px rgba(8,12,30,0.38), inset 0 1px 0 rgba(255,255,255,0.16); }
.tb-river::before { content: ''; position: absolute; left: 50%; top: 46%; width: 26rem; height: 26rem; transform: translate(-50%,-50%); border-radius: 50%;
  background: repeating-radial-gradient(circle, transparent 0 2.2rem, rgba(255,255,255,0.05) 2.2rem calc(2.2rem + 1px)); pointer-events: none; }
.tb-river svg { position: relative; width: 100%; display: block; }
.tb-river .fl { fill: none; stroke: rgba(255,255,255,0.20); stroke-width: 1.4; }
.tb-river .fl.live { stroke: var(--accent-2); stroke-width: 1.6; stroke-dasharray: 5 9; animation: tbFlow 3.4s linear infinite; filter: drop-shadow(0 0 4px var(--accent-2)); }
@keyframes tbFlow { to { stroke-dashoffset: -56; } }
.tb-river .fh { fill: rgba(255,255,255,0.04); stroke: rgba(255,255,255,0.10); }
.tb-river .fc { fill: #121A33; stroke: rgba(255,255,255,0.32); stroke-width: 1.5; }
.tb-river .fn.on .fc { stroke: var(--accent-2); stroke-width: 2; filter: drop-shadow(0 0 9px var(--accent-2)); }
.tb-river .fnum { fill: #fff; font-size: 24px; font-weight: 300; font-variant-numeric: tabular-nums; }
.tb-river .flab { fill: rgba(255,255,255,0.66); font-size: 11px; letter-spacing: 0.14em; }
.tb-river .fn.on .flab { fill: #fff; }
.tb-river-foot { display: flex; justify-content: space-between; margin-top: 0.2rem; padding: 0 0.4rem; font-size: 0.74rem; color: rgba(255,255,255,0.6); }
.tb-track5 { display: inline-flex; align-items: center; gap: 5px; }
.tb-track5 i { width: 7px; height: 7px; border-radius: 50%; background: var(--border-2); }
.tb-track5 i.on { background: var(--accent-2); } .tb-track5 i.cur { box-shadow: 0 0 0 3px var(--accent-soft); }
.tb-track5 em { font-style: normal; margin-left: 0.4rem; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.09em; color: var(--muted); font-weight: 600; }
.tb-track5.off i { background: var(--border); }

/* dashboard calendar + chart card, theme colours only */
.st-key-dcard_cal { margin: 0.8rem 0; } .st-key-dcard_chart { background: var(--surface); border: 1px solid var(--border); border-radius: 26px; padding: 1.1rem 1.2rem; box-shadow: var(--shadow); }
.tb-i { width: 1.15rem; height: 1.15rem; fill: none; stroke: currentColor; stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; }
.tb-cal { background: var(--surface); border: 1px solid var(--border); border-radius: 26px; padding: 1.1rem 1.2rem 1rem 1.2rem; color: var(--text); box-shadow: var(--shadow); }
.tb-cal-h { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.8rem; } .tb-cal-h b { font-size: 1.05rem; } .tb-cal-h span { font-size: 0.78rem; color: var(--muted); }
.tb-cal-w, .tb-cal-g { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; text-align: center; } .tb-cal-w span { font-size: 0.62rem; letter-spacing: .08em; color: var(--muted); margin-bottom: 3px; }
.tb-cal-g i { font-style: normal; aspect-ratio: 1; display: flex; align-items: center; justify-content: center; border-radius: 50%; background: var(--surface-2); font-size: 0.72rem; color: var(--text-2); }
.tb-cal-g i.e { background: none; } .tb-cal-g i.due { background: var(--accent-soft); box-shadow: inset 0 0 0 1.5px var(--accent-2); color: var(--text); } .tb-cal-g i.tod { background: var(--accent); color: var(--on-accent); font-weight: 700; }
.tb-cal-f { display: flex; gap: 1rem; margin-top: 0.8rem; font-size: 0.7rem; color: var(--muted); } .tb-cal-f i { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 0.35rem; } .tb-cal-f i.due { box-shadow: inset 0 0 0 1.5px var(--accent-2); } .tb-cal-f i.tod { background: var(--accent); }
.tb-kp-ico { color: var(--accent); }

/* dashboard bento: calm, even panels on a pastel gradient (reference: weather dashboard). Panels are near-opaque theme surfaces. */
.st-key-dgreet, .st-key-dscore, .st-key-dtabs, .tb-kp, .tb-recent, .tb-cal, .st-key-dcard_chart {
  background: var(--glass-a) !important; border: 1px solid var(--glass-rim) !important; -webkit-backdrop-filter: blur(24px) saturate(150%); backdrop-filter: blur(24px) saturate(150%);
  box-shadow: 0 10px 30px rgba(40,30,20,0.08), inset 0 1px 0 var(--glass-hi) !important; }
.st-key-dgreet, .st-key-dscore, .st-key-dtabs { border-radius: 28px; padding: 1.3rem 1.5rem 1.2rem 1.5rem; margin-bottom: 1rem; }
.st-key-dcard_chart { margin-top: 1rem; }
.stApp [data-baseweb="tab-list"] { background: transparent !important; border-color: var(--glass-rim) !important; }
.tb-gc2 { box-shadow: 0 8px 22px rgba(30,20,10,0.16); }
.tb-recent .tb-recent-t { font-size: 0.85rem; }
.st-key-dcard_recent .tb-recent { flex-direction: column; align-items: flex-start; justify-content: space-between; gap: 0.5rem; min-height: 11rem; margin: 0; padding: 1rem 1.1rem 1.1rem 1.1rem !important; border-radius: 26px; }
.st-key-dcard_recent .tb-recent .tb-kp-l { margin-top: 1.4rem; }
[class*="st-key-dcard_recent"] [class*="st-key-dbtw_"] { top: 0.9rem; transform: none; right: 0.9rem; }
.st-key-dcard_chart .tb-chart { max-height: 15rem; }

/* ---------- Pipeline timeline (reference: Cardiology treatment timeline) ---------- */
.st-key-tlhead { background: var(--surface); border: 1px solid var(--border); border-radius: 30px; padding: 1.1rem 1.5rem 1rem 1.5rem; box-shadow: var(--shadow); margin-bottom: 1rem; }
.tb-tl-title { font-size: 2.6rem; font-weight: 400; letter-spacing: -0.045em; line-height: 1; }
.tb-tl-stats { display: flex; gap: 2.4rem; flex-wrap: wrap; }
.tb-tl-stats div { display: flex; flex-direction: column; gap: 0.1rem; } .tb-tl-stats span { font-size: 0.68rem; color: var(--muted); }
.tb-tl-stats b { font-size: 1.7rem; font-weight: 400; letter-spacing: -0.04em; font-variant-numeric: tabular-nums; } .tb-tl-stats b small { font-size: 0.8rem; color: var(--muted); margin-left: 0.15rem; } .tb-tl-stats b.bad { color: var(--alert); }
.st-key-tlhead [data-testid="stButtonGroup"] { margin-top: 0.8rem; }
.st-key-tlpanel { position: relative; background: var(--surface-3); border-radius: 36px; padding: 1.5rem 1.4rem 1.6rem 1.4rem; border: 1px solid var(--border); }
.st-key-tlpanel::before { content: ''; position: absolute; left: 1rem; right: 1rem; top: 2.65rem; height: 2px; background: linear-gradient(90deg, var(--border-2), var(--accent-2) 50%, var(--accent)); z-index: 0; }
.tb-tl-node { position: relative; z-index: 1; width: 2.7rem; height: 2.7rem; border-radius: 50%; background: var(--surface); border: 1px solid var(--border-2); display: flex; align-items: center; justify-content: center; margin: 0.35rem 0 0.2rem 0; }
.tb-tl-node.on { background: var(--accent); border-color: var(--accent); box-shadow: 0 0 0 6px var(--accent-soft); } .tb-tl-node i { font-style: normal; font-size: 1.05rem; font-weight: 600; font-variant-numeric: tabular-nums; color: var(--text-2); } .tb-tl-node.on i { color: var(--on-accent); }
.tb-tl-label { font-size: 1.05rem; font-weight: 500; letter-spacing: -0.02em; margin: 0.5rem 0 0 0; }
.tb-tl-stem { width: 1.5px; height: 1.1rem; margin: 0.3rem 0 0.2rem 1.3rem; background: var(--border-2); }
.tb-tl-empty { font-size: 0.8rem; color: var(--muted); padding: 0.5rem 0.2rem; }
[class*="st-key-tlc_"] { background: var(--surface); border: 1px solid var(--border); border-radius: 24px; padding: 0.9rem 1rem 0.9rem 1rem; margin-bottom: 0.8rem; box-shadow: var(--shadow); }
.tb-tc-top { display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; } .tb-tc-top b { font-size: 0.98rem; letter-spacing: -0.02em; line-height: 1.2; }
.tb-tc-sub { font-size: 0.74rem; color: var(--muted); margin: 0.25rem 0 0.7rem 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.tb-tc-next { font-size: 0.82rem; line-height: 1.35; padding: 0.55rem 0.75rem; border-radius: 14px; background: var(--surface-2); } .tb-tc-due { font-size: 0.74rem; margin: 0.45rem 0 0.5rem 0.2rem; }
[class*="st-key-tlc_"] .stButton button { padding: 0.35rem 0.6rem; font-size: 0.82rem; }
.tb-tc-top .tb-score { white-space: nowrap; flex: none; min-width: 2.6rem; padding: 0.12rem 0.55rem; }
[class*="st-key-tlc_"] .stButton button { white-space: nowrap; overflow: visible; }
[class*="st-key-tlc_"] [data-testid="stHorizontalBlock"] { gap: 0.4rem; } [class*="st-key-tlc_"] [data-testid="stColumn"]:nth-child(-n+2) button { padding: 0.35rem 0 !important; min-width: 2.2rem; }
.tb-tc-top { flex-wrap: wrap; } .tb-tc-top b { flex: 1 1 6rem; min-width: 0; } .tb-tc-top .tb-score { flex: none !important; width: auto !important; min-width: 3rem; white-space: nowrap !important; word-break: keep-all; padding: 0.12rem 0.6rem; }
.tb-tc .tb-score { overflow-wrap: normal !important; word-break: normal !important; hyphens: none; display: inline-block; width: max-content !important; }

/* ---------- Dashboard bento (reference: weather dashboard). One frame, flat tiles, label top-left, value bottom-left. ---------- */
.st-key-dframe { background: var(--surface-3); border: 1px solid var(--border); border-radius: 38px; padding: 0.9rem; box-shadow: 0 24px 60px rgba(30,25,20,0.14); }
.st-key-dframe [data-testid="stHorizontalBlock"] { gap: 0.9rem; } .st-key-dframe [data-testid="stVerticalBlock"] { gap: 0.9rem; }
.tb-bt, .st-key-bt_hero, .st-key-bt_high, .st-key-bt_list { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 26px !important; box-shadow: none !important; padding: 1.1rem 1.2rem 1.1rem 1.2rem; -webkit-backdrop-filter: none; backdrop-filter: none; }
.st-key-bt_high { background: transparent !important; border: none !important; padding: 0; } .st-key-bt_high [data-testid="stHorizontalBlock"] { margin-top: 0; }
.st-key-bt_high > div > [data-testid="stMarkdownContainer"] .tb-bt-h { display: none; }
.tb-bt { display: flex; flex-direction: column; height: 100%; min-height: 10.5rem; }
.tb-bt-h { display: flex; justify-content: space-between; align-items: baseline; font-size: 0.82rem; font-weight: 500; color: var(--text-2); margin-bottom: 0.8rem; }
.tb-bt-n { font-size: 0.72rem; color: var(--muted); font-weight: 400; }
.tb-bt-b { flex: 1; display: flex; flex-direction: column; justify-content: center; }
.tb-bt-f { margin-top: 0.8rem; font-size: 0.74rem; color: var(--muted); min-height: 1rem; }
.tb-big { font-size: 2.9rem; font-weight: 300; letter-spacing: -0.05em; line-height: 1; font-variant-numeric: tabular-nums; } .tb-big small { font-size: 0.85rem; letter-spacing: 0; color: var(--muted); margin-left: 0.3rem; font-weight: 400; }
.tb-mid { font-size: 2.1rem; font-weight: 300; letter-spacing: -0.04em; line-height: 1; font-variant-numeric: tabular-nums; } .tb-mid.bad { color: var(--alert); }
.tb-bt .tb-gauge svg { max-width: 9.5rem; margin: 0 auto; display: block; } .tb-bt .tb-gauge .tb-gnum { font-size: 1.7rem; margin-top: -2.2rem; } .tb-bt .tb-gauge .tb-muted { display: none; }
.tb-bt .tb-bg { margin: 0.9rem 0 0 0; padding: 0; } .tb-bt .tb-bg-zones { height: 1.2rem; } .tb-bt .tb-bg-axis { display: none; } .tb-bt .tb-bg-val { display: none; }
.tb-hello { font-size: 2.3rem; font-weight: 500; letter-spacing: -0.045em; line-height: 1.05; margin-top: 1.6rem; } .tb-hello-sub { font-size: 0.95rem; color: var(--muted); margin: 0.35rem 0 1.4rem 0; }
.st-key-bt_hero [data-baseweb="select"] > div { min-height: 2.6rem; }
.st-key-bt_list .tb-bt-h { margin-bottom: 0.4rem; }
.st-key-bt_list [data-baseweb="tab-list"] { background: var(--surface-3) !important; margin-bottom: 0.7rem; }
[class*="st-key-drow_"] { background: var(--surface-2); border-radius: 18px; padding: 0.65rem 0.9rem; margin-bottom: 0.5rem; }
.tb-r-t { font-size: 0.92rem; font-weight: 500; letter-spacing: -0.015em; line-height: 1.3; } .tb-r-s { font-size: 0.76rem; color: var(--muted); margin-top: 0.15rem; }
[class*="st-key-drow_"] .stButton button { padding: 0.35rem 0.6rem; font-size: 0.82rem; }
.tb-bt .tb-chart { max-height: 11rem; margin: 0; } .tb-bt .tb-legend { margin-top: 0.3rem; }
.tb-bt .tb-cal-g { gap: 4px; } .tb-bt .tb-cal-g i { font-size: 0.68rem; } .tb-cal-lg { display: inline-flex; align-items: center; gap: 0.35rem; } .tb-cal-lg i { margin-left: 0.5rem; }
.st-key-bt_hero { min-height: 22.4rem; display: flex; flex-direction: column; } .st-key-bt_hero [data-testid="stSelectbox"] { margin-top: auto; }
.tb-bt .tb-cal-g i { aspect-ratio: auto; height: 1.9rem; width: 1.9rem; margin: 0 auto; } .tb-bt .tb-cal-g { gap: 3px; }

/* ---------- Alignment pass ---------- */
.tb-tile { min-height: 10rem; } .tb-tile .tb-sub { min-height: 2.4em; }
.tb-glass { min-height: 14.6rem; display: flex; flex-direction: column; } .tb-psub { min-height: 3.9rem; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; } .tb-pfoot { margin-top: auto; padding-top: 0.6rem; }
.tb-ptitle { min-height: 3.2rem; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.st-key-herobtns { margin-left: -5rem; } .st-key-herobtns .stButton button { height: 2.9rem; padding: 0 1.2rem; }
.st-key-herobtns [data-testid="stHorizontalBlock"] { align-items: center; }
[data-testid="stRadio"] [role="radiogroup"] { flex-wrap: nowrap; gap: 1rem; } [data-testid="stRadio"] label { white-space: nowrap; }
.tb-tile { min-height: 11rem; } [data-testid="stRadio"] [role="radiogroup"] { gap: 0.8rem; } [data-testid="stRadio"] label p { font-size: 0.88rem; }

/* =================== LIQUID GLASS, platform-wide ===================
   One recipe everywhere: translucent theme surface, strong blur + saturation, bright rim, soft shadow. Opacity stays high so text keeps full contrast. */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]), .tb-tile, .tb-step, .tb-block, .tb-fact, [data-testid="stExpander"], [data-testid="stMetric"], .tb-bt,
.st-key-bt_hero, .st-key-bt_list, .st-key-tlhead, [class*="st-key-tlc_"], .st-key-consentlink [data-testid="stPageLink-NavLink"] {
  background: linear-gradient(135deg, var(--glass-a), var(--glass-b)) !important; border: 1px solid var(--glass-rim) !important;
  -webkit-backdrop-filter: blur(26px) saturate(170%) !important; backdrop-filter: blur(26px) saturate(170%) !important;
  box-shadow: 0 12px 34px rgba(30,25,40,0.10), inset 0 1.5px 0 var(--glass-hi), inset 0 -1px 0 rgba(255,255,255,0.08) !important; }
.st-key-dframe, .st-key-tlpanel { background: linear-gradient(135deg, var(--glass-b), rgba(255,255,255,0.10)) !important; border: 1px solid var(--glass-rim) !important;
  -webkit-backdrop-filter: blur(30px) saturate(170%); backdrop-filter: blur(30px) saturate(170%); box-shadow: 0 24px 60px rgba(30,25,40,0.14), inset 0 1.5px 0 var(--glass-hi) !important; }
.st-key-topbar, .st-key-bottomnav { -webkit-backdrop-filter: blur(26px) saturate(180%); backdrop-filter: blur(26px) saturate(180%); box-shadow: 0 14px 38px rgba(20,16,30,0.18), inset 0 1.5px 0 var(--glass-hi); }
.st-key-topbar { background: linear-gradient(135deg, var(--glass-a), var(--glass-b)) !important; border-color: var(--glass-rim) !important; }
.st-key-bottomnav { background: linear-gradient(135deg, rgba(40,42,48,0.72), rgba(30,32,38,0.62)) !important; border-color: rgba(255,255,255,0.18) !important; }
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div { background: var(--glass-b) !important; border: 1px solid var(--glass-rim) !important; -webkit-backdrop-filter: blur(16px); backdrop-filter: blur(16px); box-shadow: inset 0 1px 0 var(--glass-hi) !important; }
[data-baseweb="popover"] > div, [data-baseweb="menu"] { background: linear-gradient(135deg, var(--glass-a), var(--glass-b)) !important; -webkit-backdrop-filter: blur(26px) saturate(170%); backdrop-filter: blur(26px) saturate(170%); border: 1px solid var(--glass-rim) !important; box-shadow: 0 18px 48px rgba(20,16,30,0.22), inset 0 1.5px 0 var(--glass-hi) !important; }
.stButton button:not([kind="primary"]), .stFormSubmitButton button:not([kind="primaryFormSubmit"]), .stDownloadButton button { background: var(--glass-b) !important; border: 1px solid var(--glass-rim) !important; -webkit-backdrop-filter: blur(14px); backdrop-filter: blur(14px); box-shadow: inset 0 1px 0 var(--glass-hi) !important; }
.stButton button[kind="primary"] { box-shadow: 0 8px 22px rgba(0,0,0,0.18), inset 0 1.5px 0 rgba(255,255,255,0.35) !important; }
[data-testid="stButtonGroup"], [data-baseweb="tab-list"] { background: var(--glass-b) !important; border: 1px solid var(--glass-rim) !important; -webkit-backdrop-filter: blur(16px); backdrop-filter: blur(16px); box-shadow: inset 0 1px 0 var(--glass-hi); }
.tb-tag, .tb-pill, .tb-score.mid { background: var(--glass-b) !important; border: 1px solid var(--glass-rim); box-shadow: inset 0 1px 0 var(--glass-hi); }
.tb-block, .tb-fact, .tb-tc-next, [class*="drow_"] { background: var(--glass-b) !important; box-shadow: inset 0 1px 0 var(--glass-hi) !important; -webkit-backdrop-filter: none !important; backdrop-filter: none !important; border-color: var(--glass-rim) !important; }

/* =================== Liquid glass, readability pass ===================
   Rule: glass is for containers (frames, tiles, bars). Anything inside a glass container (rows, buttons, inputs) is SOLID, so text never sits on blur-on-blur. */
.st-key-bottomnav { background: var(--dock-bg) !important; border-color: rgba(255,255,255,0.22) !important; }
.st-key-bottomnav [data-testid="stPageLink-NavLink"] p { color: #FFFFFF !important; opacity: 0.92; }
[class*="drow_"], .tb-tc-next, .tb-block, .tb-fact { background: var(--row-bg) !important; border: 1px solid var(--border) !important; box-shadow: none !important; }
.stButton button:not([kind="primary"]), .stFormSubmitButton button:not([kind="primaryFormSubmit"]), .stDownloadButton button { background: var(--btn-bg) !important; border: 1px solid var(--border-2) !important; color: var(--text) !important; -webkit-backdrop-filter: none; backdrop-filter: none; box-shadow: 0 1px 2px rgba(0,0,0,0.08) !important; }
.stButton button:not([kind="primary"]) p { color: var(--text) !important; }
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div { background: var(--btn-bg) !important; border: 1px solid var(--border-2) !important; box-shadow: none !important; -webkit-backdrop-filter: none; backdrop-filter: none; }
[data-testid="stButtonGroup"], [data-baseweb="tab-list"] { background: var(--row-bg) !important; box-shadow: none !important; }
.tb-tag, .tb-pill { background: var(--row-bg) !important; border: 1px solid var(--border) !important; box-shadow: none !important; }
/* liquid highlight: a soft specular sheen across the top-left of every glass container (decorative, under the text) */
.tb-bt, [data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]), .st-key-tlhead, .tb-tile { background-image: radial-gradient(120% 70% at 0% 0%, rgba(255,255,255,0.35), transparent 55%), linear-gradient(135deg, var(--glass-a), var(--glass-b)) !important; }
.st-key-dframe, .st-key-tlpanel { background-image: radial-gradient(90% 40% at 8% 0%, rgba(255,255,255,0.30), transparent 60%), linear-gradient(135deg, var(--glass-b), rgba(255,255,255,0.12)) !important; }
.tb-bt-n, .tb-bt-f, .tb-muted, .tb-r-s, .tb-tc-sub { color: var(--muted) !important; }
.tb-hello-sub { color: var(--text-2) !important; }

/* =================== Liquid glass, material pass (refs: glass switch + glass interface kit) ===================
   Thick glass: cool thin rim on top, bright caught-light line along the bottom edge, soft inner glow, deep soft drop shadow. */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]), .tb-tile, .tb-step, [data-testid="stExpander"], [data-testid="stMetric"], .tb-bt,
.st-key-bt_hero, .st-key-bt_list, .st-key-tlhead, [class*="st-key-tlc_"], .st-key-topbar, .st-key-dframe, .st-key-tlpanel {
  border: 1px solid var(--glass-rim) !important; border-top-color: var(--lg-top) !important; border-bottom-color: var(--lg-bot) !important;
  box-shadow: 0 18px 40px var(--lg-drop), 0 2px 6px rgba(0,0,0,0.06), inset 0 1px 0 var(--lg-top), inset 0 -2px 0 var(--lg-bot), inset 0 0 26px var(--lg-glow) !important; }
.st-key-bottomnav { box-shadow: 0 18px 40px rgba(0,0,0,0.30), inset 0 1px 0 rgba(255,255,255,0.28), inset 0 -2px 0 rgba(255,255,255,0.32), inset 0 0 20px rgba(255,255,255,0.06) !important; }
/* pill switch: recessed track, raised glass thumb (ref 1) */
[data-testid="stButtonGroup"], [data-baseweb="tab-list"] { padding: 4px !important; border: 1px solid var(--glass-rim) !important; border-bottom-color: var(--lg-bot) !important; box-shadow: inset 0 2px 6px rgba(0,0,0,0.12), inset 0 -1.5px 0 var(--lg-bot), 0 8px 18px var(--lg-drop) !important; }
[data-testid="stButtonGroup"] button[kind="segmented_controlActive"], [data-testid="stButtonGroup"] button[aria-checked="true"], [data-baseweb="tab"][aria-selected="true"] {
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.28), inset 0 -8px 14px rgba(0,0,0,0.18), 0 3px 8px rgba(0,0,0,0.22) !important; }
/* round glass icon buttons (ref 2) */
[data-testid="stPopover"] button, .st-key-themebtn button { background: var(--btn-bg) !important; border: 1px solid var(--glass-rim) !important; border-bottom-color: var(--lg-bot) !important; box-shadow: 0 6px 14px var(--lg-drop), inset 0 1px 0 var(--lg-top), inset 0 -1.5px 0 var(--lg-bot) !important; }
.stButton button:not([kind="primary"]) { border-bottom-color: var(--lg-bot) !important; box-shadow: 0 4px 10px var(--lg-drop), inset 0 1px 0 var(--lg-top), inset 0 -1.5px 0 var(--lg-bot) !important; }
.stButton button[kind="primary"] { box-shadow: 0 8px 20px var(--lg-drop), inset 0 1px 0 rgba(255,255,255,0.45), inset 0 -2px 0 rgba(255,255,255,0.28) !important; }
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div { box-shadow: inset 0 2px 5px rgba(0,0,0,0.08), inset 0 -1.5px 0 var(--lg-bot) !important; }
/* rows: enough room for two lines of text + sub line */
[class*="st-key-drow_"] { padding: 0.8rem 0.95rem !important; min-height: 4.6rem; display: flex; flex-direction: column; justify-content: center; }
.tb-r-s { line-height: 1.35; }
[class*="st-key-drow_"] [data-testid="stElementContainer"], [class*="st-key-drow_"] [data-testid="stMarkdown"] { flex-shrink: 0; height: auto !important; min-height: fit-content; }
[class*="st-key-drow_"] [data-testid="stColumn"] { min-height: fit-content; }
[class*="st-key-drow_"] { min-height: 5.8rem !important; }
[class*="st-key-drow_"] .tb-r-s { padding-bottom: 0.2rem; }
[class*="st-key-drow_"] { min-height: 4.9rem !important; } [class*="st-key-drow_"] .tb-r-t, [class*="st-key-drow_"] .tb-r-s { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%; }
[data-baseweb="tab"][aria-selected="true"], [data-baseweb="tab"][aria-selected="true"] p { color: var(--accent-ink) !important; }
.tb-note { color: var(--text); } .tb-overdue { color: var(--alert); }

/* ---- contrast fixes found by the pixel audit ---- */
.tb-peek { background: var(--peek-bg, rgba(20,28,40,0.62)) !important; } .tb-peek b, .tb-peek span { color: #FFFFFF !important; }
.st-key-herobtns [data-testid="stColumn"]:nth-child(2) button { background: rgba(18,22,26,0.78) !important; color: #fff !important; } .st-key-herobtns [data-testid="stColumn"]:nth-child(2) button p { color: #fff !important; }
.tb-glass { background: rgba(12,18,32,0.66) !important; } .tb-pshade { background: linear-gradient(180deg, rgba(6,10,24,0.62) 0%, rgba(6,10,24,0.12) 28%, rgba(6,10,24,0) 50%, rgba(6,10,24,0.6) 100%) !important; }
.tb-pchip { background: rgba(10,14,28,0.58) !important; border-color: rgba(255,255,255,0.4) !important; color: #fff !important; } .tb-pk, .tb-pstage { color: #fff !important; text-shadow: 0 1px 8px rgba(0,0,0,0.55); }
.tb-bm.hi { background: var(--bm-hi) !important; }
.tb-bm.mid { background: var(--bm-mid) !important; }
.st-key-brtop { background: rgba(10,16,32,0.86) !important; } .st-key-brtop button { background: rgba(255,255,255,0.16) !important; color: #fff !important; } .st-key-brtop button *, .st-key-brpanel .stButton button * { color: #fff !important; }
.st-key-brpanel { background: rgba(10,16,32,0.80) !important; } .st-key-brleg { background: rgba(10,16,32,0.82) !important; }
.tb-bm-s, .tb-bm-t { color: #fff !important; opacity: 1; } .tb-bm-s { opacity: 0.92; }
button[role="tab"][aria-selected="true"], button[role="tab"][aria-selected="true"] *, [data-testid="stTab"][aria-selected="true"], [data-testid="stTab"][aria-selected="true"] * { color: var(--accent-ink) !important; }
button[role="tab"][aria-selected="false"], button[role="tab"][aria-selected="false"] * { color: var(--text-2) !important; }
button[role="tab"][aria-selected="true"]::after, [data-baseweb="tab-highlight"] { background-color: var(--accent) !important; }
.stApp [class*="st-key-poster_edit_"] button { background: #FFFFFF !important; color: #0A1636 !important; border: none !important; box-shadow: 0 6px 18px rgba(0,0,0,0.25) !important; }
.stApp [class*="st-key-poster_edit_"] button p { color: #0A1636 !important; }
.stApp [class*="st-key-bmb_"] button { background: transparent !important; border: none !important; box-shadow: none !important; backdrop-filter: none !important; -webkit-backdrop-filter: none !important; padding: 0.2rem 0 !important; }
.stApp .st-key-herobtns [data-testid="stColumn"]:nth-child(1) button { background: #FFFFFF !important; border: none !important; color: #15181C !important; } .stApp .st-key-herobtns [data-testid="stColumn"]:nth-child(1) button p { color: #15181C !important; }
.stApp [class*="st-key-bmb_"] button, .stApp [class*="st-key-bmb_"] button p, .stApp [class*="st-key-bmb_"] button span { color: #FFFFFF !important; }
.stApp [class*="st-key-bmb_"] button { text-shadow: 0 1px 6px rgba(0,0,0,0.55); border-bottom: 1px solid rgba(255,255,255,0.6) !important; border-radius: 0 !important; }
.tb-bm.lo { background: var(--bm-lo) !important; }
.tb-bg-mark span { color: var(--accent-2) !important; } .tb-bg-mark b { background: var(--accent-2) !important; }

/* ---------- Why Trustpont: the Culture > Trust > Value loop ---------- */
.tb-cycle { display: grid; grid-template-columns: 1.05fr 1fr; gap: 3rem; align-items: center; margin: 3.5rem 0 3rem 0; padding: 2.4rem 2.6rem; border-radius: 34px; background: linear-gradient(135deg, var(--glass-a), var(--glass-b)); border: 1px solid var(--glass-rim); box-shadow: var(--shadow); }
.tb-cycle h2 { margin: 0.3rem 0 1.4rem 0; font-size: 2rem !important; letter-spacing: -0.04em; }
.cy-i { display: grid; grid-template-columns: 2rem 1fr; gap: 0.9rem; align-items: start; padding: 0.85rem 0; border-top: 1px solid var(--border); }
.cy-i i { font-style: normal; width: 2rem; height: 2rem; border-radius: 50%; background: var(--accent); color: var(--on-accent); display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 600; }
.cy-i b { display: block; font-size: 1.05rem; letter-spacing: -0.02em; margin-bottom: 0.15rem; } .cy-i span { font-size: 0.92rem; line-height: 1.5; color: var(--text-2); }
.tb-cy { width: 100%; max-width: 25rem; display: block; margin: 0 auto; }
.tb-cy .cy-arc { fill: none; stroke: var(--accent); stroke-width: 2; stroke-dasharray: 4 7; animation: tbFlow 3.2s linear infinite; }
.tb-cy .cy-ah { fill: none; stroke: var(--accent); stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
.tb-cy .cy-h { fill: var(--accent-soft); } .tb-cy .cy-c { fill: var(--accent); }
.tb-cy .cy-t { fill: var(--on-accent); font-size: 15px; font-weight: 600; letter-spacing: -0.01em; }
.tb-cy .cy-mid { fill: var(--text); font-size: 15px; font-weight: 600; } .tb-cy .cy-mid2 { fill: var(--muted); font-size: 11px; }
@media (max-width: 800px) { .tb-cycle { grid-template-columns: 1fr; padding: 1.6rem 1.3rem; gap: 1.5rem; } }

/* ---------- Small screens: stack everything, no fixed heights, nothing overlaps ---------- */
@media (max-width: 900px) {
  .tb-bt { height: auto !important; min-height: 0 !important; }
  .st-key-dframe [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
  .st-key-dframe [data-testid="stColumn"] { min-width: calc(50% - 0.6rem) !important; flex: 1 1 calc(50% - 0.6rem) !important; width: auto !important; }
  .st-key-dframe > div > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:only-child, .st-key-bt_hero, .st-key-bt_list { min-width: 100% !important; }
  .st-key-bt_hero { min-height: 0 !important; }
  .block-container { padding-left: 0.8rem !important; padding-right: 0.8rem !important; padding-bottom: 8rem !important; }
  .st-key-dframe { padding: 0.5rem; border-radius: 28px; }
  .tb-tc, [class*="st-key-tlc_"] { min-width: 0; }
  .st-key-tlpanel [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; } .st-key-tlpanel [data-testid="stColumn"] { min-width: 100% !important; }
  .st-key-tlpanel::before { display: none; }
}
@media (max-width: 520px) { .st-key-dframe [data-testid="stColumn"] { min-width: 100% !important; flex-basis: 100% !important; } }
.tb-bt { box-sizing: border-box; } .st-key-bt_high > div[data-testid="stVerticalBlock"] { row-gap: 0.9rem; }
.st-key-dframe [data-testid="stColumn"] [data-testid="stElementContainer"]:has(> [data-testid="stMarkdown"] .tb-bt) { margin-bottom: 0; }
.st-key-dframe [data-testid="stColumn"] > [data-testid="stVerticalBlock"] { row-gap: 0.9rem; }
@media (max-width: 700px) {
  .st-key-bottomnav { width: 96vw !important; padding: 0.3rem 0.35rem; } .st-key-bottomnav [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 0.1rem !important; }
  .st-key-bottomnav [data-testid="stColumn"] { min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; } .st-key-bottomnav [data-testid="stPageLink-NavLink"] { padding: 0.55rem 0.1rem; } .st-key-bottomnav [data-testid="stPageLink-NavLink"] p { font-size: 0.74rem !important; }
  .st-key-topbar [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; } .st-key-topbar [data-testid="stColumn"] { min-width: 0 !important; } .tb-topc b { font-size: 1.05rem; } .st-key-topbar { padding: 0.3rem 0.5rem; }
}
[data-testid="stMarkdownContainer"]:has(> .tb-bt), [data-testid="stMarkdownContainer"]:has(> .tb-tile) { margin-bottom: 0 !important; }
.tb-bt { height: auto; }

.tb-photo, .tb-bm-img { background-color: var(--photo-tint); background-blend-mode: luminosity; }
.tb-overdue { color: var(--alert) !important; text-decoration: underline; text-decoration-thickness: 1.5px; text-underline-offset: 3px; font-weight: 700; }
.tb-wl { color: var(--text-2) !important; }
.tb-bg-mark span { color: var(--accent-ink) !important; } .tb-bg-mark b { background: var(--accent-ink) !important; }

/* =================== Buttons: soft glass pills (ref: "Get Started") ===================
   Gentle top-to-bottom gradient, hairline rim with bright top and bottom edges, soft drop shadow, firm label. Hover lifts, press sinks. */
.stApp .stButton button, .stApp .stDownloadButton button, .stApp .stFormSubmitButton button, .stApp [data-testid="stPageLink-NavLink"].tb-btnlink {
  border-radius: 999px !important; min-height: 2.75rem; padding: 0 1.35rem !important; font-weight: 600; letter-spacing: -0.005em; line-height: 1;
  display: inline-flex; align-items: center; justify-content: center; text-align: center;
  transition: transform .16s cubic-bezier(.2,.7,.2,1), box-shadow .16s ease, background .16s ease; }
.stApp .stButton button:not([kind="primary"]), .stApp .stFormSubmitButton button:not([kind="primaryFormSubmit"]), .stApp .stDownloadButton button {
  background: var(--btn-grad) !important; border: 1px solid var(--border-2) !important; border-top-color: var(--lg-top) !important; border-bottom-color: var(--lg-bot) !important;
  box-shadow: 0 10px 22px var(--lg-drop), 0 1px 2px rgba(0,0,0,0.08), inset 0 1px 0 var(--lg-top), inset 0 -1px 0 var(--lg-bot) !important; }
.stApp .stButton button:not([kind="primary"]):hover, .stApp .stFormSubmitButton button:not([kind="primaryFormSubmit"]):hover, .stApp .stDownloadButton button:hover {
  background: var(--btn-grad-h) !important; transform: translateY(-1px); box-shadow: 0 14px 26px var(--lg-drop), 0 1px 2px rgba(0,0,0,0.1), inset 0 1px 0 var(--lg-top), inset 0 -1px 0 var(--lg-bot) !important; }
.stApp .stButton button[kind="primary"], .stApp .stFormSubmitButton button[kind="primaryFormSubmit"] {
  background: var(--pbtn-grad) !important; border: 1px solid rgba(255,255,255,0.22) !important; border-bottom-color: rgba(255,255,255,0.40) !important; color: var(--pbtn-text) !important;
  box-shadow: 0 12px 24px var(--lg-drop), 0 1px 2px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.35), inset 0 -1px 0 rgba(255,255,255,0.18) !important; }
.stApp .stButton button[kind="primary"]:hover, .stApp .stFormSubmitButton button[kind="primaryFormSubmit"]:hover { background: var(--pbtn-grad-h) !important; transform: translateY(-1px); }
.stApp .stButton button:active, .stApp .stFormSubmitButton button:active { transform: translateY(1px) scale(0.985); box-shadow: 0 3px 8px var(--lg-drop), inset 0 2px 4px rgba(0,0,0,0.12) !important; }
.stApp .stButton button:focus-visible, .stApp .stFormSubmitButton button:focus-visible { outline: 2px solid var(--accent-2); outline-offset: 2px; }
.stApp .stButton button:disabled { opacity: 0.45; }
.stApp .stButton button p, .stApp .stFormSubmitButton button p { margin: 0; line-height: 1; white-space: nowrap; }
.stApp [class*="st-key-poster_edit_"] button { background: #FFFFFF !important; }
.stApp [class*="st-key-tlc_"] .stButton button, .stApp [class*="st-key-drow_"] .stButton button { min-height: 2.25rem; padding: 0 0.5rem !important; font-size: 0.82rem; }
.stApp [class*="st-key-tlc_"] [data-testid="stColumn"]:nth-child(-n+2) .stButton button { padding: 0 !important; width: 100%; }
.stApp [class*="st-key-poster_edit_"] button { min-height: 2.9rem; padding: 0 2.3rem !important; }
.stApp [class*="st-key-dbtw_"] button, .stApp [class*="st-key-dbtn_"] button { padding: 0 !important; min-height: 0; }
.stApp .st-key-herobtns .stButton button { min-height: 2.9rem; padding: 0 1.2rem !important; }
.stApp .stButton button[kind="primary"] { letter-spacing: 0; }
.tb-cal-w span, .tb-bt .tb-cal-g i { font-size: 0.72rem !important; } .tb-bg-mark span { font-size: 0.72rem !important; }
.tb-blocks { grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr)) !important; } .tb-block.wide { grid-column: 1 / -1; }
.tb-facts, .tb-facts.three { grid-template-columns: repeat(auto-fit, minmax(6.2rem, 1fr)) !important; } .tb-fv { overflow-wrap: break-word; word-break: normal; hyphens: none; }

/* ---------- Mid-width layouts: the 5-stage timeline wraps instead of squeezing cards; legend dots; no ellipsis on button labels ---------- */
@media (max-width: 1260px) {
  .st-key-tlpanel [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; row-gap: 1.2rem; }
  .st-key-tlpanel [data-testid="stColumn"] { min-width: 13.5rem !important; flex: 1 1 13.5rem !important; width: auto !important; }
  .st-key-tlpanel::before { display: none; }
}
.stApp .stButton button p { overflow: visible !important; text-overflow: clip !important; }
.tb-cal-lg { display: inline-flex; align-items: center; gap: 0.4rem; } .tb-cal-lg i { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin: 0 0 0 0.6rem; box-sizing: border-box; }
.tb-cal-lg i:first-child { margin-left: 0; } .tb-cal-lg i.due { background: var(--accent-soft); box-shadow: inset 0 0 0 1.5px var(--accent-2); } .tb-cal-lg i.tod { background: var(--accent); }
[class*="st-key-tlc_"] [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; row-gap: 0; gap: 0.4rem !important; }
[class*="st-key-tlc_"] [data-testid="stColumn"] { min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; }
[class*="st-key-tlc_"] [data-testid="stColumn"]:nth-child(-n+2) { flex: 0 0 2.5rem !important; }

@media (max-width: 700px) {
  .tb-who > div:last-child { display: none; } .tb-av2 { width: 2.1rem; height: 2.1rem; }
  .st-key-topbar [data-testid="stButtonGroup"] button { padding: 0 0.55rem !important; font-size: 0.78rem; min-height: 2rem; }
  .st-key-topbar [data-testid="stHorizontalBlock"] { gap: 0.3rem !important; }
  .st-key-topbar [data-testid="stColumn"]:nth-child(3) { flex: 2.4 1 0 !important; }
  .tb-topc b { font-size: 0.98rem; }
  .st-key-themebtn button, .st-key-topbar [data-testid="stPopover"] button { width: 2.1rem !important; height: 2.1rem !important; min-height: 0 !important; padding: 0 !important; }
}

@media (max-width: 700px) {
  .st-key-topbar > div > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(1) { flex: 0 0 2.4rem !important; min-width: 0 !important; }
  .st-key-topbar > div > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) { flex: 1 1 0 !important; min-width: 0 !important; }
  .st-key-topbar > div > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(3) { flex: 0 0 auto !important; min-width: 0 !important; width: auto !important; }
  .st-key-topbar [data-testid="stColumn"]:nth-child(3) [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] { flex: 0 0 auto !important; width: auto !important; min-width: 0 !important; }
  .st-key-topbar [data-testid="stButtonGroup"] { margin-left: 0; } .st-key-topbar [data-testid="stButtonGroup"] button { padding: 0 0.45rem !important; font-size: 0.72rem; }
  .tb-topc b::after { display: none; }
}

/* =================== Readability fixes from the deep audit (both themes) =================== */
/* special buttons keep their own skin (the generic glass-pill rule must not repaint them) */
.stApp [class*="st-key-poster_edit_"] .stButton button, .stApp [class*="st-key-poster_edit_"] .stButton button:hover { background: #FFFFFF !important; border: none !important; color: #0A1F1F !important; box-shadow: 0 6px 18px rgba(0,0,0,0.25) !important; }
.stApp [class*="st-key-poster_edit_"] .stButton button p { color: #0A1F1F !important; }
.stApp [class*="st-key-bmb_"] .stButton button, .stApp [class*="st-key-bmb_"] .stButton button:hover { background: transparent !important; border: none !important; border-bottom: 1px solid rgba(255,255,255,0.7) !important; border-radius: 0 !important; box-shadow: none !important; min-height: 0; padding: 0.2rem 0 !important; transform: none; }
.stApp [class*="st-key-bmb_"] .stButton button p { color: #FFFFFF !important; }
.stApp .st-key-herobtns [data-testid="stColumn"]:nth-child(1) .stButton button, .stApp .st-key-herobtns [data-testid="stColumn"]:nth-child(1) .stButton button:hover { background: #FFFFFF !important; border: none !important; }
.stApp .st-key-herobtns [data-testid="stColumn"]:nth-child(1) .stButton button p { color: #10201F !important; }
.stApp .st-key-herobtns [data-testid="stColumn"]:nth-child(2) .stButton button, .stApp .st-key-herobtns [data-testid="stColumn"]:nth-child(2) .stButton button:hover { background: rgba(14,22,24,0.80) !important; border: 1px solid rgba(255,255,255,0.5) !important; box-shadow: none !important; }
.stApp .st-key-herobtns [data-testid="stColumn"]:nth-child(2) .stButton button p { color: #FFFFFF !important; }
.stApp .st-key-brpanel .stButton button:not([kind="primary"]), .stApp .st-key-brpanel .stButton button:not([kind="primary"]):hover { background: rgba(255,255,255,0.16) !important; border: 1px solid rgba(255,255,255,0.3) !important; box-shadow: none !important; }
.stApp .st-key-brpanel .stButton button p { color: #FFFFFF !important; }
.stApp .stButton button[kind="primary"] p, .stApp .stFormSubmitButton button[kind="primaryFormSubmit"] p { color: var(--pbtn-text) !important; }
.stApp .stButton button:disabled { opacity: 1 !important; } .stApp .stButton button:disabled p { color: var(--muted) !important; opacity: 0.85; }
/* popovers and menus live outside the page flow: give them the theme surface and text explicitly */
[data-testid="stPopoverBody"], [data-baseweb="popover"] [data-testid="stVerticalBlock"] { background: var(--surface) !important; color: var(--text) !important; }
[data-testid="stPopoverBody"] *, [data-baseweb="popover"] li, [data-baseweb="popover"] [role="option"], [data-baseweb="popover"] [role="option"] * { color: var(--text) !important; }
[data-testid="stPopoverBody"] .tb-muted, [data-testid="stPopoverBody"] [data-testid="stCaptionContainer"] * { color: var(--muted) !important; }
[data-baseweb="popover"] ul, [data-baseweb="popover"] [role="listbox"] { background: var(--surface) !important; }
[data-baseweb="popover"] [role="option"]:hover, [data-baseweb="popover"] [role="option"][aria-selected="true"] { background: var(--surface-3) !important; }
/* slider end labels, thumb value, captions, placeholders */
[data-testid="stSliderTickBarMin"], [data-testid="stSliderTickBarMax"], [data-testid="stSliderTickBar"] * { color: var(--muted) !important; background: transparent !important; }
[data-testid="stSliderThumbValue"] { color: var(--text) !important; }
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] p { color: var(--muted) !important; opacity: 1 !important; }
.stApp input::placeholder, .stApp textarea::placeholder { color: var(--muted) !important; opacity: 1; }
.stApp [data-baseweb="select"] [data-baseweb="tag"] span, .stApp [data-baseweb="tag"] * { color: var(--on-strong) !important; }
.stApp .stButton button[kind="primary"]:disabled, .stApp .stFormSubmitButton button[kind="primaryFormSubmit"]:disabled { background: var(--surface-3) !important; border: 1px solid var(--border-2) !important; box-shadow: none !important; }
.stApp .stButton button[kind="primary"]:disabled p { color: var(--text-2) !important; opacity: 1; }
.stApp .stButton button:disabled p { color: var(--text-2) !important; opacity: 1; }
.stApp .stButton button:disabled { background: var(--surface-3) !important; box-shadow: none !important; cursor: not-allowed; }

/* =================== Form fields (this Streamlit renders them with react-aria, not baseweb) ===================
   The field shell takes the theme surface; the inner input is transparent with theme text, so text is never white-on-white. */
[data-testid="stTextAreaRootElement"], [data-testid="stTextInputRootElement"], [data-testid="stNumberInputContainer"],
[data-testid="stSelectbox"] [role="group"], [data-testid="stMultiSelect"] [role="group"]:not(span), [data-testid="stDateInput"] [role="group"], [data-testid="stDateInputContainer"] {
  background: var(--btn-bg) !important; border: 1px solid var(--border-2) !important; color: var(--text) !important; box-shadow: inset 0 1px 3px rgba(0,0,0,0.08) !important; }
[data-testid="stSelectbox"] [role="group"], [data-testid="stMultiSelect"] [role="group"]:not(span) { border-radius: 999px !important; }
[data-testid="stMultiSelectTagsContainer"] [role="group"] { background: transparent !important; border: none !important; box-shadow: none !important; }
.stApp textarea, .stApp input[type="text"], .stApp input[type="password"], .stApp input[type="number"], .stApp input[role="combobox"], .stApp [data-testid="stDateInput"] input {
  background: transparent !important; color: var(--text) !important; -webkit-text-fill-color: var(--text) !important; caret-color: var(--text); }
.stApp [data-testid="stSelectbox"] button, .stApp [data-testid="stMultiSelect"] button, .stApp [data-testid="stSelectbox"] svg, .stApp [data-testid="stMultiSelect"] svg, .stApp [data-testid="stNumberInputContainer"] button { color: var(--text-2) !important; fill: currentColor; background: transparent !important; }
[data-testid="stTextAreaRootElement"]:focus-within, [data-testid="stTextInputRootElement"]:focus-within, [data-testid="stSelectbox"] [role="group"]:focus-within, [data-testid="stMultiSelect"] [role="group"]:not(span):focus-within { border-color: var(--accent-2) !important; box-shadow: 0 0 0 3px var(--accent-soft) !important; }
[data-testid="stMultiSelectTagsContainer"] [role="group"] > span { background: var(--accent) !important; color: var(--on-accent) !important; border-radius: 999px !important; }
[data-testid="stMultiSelectTagsContainer"] [role="group"] > span * { color: var(--on-accent) !important; fill: var(--on-accent) !important; }
/* dropdown lists (rendered at the end of <body>) */
[data-testid*="VirtualDropdown"], [data-testid*="Dropdown"][data-rac], [role="listbox"] { background: var(--surface) !important; color: var(--text) !important; border: 1px solid var(--border-2) !important; border-radius: 16px !important; box-shadow: var(--menu-shadow) !important; }
[role="listbox"] { border: none !important; box-shadow: none !important; }
[role="option"], [role="option"] * { color: var(--text) !important; }
[role="option"] [data-item-hl], [role="option"][data-focused] > div, [role="option"][aria-selected="true"] > div { background: var(--surface-3) !important; }
[data-testid="stDateInput"] [role="dialog"], [data-baseweb="calendar"], [role="dialog"][data-rac] { background: var(--surface) !important; color: var(--text) !important; }
[role="dialog"][data-rac] * { color: var(--text) !important; }

/* fields inside popovers/dialogs are outside .stApp: same rules without the page prefix */
textarea, input[type="text"], input[type="password"], input[type="number"], input[role="combobox"] { background: transparent !important; color: var(--text) !important; -webkit-text-fill-color: var(--text) !important; caret-color: var(--text); }
input::placeholder, textarea::placeholder { color: var(--text-2) !important; -webkit-text-fill-color: var(--text-2) !important; opacity: 0.9 !important; }
[data-testid="stDateInput"] *, [data-testid="stDateInput"] [role="spinbutton"], [data-testid="stDateInput"] [data-type], [role="spinbutton"] { color: var(--text) !important; -webkit-text-fill-color: var(--text) !important; }
[data-testid="stDateInput"] [role="group"] { background: var(--btn-bg) !important; border: 1px solid var(--border-2) !important; }
[data-testid="stSelectbox"] button, [data-testid="stMultiSelect"] button, [data-testid="stSelectbox"] svg, [data-testid="stMultiSelect"] svg, [data-testid="stDateInput"] button, [data-testid="stDateInput"] svg { color: var(--text-2) !important; fill: currentColor; background: transparent !important; }
[data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p { color: var(--text) !important; }
[data-testid="stCheckbox"] p, [data-testid="stRadio"] p { color: var(--text) !important; }
[role="grid"] *, [role="gridcell"] { color: var(--text) !important; }
[data-testid="stDateInput"] div, [data-testid="stDateInput"] button { background-color: transparent !important; }
[data-testid="stDateInput"] [role="group"] { background: var(--btn-bg) !important; }
[data-testid="stDateInput"] button svg { color: var(--text-2) !important; }
.stApp [class*="st-key-bmb_"] .stButton button, .stApp [class*="st-key-bmb_"] .stButton button:hover { border-top: none !important; border-left: none !important; border-right: none !important; }
.tb-avl { background: var(--accent) !important; color: var(--on-accent) !important; }

/* ---------- Profile ---------- */
.st-key-phead { margin-bottom: 1rem; }
.tb-ph { display: flex; align-items: center; gap: 1.2rem; }
.tb-ph-av { width: 4.6rem; height: 4.6rem; flex: none; border-radius: 50%; background: var(--accent); color: var(--on-accent); display: flex; align-items: center; justify-content: center; font-size: 1.9rem; font-weight: 600; box-shadow: 0 8px 20px var(--lg-drop), inset 0 1px 0 rgba(255,255,255,0.35); }
.tb-ph-n { font-size: 1.9rem; font-weight: 600; letter-spacing: -0.04em; line-height: 1.1; margin: 0.15rem 0 0.2rem 0; }
.tb-ph-chips { margin-top: 0.6rem; }
.st-key-phead .tb-ring { margin: 0 auto; } .st-key-phead .tb-ring .tb-rl { font-size: 0.62rem; }
[data-testid="stForm"] { border: none !important; padding: 0.4rem 0 0 0 !important; }
@media (max-width: 800px) { .tb-ph { flex-direction: column; align-items: flex-start; } }
.st-key-bottomnav { width: min(94vw, 42rem) !important; } .st-key-bottomnav [data-testid="stPageLink-NavLink"] { padding-left: 0.2rem; padding-right: 0.2rem; } .st-key-bottomnav [data-testid="stPageLink-NavLink"] p { font-size: 0.86rem !important; }

/* Profile header: the full train-window photo across the top, dissolving into the card surface (ref: profile card "Top").
   The photo band is 22rem tall and the text starts below it, on the solid surface, so nothing is ever drawn over the picture. */
.st-key-phead { padding: 22.5rem 1.5rem 1.2rem 1.5rem !important; overflow: hidden; border-radius: 30px;
  background-image: linear-gradient(180deg, rgba(0,0,0,0) 0, rgba(0,0,0,0) 13rem, var(--ph-fade-a) 17rem, var(--ph-fade-b) 20rem, var(--ph-solid) 22rem), var(--ph-tint), url(/app/static/profile_bg.jpg) !important;
  background-size: 100% 100%, 100% 100%, 100% auto !important; background-position: 0 0, 0 0, center top !important; background-repeat: no-repeat !important; background-color: var(--ph-solid) !important; }
.st-key-phead .tb-ph-av { border: 4px solid var(--ph-solid); }
.st-key-phead .tb-ring { margin-top: 0.4rem; }
@media (max-width: 800px) { .st-key-phead { padding-top: 14.5rem !important; background-image: linear-gradient(180deg, rgba(0,0,0,0) 0, rgba(0,0,0,0) 8rem, var(--ph-fade-a) 10.5rem, var(--ph-fade-b) 12.5rem, var(--ph-solid) 14rem), var(--ph-tint), url(/app/static/profile_bg.jpg) !important; background-size: 100% 100%, 100% 100%, 100% auto !important; } .st-key-phead .tb-ph { gap: 0.9rem; } }
@media (max-width: 700px) {
  .st-key-bottomnav { width: 97vw !important; } .st-key-bottomnav [data-testid="stPageLink-NavLink"] p { font-size: 0.68rem !important; letter-spacing: -0.01em; }
  .st-key-bottomnav [data-testid="stPageLink-NavLink"] { padding: 0.5rem 0.05rem !important; }
}
[data-testid="stTooltipIcon"] svg, [data-testid="stTooltipHoverTarget"] svg { color: var(--text-2) !important; stroke: currentColor; opacity: 1 !important; }
.tb-label { color: var(--text-2) !important; opacity: 0.92; }
</style>
"""


def current_theme():
    return st.session_state.get("theme", "warm")


def toggle_theme():
    st.session_state.theme = "azure" if current_theme() == "warm" else "warm"


def inject_css():
    theme = current_theme()
    extra = f"<style>{DARK_OVERRIDES}</style>" if theme == "azure" else ""
    st.markdown(f"<style>{THEMES[theme]}</style>{CSS}{extra}", unsafe_allow_html=True)
