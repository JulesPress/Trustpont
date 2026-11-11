from datetime import timedelta
from html import escape

import streamlit as st

import model
import store
import ui

role = ui.role()
persona = store.persona(role)
matches = sorted(store.my_matches(role), key=lambda m: m["last_action_at"], reverse=True)

st.title("Match detail")
if not matches:
    st.info("No matches yet. Browse the other side to send a first request.")
    st.stop()

ids = [m["id"] for m in matches]
current = st.session_state.get("selected_match")


def describe(match_id):
    m = store.get_match(match_id)
    rc, _ = ui.match_cards(m)
    return f"{ui.counterpart(m, role)} · {rc['title']} · {m['status']}"


# Unkeyed on purpose: a keyed selectbox keeps showing a stale choice when its options change
st.session_state.selected_match = st.selectbox(
    "Match", ids, index=ids.index(current) if current in ids else 0,
    format_func=describe, label_visibility="collapsed")
m = store.get_match(st.session_state.selected_match)
rc, bc = ui.match_cards(m)
score = ui.match_score(m)
revealed = role == "research" or ui.is_revealed(rc, bc["id"])
received = ui.direction(m, role) == "received"

ui.md(f'<span class="tb-status">{escape(m["status"])}</span> &nbsp; '
      f'<span class="tb-muted">{"Received" if received else "Sent"} on {m["created_at"]} · '
      f'last action {m["last_action_at"]}</span>')
if m["status"] == model.DECLINED and m["decline_reason"]:
    ui.md(f'<div class="tb-muted">Declined, reason recorded: <b>{escape(m["decline_reason"])}</b></div>')

# --- Scores and explanation ---
if score is None:
    st.warning("These two cards are now more than two maturity levels apart, so they no longer count as a match.")
else:
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="tb-label">Mutual score</div><div style="font-size:2.4rem" class="tb-serif">{score["mutual"]}</div>',
                    unsafe_allow_html=True)
        c2.markdown(f'<div class="tb-label">With the researcher\'s weights</div>'
                    f'<div style="font-size:1.6rem" class="tb-serif">{score["research"]}</div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="tb-label">With the business weights</div>'
                    f'<div style="font-size:1.6rem" class="tb-serif">{score["business"]}</div>', unsafe_allow_html=True)
        gap = abs(score["research"] - score["business"])
        if gap >= 15:
            keen = "the researcher" if score["research"] > score["business"] else "the business side"
            ui.md(f'<div class="tb-muted">Asymmetric match: it fits {keen} much better than the other side '
                  f"({gap} points apart). Worth discussing openly.</div>")
        c1, c2 = st.columns([3, 2], gap="large")
        with c1:
            ui.label("Why it matches")
            st.markdown("\n".join(f"- {r}" for r in score["reasons"]) or "—")
            if score["watch_out"]:
                ui.label("Watch out")
                st.markdown(score["watch_out"])
        with c2:
            ui.label("Maturity")
            lo, hi = bc["maturity_accepted"]
            ui.md(ui.maturity_scale(rc["maturity_level"], (lo, hi)) +
                  f'<div class="tb-muted">Research at {ui.maturity_text(rc["maturity_level"])}. '
                  f"Business accepts {lo} to {hi}.</div>")
        with st.expander("How the score is computed"):
            rw, bw = rc["criteria_weights"], bc["criteria_weights"]
            st.dataframe([{
                "Criterion": model.CRITERIA_LABELS[c], "Sub-score": score["subs"][c][0],
                "Researcher weight": rw[c], "Business weight": bw[c], "Detail": score["subs"][c][1],
            } for c in model.CRITERIA], hide_index=True, use_container_width=True)
            st.caption("Sub-scores: 1 clear match, 0.5 partial, 0 none. Weights: Must have 5, Important 3, "
                       "Nice to have 1. Each side's score is the weighted average out of 100; the mutual score "
                       "is the average of the two.")

