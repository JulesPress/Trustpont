from datetime import date
from html import escape

import streamlit as st

import model
import store
import ui

role = ui.role()
matches = store.my_matches(role)

st.title("Pipeline")
ui.md('<div class="tb-muted">Move a match forward or back once both sides have accepted. '
      "New requests are answered from the match detail.</div>")
st.write("")


def move(match_id, status):
    store.update_match(match_id, status=status)
    if status == "closed":
        store.update_match(match_id, next_action={"text": "", "due": None})


columns = st.columns(len(model.ALL_STATUSES), gap="small")
for col, status in zip(columns, model.ALL_STATUSES):
    in_col = sorted((m for m in matches if m["status"] == status),
                    key=lambda m: m["next_action"]["due"] or "9999")
    with col:
        ui.md(f'<div class="tb-col-head{" active" if in_col else ""}">'
              f'<span class="tb-status">{status}</span> <span class="tb-muted">{len(in_col)}</span></div>')
        for m in in_col:
            rc, _ = ui.match_cards(m)
            s = ui.match_score(m)
            with st.container(border=True):
                overdue = m["next_action"]["due"] and date.fromisoformat(m["next_action"]["due"]) < store.today() \
                    and status not in ("closed", model.DECLINED)
                ui.md(f'{ui.score_badge(s["mutual"] if s else None)} '
                      f'{"<span class=tb-overdue>· overdue</span>" if overdue else ""}<br>'
                      f'<b>{escape(ui.counterpart(m, role))}</b><br>'
                      f'<span class="tb-muted">{escape(rc["title"])}</span>')
                if status == model.DECLINED:
                    ui.md(f'<div class="tb-muted">Reason: {escape(m["decline_reason"] or "not given")}</div>')
                elif m["next_action"]["text"]:
                    ui.md(f'<div style="font-size:0.85rem">{escape(m["next_action"]["text"])}</div>'
                          f'<div style="font-size:0.8rem">{ui.due_html(m["next_action"]["due"])}</div>')
                if status == "not contacted":
                    waiting = ui.direction(m, role) == "sent"
                    if st.button("Waiting" if waiting else "Answer", key=f"p_open_{m['id']}",
                                 use_container_width=True, type="secondary" if waiting else "primary"):
                        ui.open_match(m["id"])
                elif status in model.ACCEPTED_STATUSES:
                    i = model.STATUSES.index(status)
                    b1, b2 = st.columns(2)
                    if i > 1 and b1.button("←", key=f"p_back_{m['id']}", help=f"Back to {model.STATUSES[i - 1]}",
                                           use_container_width=True):
                        move(m["id"], model.STATUSES[i - 1])
                        st.rerun()
                    if i < len(model.STATUSES) - 1 and b2.button("→", key=f"p_fwd_{m['id']}",
                                                                 help=f"Move to {model.STATUSES[i + 1]}",
                                                                 use_container_width=True):
                        move(m["id"], model.STATUSES[i + 1])
                        st.rerun()
                    if st.button("Open", key=f"p_det_{m['id']}", use_container_width=True):
                        ui.open_match(m["id"])
