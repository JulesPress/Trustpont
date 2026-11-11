import streamlit as st

import model
import store
import ui


def enter(role):
    st.session_state.role = role


ui.md("""
<div class="tb-hero">
  <div class="tb-label">ENGAGE.EU Expedition+ · prototype</div>
  <h1>Research that business can read.<br>Business needs that research can answer.</h1>
  <p>PhD students rarely learn to pitch, and industry rarely has time to decode an abstract.
  Good ideas stay in the lab because the two sides do not speak the same language.</p>
</div>
""")

c1, c2, c3 = st.columns(3)
with c1, st.container(border=True):
    ui.label("1 · The card")
    st.write("Researchers publish a card in two parts: plain language first, then the business "
             "facts. Claude drafts it from an abstract; the researcher stays in control of every word.")
with c2, st.container(border=True):
    ui.label("2 · The match")
    st.write("Companies, investors, business developers, ex-founders and incubators publish what "
             "they scout for. Six explicit criteria, weighted by each side, give a score both can read.")
with c3, st.container(border=True):
    ui.label("3 · The trust")
    st.write("Cards can stay anonymous until both sides accept. Technology transfer offices validate "
             "before anything is shared, and access can be revoked at any time.")

st.write("")
n_research = len(store.published_cards("research"))
n_business = len(store.published_cards("business"))
n_live = sum(m["status"] in model.ACCEPTED_STATUSES for m in store.all_matches())
ui.md(f'<div class="tb-muted">{n_research} research cards · {n_business} business profiles · '
      f'{n_live} conversations started on the platform</div>')
st.write("")

c1, c2 = st.columns(2)
if c1.button("I am a researcher", type="primary", use_container_width=True,
             on_click=enter, args=("research",)):
    st.switch_page("views/dashboard.py")
if c2.button("I am business", use_container_width=True, on_click=enter, args=("business",)):
    st.switch_page("views/dashboard.py")