# --- Actions ---
st.subheader("Actions")
open_statuses = model.STATUSES[:-1]
if m["status"] not in open_statuses:
    ui.md('<div class="tb-muted">This match is closed. No further action.</div>')
else:
    acts = st.columns(3, gap="medium")
    with acts[0], st.container(border=True):
        if m["status"] == "not contacted" and received:
            ui.label("Accept")
            warning = ui.time_guard_warning() if role == "research" else None
            ok = True
            if warning:
                ui.md(f"<b>{escape(warning)}</b>")
                ok = st.checkbox("Accept anyway", key=f"anyway_{m['id']}")
            if st.button("Accept the match", type="primary", disabled=not ok, key=f"accept_{m['id']}"):
                store.update_match(m["id"], status="contacted", next_action={
                    "text": "Plan a first call",
                    "due": (store.today() + timedelta(days=7)).isoformat()})
                store.add_log(m["id"], persona["name"], "Accepted the match. Identities are now visible to both sides.")
                st.rerun()
        elif m["status"] == "not contacted":
            ui.label("Waiting")
            st.write(f"Your request was sent on {m['created_at']}. The other side has not answered yet.")
        else:
            ui.label("Schedule a meeting")
            with st.form(f"meet_{m['id']}", border=False):
                when = st.date_input("Date", value=store.today() + timedelta(days=3), min_value=store.today())
                what = st.text_input("Topic", value="First call")
                if st.form_submit_button("Schedule"):
                    store.update_match(m["id"], status="meeting scheduled",
                                       next_action={"text": f"Meeting: {what}",
                                                    "due": when.isoformat()})
                    store.add_log(m["id"], persona["name"], f"Scheduled a meeting on {when.isoformat()}: {what}")
                    st.rerun()

    with acts[1], st.container(border=True):
        ui.label("Message")
        with st.form(f"msg_{m['id']}", border=False, clear_on_submit=True):
            text = st.text_area("Message", height=96, label_visibility="collapsed",
                                placeholder="Write a short message")
            if st.form_submit_button("Send") and text.strip():
                store.add_log(m["id"], persona["name"], text.strip())
                st.rerun()
        ui.md('<div class="tb-muted">Prototype: messages are kept on the match for this session, nothing is emailed.</div>')

    with acts[2], st.container(border=True):
        verb = "Withdraw" if not received and m["status"] == "not contacted" else "Decline"
        ui.label(verb)
        reasons = (["wrong sector", "no time", "too early for me", "other"] if role == "research"
                   else ["wrong sector", "no budget", "too early for us", "other"])
        with st.form(f"decline_{m['id']}", border=False):
            reason = st.radio("Reason", reasons, label_visibility="collapsed")
            detail = st.text_input("Detail (optional)")
            if st.form_submit_button(verb):
                recorded = reason if not detail.strip() else f"{reason}: {detail.strip()}"
                store.update_match(m["id"], status=model.DECLINED, decline_reason=recorded,
                                   next_action={"text": "", "due": None})
                store.add_log(m["id"], persona["name"], f"Declined ({recorded}).")
                st.rerun()

if m["status"] in open_statuses and m["next_action"]["text"]:
    ui.md(f'<div class="tb-muted">Next action: {escape(m["next_action"]["text"])} · '
          f'{ui.due_html(m["next_action"]["due"])}</div>')

# --- Cards side by side ---
st.subheader("The two cards")
left, right = st.columns(2, gap="large")
with left:
    ui.research_card(rc, revealed=revealed)
with right:
    ui.business_card(bc)

st.subheader("Conversation")
if not m["log"]:
    ui.md('<div class="tb-muted">No messages yet.</div>')
for entry in reversed(m["log"]):
    who = entry["who"]
    if who == rc["owner"]["name"] and not revealed:
        who = "Anonymous researcher"
    ui.md(f'<div class="tb-muted">{entry["at"]} · {escape(who)}</div>')
    st.write(entry["text"])
