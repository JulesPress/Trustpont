import streamlit as st

import ai
import store
import style

st.set_page_config(page_title="TrustBridge", layout="wide", initial_sidebar_state="expanded")
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
        ("views/consent.py", "Visibility & consent", "consent"),
    ],
    "business": [
        ("views/dashboard.py", "Dashboard", "dashboard"),
        ("views/my_cards.py", "My card", "cards"),
        ("views/browse.py", "Browse research", "browse"),
        ("views/match_detail.py", "Match detail", "match"),
        ("views/pipeline.py", "Pipeline", "pipeline"),
    ],
}

home = st.Page("views/landing.py", title="Home", url_path="home", default=True)
pages = [home] + [st.Page(path, title=title, url_path=url) for path, title, url in PAGES[st.session_state.role]]
current = st.navigation(pages, position="hidden")

with st.sidebar:
    st.markdown('<div class="tb-brand">TrustBridge</div>'
                '<div class="tb-muted">Research to business, in a language both sides read</div>',
                unsafe_allow_html=True)
    st.write("")
    # Unkeyed: the landing buttons also set the role, and a keyed radio would send back its stale value
    roles = ["research", "business"]
    chosen = st.radio("Role", roles, index=roles.index(st.session_state.role), horizontal=True,
                      format_func=lambda r: "I am a researcher" if r == "research" else "I am business")
    if chosen != st.session_state.role:
        st.session_state.role = chosen
        st.rerun()
    persona = store.persona(st.session_state.role)
    st.markdown(f"**{persona['name']}**  \n"
                f'<span class="tb-muted">{persona["headline"]}</span>', unsafe_allow_html=True)
    st.divider()
    for page in pages:
        st.page_link(page)
    st.divider()
    ai.render_key_input()

current.run()
