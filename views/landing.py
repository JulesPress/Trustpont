import streamlit as st

import model
import partners
import store
import ui


def enter(role):
    st.session_state.role = role


n_research = len(store.published_cards("research"))
n_business = len(store.published_cards("business"))
n_live = sum(m["status"] in model.ACCEPTED_STATUSES for m in store.all_matches())

# Full-bleed picture: a bridge between two cliffs. The words float on it.
ui.md(f"""<div class="tb-home"><div class="tb-home-bg"></div><div class="tb-home-tint"></div><div class="tb-home-fade"></div>
<div class="tb-home-copy"><h1>Bridge the gap <em>between</em><br><em class="b">research and business</em></h1>
<p>Turn lab results into plain-language cards, and match them with the companies looking for them.</p></div>
<div class="tb-home-left"><div class="tb-tagline"><span class="tb-dots"></span>Trustpont Match</div>
<p>Researchers publish a card anyone can read. Companies, investors and incubators say what they scout for. Six criteria give both sides one score.</p>
<p style="margin-top:0.7rem;opacity:.75;font-size:0.8rem">{n_research} research cards · {n_business} business profiles · {n_live} conversations</p></div>
<div class="tb-home-right"><a class="tb-peek" href="#how-it-works"><b><i>&#8595;</i>How it works?</b><span>3 steps · 1 min read</span></a></div></div>""")

# The two doors, sitting on the bottom-left of the picture
with st.container(key="herobtns"):
    c1, c2, _ = st.columns([1.35, 1.2, 3.4])
    if c1.button("I am a researcher", use_container_width=True, on_click=enter, args=("research",)):
        st.switch_page("views/dashboard.py")
    if c2.button("I am business", use_container_width=True, on_click=enter, args=("business",)):
        st.switch_page("views/dashboard.py")

ui.cycle_section()

partners.render()

ui.md("""<div id="how-it-works"></div><div class="tb-section-title">How it works</div>
<div class="tb-steps">
<div class="tb-step"><i>1</i><b>Write a card</b><span>Researchers explain their work in plain language first, then the business facts.</span></div>
<div class="tb-step"><i>2</i><b>Get matched</b><span>Companies and investors say what they scout for. Six criteria give a score both sides can read.</span></div>
<div class="tb-step"><i>3</i><b>Stay in control</b><span>Stay anonymous until both sides accept. Revoke access at any time.</span></div>
</div>""")

st.write("")
featured = [ui.stage_item_research(c) for c in store.published_cards("research")[:3]] + \
           [ui.stage_item_business(c) for c in store.published_cards("business")[:3]]
ui.card_stage(featured, "home", "A look inside")
