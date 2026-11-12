import calendar as _cal
from datetime import date, timedelta
from html import escape

import streamlit as st

import model
import store
import ui

role = ui.role()
persona = store.persona(role)
all_matches = store.my_matches(role)
today = store.today()
first = persona["name"].split()[0]
my_cards = store.my_cards(role)
key_field = "researcher_card_id" if role == "research" else "business_card_id"

# Pastel gradient that follows the user's theme
_bg = ("radial-gradient(38rem 30rem at 8% 6%, rgba(160,190,255,0.80), transparent 62%), radial-gradient(34rem 28rem at 96% 10%, rgba(196,176,255,0.60), transparent 60%), "
       "radial-gradient(40rem 32rem at 80% 96%, rgba(120,160,235,0.70), transparent 62%), radial-gradient(34rem 28rem at 4% 92%, rgba(140,200,235,0.55), transparent 60%), "
       "linear-gradient(135deg, #22346F 0%, #34508F 50%, #5873B8 100%)"
       if st.session_state.get("theme", "warm") == "azure" else
       "radial-gradient(38rem 30rem at 6% 8%, rgba(182,210,152,0.85), transparent 62%), radial-gradient(34rem 28rem at 96% 8%, rgba(220,226,200,0.95), transparent 60%), "
       "radial-gradient(40rem 32rem at 84% 96%, rgba(150,190,150,0.55), transparent 62%), radial-gradient(34rem 28rem at 2% 94%, rgba(200,218,180,0.85), transparent 60%), "
       "linear-gradient(135deg, #F1F4E4 0%, #E4EBD2 50%, #DCE2C8 100%)")
st.markdown(f"<style>.stApp {{ background: {_bg} !important; background-attachment: fixed !important; }}"
            ".block-container { max-width: 78rem !important; }</style>", unsafe_allow_html=True)


def card_title(card):
    if role == "research":
        return card["title"] or "Untitled card"
    return f"{model.PROFILE_LABELS[card['profile_type']]} · {ui.business_name(card)}"


def tile(title, body, foot="", note=""):
    n = f'<span class="tb-bt-n">{note}</span>' if note else ""
    return f'<div class="tb-bt"><div class="tb-bt-h"><span>{title}</span>{n}</div><div class="tb-bt-b">{body}</div><div class="tb-bt-f">{foot}</div></div>'


