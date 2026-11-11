from html import escape

import streamlit as st

import matching
import model
import store
import ui

role = ui.role()
persona = store.persona(role)
mine = [c for c in store.my_cards(role) if c["status"] != "draft"]

st.title("Browse business" if role == "research" else "Browse research")
if not mine:
    ui.note("Publish a card first: scores are computed against it.")
    st.stop()


def card_label(card_id):
    c = store.get_card(role, card_id)
    return c["title"] if role == "research" else f"{model.PROFILE_LABELS[c['profile_type']]} · {ui.business_name(c)}"


ids = [c["id"] for c in mine]
current = st.session_state.get("browse_card")
# Unkeyed on purpose: a keyed selectbox keeps showing a stale choice when its options change
st.session_state.browse_card = st.selectbox(
    "Scores computed against your card", ids, index=ids.index(current) if current in ids else 0,
    format_func=card_label)
me = store.get_card(role, st.session_state.browse_card)

# --- Filters ---
with st.container(border=True):
    c1, c2, c3, c4, c5 = st.columns(5)
    sectors = c1.multiselect("Sector", model.SECTORS)
    if role == "research":
        types = c2.multiselect("Profile type", model.PROFILE_TYPES, format_func=model.PROFILE_LABELS.get)
        accepts = c3.checkbox(f"Accepts my maturity ({me['maturity_level']})")
        engagement = c4.multiselect("Engagement type", model.ENGAGEMENT_TYPES)
        country = c5.selectbox("Works with", ["Any country"] + model.COUNTRIES)
    else:
        maturity = c2.slider("Maturity", 1, 5, (1, 5))
        ip = c3.multiselect("IP status", model.IP_STATUS)
        engagement = c4.multiselect("Open to", model.ENGAGEMENT_TYPES)
        country = c5.selectbox("Based in", ["Any country"] + model.COUNTRIES)


def keep(card):
    if sectors and not set(sectors) & set(card["sectors"]):
        return False
    if role == "research":
        lo, hi = card["maturity_accepted"]
        return ((not types or card["profile_type"] in types)
                and (not accepts or lo <= me["maturity_level"] <= hi)
                and (not engagement or set(engagement) & set(card["engagement_type"]))
                and (country == "Any country" or country in card["geography_accepted"]
                     or model.EUROPE_WIDE in card["geography_accepted"]))
    return (maturity[0] <= card["maturity_level"] <= maturity[1]
            and (not ip or card["ip_status"] in ip)
            and (not engagement or set(engagement) & set(card["engagement_wanted"]))
            and (country == "Any country" or card["geography"]["country"] == country)
            and me["id"] not in card["revoked"])


others = [c for c in store.published_cards(ui.other(role)) if keep(c)]
if role == "business":
    others = [c for c in others if c["visibility"] != "private"]
rows, hidden = [], 0
for c in others:
    rc, bc = (me, c) if role == "research" else (c, me)
    s = matching.score_pair(rc, bc)
    if s is None:
        hidden += 1
    else:
        rows.append((s, c, rc, bc))
rows.sort(key=lambda r: -r[0]["mutual"])

ui.md(f'<div class="tb-muted">{len(rows)} profiles, best match first'
      + (f" · {hidden} hidden because the maturity gap is more than two levels" if hidden else "") + "</div>")
st.write("")

for s, c, rc, bc in rows:
    existing = store.find_match(rc["id"], bc["id"])
    with st.container(border=True):
        left, right = st.columns([3, 2], gap="large")
        with left:
            if role == "research":
                ui.md(f'<span class="tb-label">{escape(model.PROFILE_LABELS[c["profile_type"]])}</span>')
                st.markdown(f"**{ui.business_name(c)}** · {c['identity']['country']}")
                ui.md(ui.tags(c["sectors"]))
                st.write(c["looking_for"])
            else:
                revealed = ui.is_revealed(c, me["id"])
                ui.md(f'<span class="tb-label">Research · maturity {ui.maturity_text(c["maturity_level"])}</span>')
                st.markdown(f"**{c['title']}**")
                ui.md(f'<div class="tb-muted">{escape(ui.researcher_name(c, revealed))}'
                      + ("" if revealed else " · Identity revealed after mutual acceptance") + "</div>")
                ui.md(ui.tags(c["sectors"]))
                st.write(c["plain_explanation"])
        with right:
            ui.md(f'{ui.score_badge(s["mutual"])} <span class="tb-muted">mutual · you {s[role]} · '
                  f'them {s[ui.other(role)]}</span>')
            st.markdown("\n".join(f"- {r}" for r in s["reasons"]))
            if s["watch_out"]:
                ui.md(f'<div class="tb-muted">Watch out: {escape(s["watch_out"])}</div>')
            st.write("")
            if existing and existing["status"] != model.DECLINED:
                ui.md(f'<span class="tb-status">Match {escape(existing["status"])}</span>')
                if st.button("Open the match", key=f"open_{c['id']}"):
                    ui.open_match(existing["id"])
            elif st.button("Send a match request", key=f"send_{c['id']}", type="primary"):
                note = (f"Hello, I think my work on \"{me['title']}\" could fit what you are scouting."
                        if role == "research" else
                        f"Hello, {ui.business_name(me)} would like to discuss your work.")
                m = store.create_match(rc["id"], bc["id"], role, persona["name"], note)
                ui.open_match(m["id"])
        with st.expander("Full card"):
            if role == "research":
                ui.business_card(c)
            else:
                ui.research_card(c, revealed=ui.is_revealed(c, me["id"]))
