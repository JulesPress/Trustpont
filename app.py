from html import escape

import streamlit as st

import ai
import store
import style

st.set_page_config(page_title="Trustpont", layout="wide", initial_sidebar_state="collapsed")
style.inject_css()
store.init()
st.session_state.setdefault("role", "research")

PAGES = {
    "research": [
        ("views/dashboard.py", "Dashboard", "dashboard"),
        ("views/my_cards.py", "My cards", "cards"),
        ("views/browse.py", "Browse business", "browse"),
        ("views/match_detail.py", "Match detail", "match"),
        ("views/pipeline.py", "Pipeline", "pipeline"),
        ("views/profile.py", "Profile", "profile"),
        ("views/consent.py", "Visibility & consent", "consent"),
    ],
    "business": [
        ("views/dashboard.py", "Dashboard", "dashboard"),
        ("views/my_cards.py", "My card", "cards"),
        ("views/browse.py", "Browse research", "browse"),
        ("views/match_detail.py", "Match detail", "match"),
        ("views/pipeline.py", "Pipeline", "pipeline"),
        ("views/profile.py", "Profile", "profile"),
    ],
}
# The dock carries only the five places you go to most. Match detail and Consent are reached from within
# the flow (opening a match, a link on My cards), and light up their parent in the dock.
SHORT = {"Home": "Home", "Dashboard": "Dashboard", "My cards": "Cards", "My card": "Card", "Browse business": "Browse",
         "Browse research": "Browse", "Pipeline": "Pipeline", "Profile": "Profile"}
PARENT = {"Match detail": "Pipeline", "Visibility & consent": "My cards"}

home = st.Page("views/landing.py", title="Home", url_path="home", default=True)
pages = [home] + [st.Page(path, title=title, url_path=url) for path, title, url in PAGES[st.session_state.role]]
current = st.navigation(pages, position="hidden")

# --- Top bar: who you are (left), the product (centre), role + settings (right) ---
persona = store.persona(st.session_state.role)
roles = ["research", "business"]
with st.container(key="topbar"):
    left, centre, right = st.columns([1, 1, 1], vertical_alignment="center", gap="small")
    left.markdown(f'<div class="tb-who"><div class="tb-av2">{escape(persona["name"][0])}</div>'
                  f'<div><div class="tb-wl">Welcome,</div><div class="tb-wn">{escape(persona["name"].split()[0])}</div></div></div>',
                  unsafe_allow_html=True)
    centre.markdown('<div class="tb-topc"><b>Trustpont</b></div>', unsafe_allow_html=True)
    with right:
        r1, rt, r2 = st.columns([4.4, 1, 1], vertical_alignment="center", gap="small")
        # Unkeyed: the landing buttons also set the role, and a keyed widget would send back its stale value
        chosen = r1.segmented_control("Role", roles, default=st.session_state.role, label_visibility="collapsed",
                                      format_func=lambda r: "Researcher" if r == "research" else "Business") or st.session_state.role
        rt.button("", icon=":material/light_mode:" if style.current_theme() == "azure" else ":material/dark_mode:",
                  key="themebtn", on_click=style.toggle_theme, help="Switch between the warm light theme and the azure dark theme")
        with r2.popover("", icon=":material/tune:"):
            st.markdown(f"**{escape(persona['name'])}**  \n"
                        f'<span class="tb-muted">{escape(persona["headline"])}</span>', unsafe_allow_html=True)
            st.page_link("views/profile.py", label="Open my profile")
            st.divider()
            ai.render_key_input()
    if chosen != st.session_state.role:
        st.session_state.role = chosen
        st.rerun()

# --- Floating dock at the bottom: every page, one tap away ---
with st.container(key="bottomnav"):
    dock = [p for p in pages if p.title in SHORT]
    cols = st.columns(len(dock), gap="small")
    for col, page in zip(cols, dock):
        col.page_link(page, label=SHORT[page.title])

# Highlight the active dock item (Streamlit exposes no active attribute on page links, so target it by position)
active_title = PARENT.get(current.title, current.title)
active = next((i for i, p in enumerate(dock) if p.title == active_title), -1)
st.markdown(f"""<style>
.st-key-bottomnav [data-testid="stHorizontalBlock"] > *:nth-child({active + 1}) [data-testid="stPageLink-NavLink"] {{
  background: var(--dock-act); }}
.st-key-bottomnav [data-testid="stHorizontalBlock"] > *:nth-child({active + 1}) [data-testid="stPageLink-NavLink"] * {{ color: var(--dock-act-text) !important; font-weight: 700; }}
</style>""", unsafe_allow_html=True)

if current.title == "Home":  # the picture runs behind the bar: make it glass
    st.markdown('<style>.st-key-topbar { background: var(--scene-glass) !important; -webkit-backdrop-filter: blur(18px) saturate(160%); backdrop-filter: blur(18px) saturate(160%); border-color: rgba(255,255,255,0.4) !important; }'
                '</style>',
                unsafe_allow_html=True)

current.run()