with st.container(key="dframe"):
    # ---------- Row 1 ----------
    top_l, top_r = st.columns([1, 1.9], gap="small")
    with top_l.container(key="bt_hero"):
        ui.md(f'<div class="tb-bt-h"><span>Welcome back</span><span class="tb-bt-n">{today.strftime("%a %d %b")}</span></div>'
              f'<div class="tb-hello">Hey, {escape(first)}</div><div class="tb-hello-sub">Let\'s find your next match.</div>')
        sel = st.selectbox("Scope", ["All my cards"] + [c["id"] for c in my_cards], label_visibility="collapsed",
                           format_func=lambda i: i if i == "All my cards" else card_title(next(c for c in my_cards if c["id"] == i)))
    matches = [m for m in all_matches if sel == "All my cards" or m[key_field] == sel]

    def needs_decision():
        items = []
        for m in matches:
            if m["status"] == "not contacted" and ui.direction(m, role) == "received":
                items.append((m["next_action"]["due"], f"New request from {ui.counterpart(m, role)}", m))
            elif m["status"] in ("contacted", "meeting scheduled", "active collaboration") and m["next_action"]["due"]:
                if date.fromisoformat(m["next_action"]["due"]) <= today + timedelta(days=7):
                    items.append((m["next_action"]["due"], m["next_action"]["text"], m))
        return sorted(items, key=lambda x: x[0] or "9999")

    items = needs_decision()
    scored = [(m, ui.match_score(m)) for m in matches]
    scored = [(m, s) for m, s in scored if s]
    scores = [s["mutual"] for _, s in scored]
    avg = round(sum(scores) / len(scores)) if scores else None
    live = sum(m["status"] in model.ACCEPTED_STATUSES for m in matches)
    new_req = sum(1 for m in matches if m["status"] == "not contacted" and ui.direction(m, role) == "received")
    overdue = sum(1 for m in matches if m["next_action"]["due"] and m["status"] not in ("closed", model.DECLINED)
                  and date.fromisoformat(m["next_action"]["due"]) < today)
    n_pub = sum(c["status"] == "published" for c in my_cards)
    declined = sum(m["status"] == model.DECLINED for m in matches)

    with top_r.container(key="bt_high"):
        a, b, c = st.columns(3, gap="small")
        if role == "research":
            cap, used = ui.weekly_cap(), ui.committed_hours()
            a.markdown(tile("Time guard", ui.gauge(min(used / cap, 1) if cap else 1, f"{used}h", f"of {cap} h this week"),
                            "Cap reached" if ui.time_guard_warning() else "Within your cap"), unsafe_allow_html=True)
        else:
            a.markdown(tile("Cards live", f'<div class="tb-big">{n_pub}<small>/{len(my_cards)}</small></div>', "published and visible"), unsafe_allow_html=True)
        b.markdown(tile("Match score", f'<div class="tb-big">{avg if avg is not None else "–"}<small>/100</small></div>' + ui.band_gauge(scores, avg),
                        f"{len(scored)} scored matches"), unsafe_allow_html=True)
        c.markdown(tile("Conversations", f'<div class="tb-big">{live}<small>live</small></div>',
                        f"{new_req} new request{'s' if new_req != 1 else ''} waiting"), unsafe_allow_html=True)
        d_, e_, f_ = st.columns(3, gap="small")
        d_.markdown(tile("Needs you", f'<div class="tb-mid">{len(items)}</div>', "decisions this week"), unsafe_allow_html=True)
        e_.markdown(tile("Overdue", f'<div class="tb-mid{" bad" if overdue else ""}">{overdue}</div>', "dated steps in the past"), unsafe_allow_html=True)
        f_.markdown(tile("Declined", f'<div class="tb-mid">{declined}</div>', "closed without a deal"), unsafe_allow_html=True)

    # ---------- Row 2 ----------
    bot_l, bot_r = st.columns([1.35, 1], gap="small")
    with bot_l.container(key="bt_list"):
        ui.md('<div class="tb-bt-h"><span>Your work</span></div>')
        t_dec, t_match, t_cards = st.tabs([f"Decisions {len(items)}", f"Matches {len(matches)}", f"Cards {len(my_cards)}"])

        def row(m, title, sub, score=None, key=""):
            with st.container(key=f"drow_{key}_{m['id']}"):
                c1, c2, c3 = st.columns([3.2, 1.1, 1], vertical_alignment="center", gap="small")
                c1.markdown(f'<div class="tb-r-t">{escape(title)}</div><div class="tb-r-s">{sub}</div>', unsafe_allow_html=True)
                c2.markdown(ui.score_badge(score) if score is not None else "", unsafe_allow_html=True)
                if c3.button("Open", key=f"{key}_{m['id']}", use_container_width=True):
                    ui.open_match(m["id"])

        with t_dec:
            if not items:
                ui.md('<div class="tb-muted" style="padding:0.8rem 0">Nothing is waiting for you.</div>')
            for due, text, m in items[:8]:
                s = ui.match_score(m)
                row(m, text, f'{ui.due_html(due)} <span class="tb-muted">· {escape(ui.counterpart(m, role))}</span>', s["mutual"] if s else None, "dec")
        with t_match:
            if not scored:
                ui.md('<div class="tb-muted" style="padding:0.8rem 0">No matches yet.</div>')
            for m, s in sorted(scored, key=lambda x: -x[1]["mutual"]):
                row(m, ui.counterpart(m, role), f'{escape(ui.PIPE_LABELS.get(m["status"], m["status"]))} · {ui.due_html(m["next_action"]["due"])}', s["mutual"], "mat")
        with t_cards:
            confirm = st.session_state.get("confirm_delete")
            for card in my_cards:
                with st.container(key=f"drow_card_{card['id']}"):
                    c1, c2 = st.columns([2.2, 2], vertical_alignment="center", gap="small")
                    sub = f"Maturity {ui.maturity_text(card['maturity_level'])}" if role == "research" else f"Scouting {', '.join(card['sectors'])}"
                    c1.markdown(f'<div class="tb-r-t">{escape(card_title(card))}</div><div class="tb-r-s">{escape(card["status"])} · {escape(sub)}</div>', unsafe_allow_html=True)
                    if confirm == card["id"]:
                        b1, b2 = c2.columns(2)
                        if b1.button("Delete", key=f"del_ok_{card['id']}", type="primary", use_container_width=True):
                            store.delete_card(role, card["id"])
                            st.session_state.confirm_delete = None
                            st.rerun()
                        if b2.button("Cancel", key=f"del_no_{card['id']}", use_container_width=True):
                            st.session_state.confirm_delete = None
                            st.rerun()
                    else:
                        b1, b2, b3 = c2.columns(3)
                        if b1.button("Edit", key=f"edit_{card['id']}", use_container_width=True):
                            st.session_state.edit_card_id = card["id"]
                            st.session_state.wizard = None
                            st.switch_page("views/my_cards.py")
                        paused = card["status"] == "paused"
                        if b2.button("Resume" if paused else "Pause", key=f"pause_{card['id']}", use_container_width=True):
                            card["status"] = "published" if paused else "paused"
                            st.rerun()
                        if b3.button("Delete", key=f"del_{card['id']}", use_container_width=True):
                            st.session_state.confirm_delete = card["id"]
                            st.rerun()
            if st.button("Add a card", type="primary"):
                st.session_state.edit_card_id = None
                st.session_state.wizard = None
                st.switch_page("views/my_cards.py")

    with bot_r:
        rows_ = [(ui.counterpart(m, role), s["mutual"], s["research"], s["business"]) for m, s in sorted(scored, key=lambda x: x[0]["last_action_at"])]
        chart = ui.score_chart(rows_) if len(rows_) >= 2 else '<div class="tb-muted">Scores appear once you have two matches.</div>'
        st.markdown(tile("Match scores", chart, "", "by last activity"), unsafe_allow_html=True)
        due_days = {date.fromisoformat(m["next_action"]["due"]).day for m in matches
                    if m["next_action"]["due"] and m["status"] not in ("declined", "closed")
                    and date.fromisoformat(m["next_action"]["due"]).month == today.month and date.fromisoformat(m["next_action"]["due"]).year == today.year}
        cells = "".join('<i class="e"></i>' for _ in range(date(today.year, today.month, 1).weekday()))
        for dd in range(1, _cal.monthrange(today.year, today.month)[1] + 1):
            cells += f'<i class="{"tod" if dd == today.day else "due" if dd in due_days else ""}">{dd}</i>'
        cal = (f'<div class="tb-cal-w"><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span><span>S</span></div><div class="tb-cal-g">{cells}</div>')
        st.markdown(tile("Active days", cal, '<span class="tb-cal-lg"><i class="due"></i>next step<i class="tod"></i>today</span>', today.strftime("%B")), unsafe_allow_html=True)
