from datetime import date, timedelta
from html import escape

import streamlit as st

import model
import store
import ui

role = ui.role()
persona = store.persona(role)
matches = store.my_matches(role)
today = store.today()

st.title(f"Welcome back, {persona['name'].split()[0]}")
ui.md(f'<div class="tb-muted">{today.strftime("%A %d %B %Y")}</div>')
st.write("")


def card_title(card):
    if role == "research":
        return card["title"] or "Untitled card"
    return f"{model.PROFILE_LABELS[card['profile_type']]} · {ui.business_name(card)}"


def needs_decision():
    items = []
    for m in matches:
        if m["status"] == "not contacted" and ui.direction(m, role) == "received":
            items.append((m["next_action"]["due"], f"New request from {ui.counterpart(m, role)}", m))
        elif m["status"] in ("contacted", "meeting scheduled", "active collaboration") and m["next_action"]["due"]:
            if date.fromisoformat(m["next_action"]["due"]) <= today + timedelta(days=7):
                items.append((m["next_action"]["due"], m["next_action"]["text"], m))
    return sorted(items, key=lambda x: x[0] or "9999")


left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("Needs your decision")
    items = needs_decision()
    if not items:
        ui.md('<div class="tb-muted">Nothing waiting for you.</div>')
    for due, text, m in items:
        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"**{escape(text)}**  \n" + ui.due_html(due) +
                        f' <span class="tb-muted">· {escape(ui.counterpart(m, role))}</span>',
                        unsafe_allow_html=True)
            if c2.button("Open", key=f"need_{m['id']}"):
                ui.open_match(m["id"])

with right:
    st.subheader("Your cards at the moment" if role == "research" else "Your card at the moment")
    confirm = st.session_state.get("confirm_delete")
    for card in store.my_cards(role):
        with st.container(border=True):
            ui.md(f'<span class="tb-status">{escape(card["status"])}</span>'
                  + (f' <span class="tb-tag">{escape(card["visibility"])}</span>' if role == "research" else ""))
            st.markdown(f"**{card_title(card)}**")
            if role == "research":
                ui.md(f'<div class="tb-muted">Maturity {ui.maturity_text(card["maturity_level"])}</div>')
            else:
                lo, hi = card["maturity_accepted"]
                ui.md(f'<div class="tb-muted">Scouting {", ".join(card["sectors"])} · maturity {lo}-{hi}</div>')
            if confirm == card["id"]:
                ui.md('<div class="tb-overdue">Delete this card and its matches? This cannot be undone.</div>')
                c1, c2, _ = st.columns([1, 1, 2])
                if c1.button("Delete", key=f"del_ok_{card['id']}", type="primary"):
                    store.delete_card(role, card["id"])
                    st.session_state.confirm_delete = None
                    st.rerun()
                if c2.button("Cancel", key=f"del_no_{card['id']}"):
                    st.session_state.confirm_delete = None
                    st.rerun()
            else:
                c1, c2, c3, _ = st.columns([1, 1, 1, 1])
                if c1.button("Edit", key=f"edit_{card['id']}"):
                    st.session_state.edit_card_id = card["id"]
                    st.session_state.wizard = None
                    st.switch_page("views/my_cards.py")
                paused = card["status"] == "paused"
                if c2.button("Resume" if paused else "Pause", key=f"pause_{card['id']}"):
                    card["status"] = "published" if paused else "paused"
                    st.rerun()
                if c3.button("Delete", key=f"del_{card['id']}"):
                    st.session_state.confirm_delete = card["id"]
                    st.rerun()
    if st.button("Add a card", type="primary"):
        st.session_state.edit_card_id = None
        st.session_state.wizard = None
        st.switch_page("views/my_cards.py")

st.write("")
st.subheader("Matches received from business" if role == "research" else "Matches received from researchers")
received = [m for m in matches if ui.direction(m, role) == "received"]
ui.match_table(sorted(received, key=lambda m: m["last_action_at"], reverse=True), role, "received")

st.subheader("Matches sent by you")
sent = [m for m in matches if ui.direction(m, role) == "sent"]
ui.match_table(sorted(sent, key=lambda m: m["last_action_at"], reverse=True), role, "sent")

st.write("")
cols = st.columns(3 if role == "research" else 2, gap="large")

with cols[0], st.container(border=True):
    st.subheader("Pipeline snapshot")
    for status in model.ALL_STATUSES:
        n = sum(m["status"] == status for m in matches)
        c1, c2 = st.columns([4, 1])
        c1.markdown(f'<span class="tb-status">{status}</span>', unsafe_allow_html=True)
        c2.markdown(f"**{n}**")

if role == "research":
    with cols[1], st.container(border=True):
        st.subheader("Time guard")
        cap, used = ui.weekly_cap(), ui.committed_hours()
        share = min(used / cap, 1) if cap else 1
        ui.md(f'<div class="tb-progress"><div style="width:{share * 100:.0f}%"></div></div>')
        st.markdown(f"**{used} of {cap} hours** committed this week")
        ui.md('<div class="tb-muted">Estimated from your live matches: 1 h a week per contact, '
              '2 h with a meeting scheduled, 5 h for an active collaboration. '
              'Set your weekly cap on your card.</div>')
        if ui.time_guard_warning():
            ui.md("<b>Cap reached:</b> accepting a new match will ask for confirmation.")

with cols[-1], st.container(border=True):
    st.subheader("Upcoming")
    upcoming = sorted((m for m in matches if m["next_action"]["due"] and m["status"] not in ("declined", "closed")),
                      key=lambda m: m["next_action"]["due"])[:6]
    if not upcoming:
        ui.md('<div class="tb-muted">No dated actions.</div>')
    for m in upcoming:
        ui.md(f'{ui.due_html(m["next_action"]["due"])}<br>{escape(m["next_action"]["text"])} '
              f'<span class="tb-muted">· {escape(ui.counterpart(m, role))}</span>')
        st.write("")
