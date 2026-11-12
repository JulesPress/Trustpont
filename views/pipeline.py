from datetime import date
from html import escape

import streamlit as st

import model
import store
import ui

role = ui.role()
matches = store.my_matches(role)
today = store.today()
st.markdown("<style>.block-container { max-width: 80rem !important; }</style>", unsafe_allow_html=True)


def move(match_id, status):
    store.update_match(match_id, status=status)
    if status == "closed":
        store.update_match(match_id, next_action={"text": "", "due": None})


def is_overdue(m):
    return bool(m["next_action"]["due"] and date.fromisoformat(m["next_action"]["due"]) < today and m["status"] not in ("closed", model.DECLINED))


def needs_me(m):
    return m["status"] == "not contacted" and ui.direction(m, role) == "received"


counts = {s: sum(m["status"] == s for m in matches) for s in model.ALL_STATUSES}
open_n = sum(counts[s] for s in model.STATUSES[:-1])
scores = [x["mutual"] for x in (ui.match_score(m) for m in matches) if x]
avg = round(sum(scores) / len(scores)) if scores else None
overdue_n = sum(is_overdue(m) for m in matches)
need_n = sum(needs_me(m) for m in matches)

# ---------- Header: title, key figures, filter pills (reference: Cardiology header) ----------
with st.container(key="tlhead"):
    h1, h2 = st.columns([1, 2.4], vertical_alignment="center", gap="large")
    h1.markdown('<div class="tb-tl-title">Pipeline</div>', unsafe_allow_html=True)
    h2.markdown(
        f'<div class="tb-tl-stats"><div><span>Open</span><b>{open_n}</b></div><div><span>Active</span><b>{counts["active collaboration"]}</b></div>'
        f'<div><span>Need you</span><b>{need_n}</b></div><div><span>Overdue</span><b class="{"bad" if overdue_n else ""}">{overdue_n}</b></div>'
        f'<div><span>Avg match</span><b>{avg if avg is not None else "–"}<small>/100</small></b></div></div>', unsafe_allow_html=True)
    choice = st.segmented_control("Show", ["All", "Needs you", "Overdue", "Declined"], default="All", label_visibility="collapsed", key="pipe_filter") or "All"

shown = [m for m in matches if choice == "All" or (choice == "Needs you" and needs_me(m)) or (choice == "Overdue" and is_overdue(m))
         or (choice == "Declined" and m["status"] == model.DECLINED)]
stages = model.STATUSES if choice != "Declined" else [model.DECLINED]

# ---------- Timeline: a line across, a node per stage, cards hanging below ----------
with st.container(key="tlpanel"):
    cols = st.columns(len(stages), gap="medium")
    for col, status in zip(cols, stages):
        in_col = sorted((m for m in shown if m["status"] == status), key=lambda m: (m["next_action"]["due"] or "9999"))
        with col:
            on = "on" if counts.get(status) else ""
            ui.md(f'<div class="tb-tl-node {on}"><i>{counts.get(status, 0)}</i></div><div class="tb-tl-label">{escape(ui.PIPE_LABELS[status])}</div><div class="tb-tl-stem"></div>')
            if not in_col:
                ui.md('<div class="tb-tl-empty">No matches</div>')
            for m in in_col:
                rc, _ = ui.match_cards(m)
                s = ui.match_score(m)
                with st.container(key=f"tlc_{m['id']}"):
                    nxt = escape(m["next_action"]["text"]) if m["next_action"]["text"] else "No next step"
                    if status == model.DECLINED:
                        nxt = f'Reason: {escape(m["decline_reason"] or "not given")}'
                    ui.md(f'<div class="tb-tc"><div class="tb-tc-top"><b>{escape(ui.counterpart(m, role))}</b>{ui.score_badge(s["mutual"] if s else None)}</div>'
                          f'<div class="tb-tc-sub">{escape(rc["title"])}</div>'
                          f'<div class="tb-tc-next">{nxt}</div><div class="tb-tc-due">{ui.due_html(m["next_action"]["due"]) if status != model.DECLINED else ""}</div></div>')
                    if status == "not contacted":
                        waiting = ui.direction(m, role) == "sent"
                        if st.button("Waiting" if waiting else "Answer", key=f"p_open_{m['id']}", use_container_width=True,
                                     type="secondary" if waiting else "primary"):
                            ui.open_match(m["id"])
                    elif status in model.ACCEPTED_STATUSES:
                        i = model.STATUSES.index(status)
                        b1, b2, b3 = st.columns([1, 1, 1.6])
                        if b1.button("←", key=f"p_back_{m['id']}", help=f"Back to {ui.PIPE_LABELS[model.STATUSES[max(i - 1, 1)]]}", use_container_width=True, disabled=i <= 1):
                            move(m["id"], model.STATUSES[i - 1])
                            st.rerun()
                        if i < len(model.STATUSES) - 1 and b2.button("→", key=f"p_fwd_{m['id']}", help=f"Move to {ui.PIPE_LABELS[model.STATUSES[i + 1]]}", use_container_width=True):
                            move(m["id"], model.STATUSES[i + 1])
                            st.rerun()
                        if b3.button("Open", key=f"p_det_{m['id']}", use_container_width=True):
                            ui.open_match(m["id"])
                    elif st.button("Open", key=f"p_det_{m['id']}", use_container_width=True):
                        ui.open_match(m["id"])

if choice != "Declined" and counts[model.DECLINED] and st.button(f"Show {counts[model.DECLINED]} declined", key="show_declined"):
    st.session_state.pipe_filter = "Declined"
    st.rerun()
