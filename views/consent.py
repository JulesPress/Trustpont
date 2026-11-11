from html import escape

import streamlit as st

import model
import store
import ui

st.title("Visibility & consent")
ui.md('<div class="tb-muted">You decide who reads your work and when your name is shown. '
      "Nothing leaves this page without your consent and, when required, your TTO's.</div>")
st.write("")

cards = store.my_cards("research")
if not cards:
    st.info("You have no card yet.")
    st.stop()

ids = [c["id"] for c in cards]
current = st.session_state.get("consent_card")
st.session_state.consent_card = st.selectbox(
    "Card", ids, index=ids.index(current) if current in ids else 0,
    format_func=lambda i: store.get_card("research", i)["title"])
card = store.get_card("research", st.session_state.consent_card)

business = store.published_cards("business")
can_see = [] if card["visibility"] == "private" or card["status"] != "published" else \
    [b for b in business if b["id"] not in card["revoked"]]
revealed_to = [b for b in business if (m := store.find_match(card["id"], b["id"]))
               and m["status"] in model.ACCEPTED_STATUSES and b["id"] not in card["revoked"]]

left, right = st.columns(2, gap="large")

with left, st.container(border=True):
    st.subheader("Who can see this card")
    choice = st.radio("Visibility", model.VISIBILITY, index=model.VISIBILITY.index(card["visibility"]),
                      key=f"vis_{card['id']}", horizontal=True,
                      format_func={"public": "Public", "anonymous": "Anonymous until accepted",
                                   "private": "Private"}.get)
    if choice != card["visibility"]:
        card["visibility"] = choice
        st.rerun()
    if card["status"] != "published":
        ui.md(f'<div class="tb-muted">This card is {escape(card["status"])}, so nobody can see it.</div>')
    else:
        ui.md(f"<b>{len(can_see)}</b> business profiles can read this card"
              + (", without your name or institution." if card["visibility"] == "anonymous" else "."))
    st.write("")
    ui.label("Your identity is visible to")
    if card["visibility"] == "public":
        st.write("Everyone who can see the card.")
    elif not revealed_to:
        st.write("Nobody yet. Your name is shown only after you accept a match.")
    for b in revealed_to if card["visibility"] != "public" else []:
        ui.md(f"{escape(ui.business_name(b))} <span class='tb-muted'>· mutual acceptance</span>")

with right, st.container(border=True):
    st.subheader("Technology Transfer Office")
    required = st.checkbox("TTO validation required for this card", value=card["tto_required"],
                           key=f"tto_{card['id']}")
    if required != card["tto_required"]:
        card["tto_required"] = required
        st.rerun()
    ui.md(f'<span class="tb-status">Status</span> &nbsp; <b>{escape(card["tto_status"])}</b>')
    if card["tto_required"] and card["tto_status"] == "not requested":
        if st.button("Request validation", type="primary"):
            card["tto_status"] = "pending"
            st.rerun()
    elif card["tto_status"] == "pending":
        ui.md(f'<div class="tb-muted">Your TTO at {escape(card["owner"]["institution"])} has been asked to review '
              "the card. In this prototype you can simulate their answer.</div>")
        if st.button("Simulate TTO approval"):
            card["tto_status"] = "approved"
            st.rerun()
    elif card["tto_status"] == "approved":
        ui.md('<div class="tb-muted">Approved: the card and its IP statement were checked by your TTO.</div>')

st.write("")
with st.container(border=True):
    st.subheader("Revoke an organisation")
    ui.md('<div class="tb-muted">A revoked organisation no longer sees this card in its search, '
          "even if it is public.</div>")
    candidates = [b for b in business if b["id"] not in card["revoked"]]
    c1, c2 = st.columns([3, 1])
    target = c1.selectbox("Organisation", [b["id"] for b in candidates], label_visibility="collapsed",
                          format_func=lambda i: ui.business_name(store.get_card("business", i)))
    if c2.button("Revoke access", disabled=not candidates):
        card["revoked"].append(target)
        st.rerun()
    if card["revoked"]:
        ui.label("Revoked")
    for bid in list(card["revoked"]):
        b = store.get_card("business", bid)
        c1, c2 = st.columns([3, 1])
        c1.markdown(ui.business_name(b) if b else bid)
        if c2.button("Restore", key=f"restore_{bid}"):
            card["revoked"].remove(bid)
            st.rerun()
