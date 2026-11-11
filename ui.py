# Rendering helpers shared by both sides of the app.
from datetime import date
from html import escape

import pandas as pd
import streamlit as st

import matching
import model
import store

MATCH_PAGE = "views/match_detail.py"


def role():
    return st.session_state.get("role", "research")


def other(r):
    return "business" if r == "research" else "research"


def md(html):
    st.markdown(html, unsafe_allow_html=True)


def score_badge(score):
    if score is None:
        return '<span class="tb-score low">n/a</span>'
    level = "high" if score > 75 else "mid" if score >= 50 else "low"
    return f'<span class="tb-score {level}">{score}</span>'


def tags(items):
    return "".join(f'<span class="tb-tag">{escape(str(i))}</span>' for i in items)


def label(text):
    md(f'<div class="tb-label">{escape(text)}</div>')


def euros(n):
    return f"EUR {n:,.0f}".replace(",", " ")


def maturity_text(level):
    return f"{level} · {model.MATURITY[level]}"


def maturity_scale(level=None, accepted=None):
    cells = []
    for i in range(1, 6):
        cls = "at" if i == level else "in" if accepted and accepted[0] <= i <= accepted[1] else ""
        cells.append(f'<div class="{cls}" title="{i}. {model.MATURITY[i]}"></div>')
    return '<div class="tb-scale">' + "".join(cells) + "</div>"


def due_html(due):
    if not due:
        return '<span class="tb-muted">no date</span>'
    d = date.fromisoformat(due)
    days = (d - store.today()).days
    when = d.strftime("%a %d %b")
    if days < 0:
        return f'<span class="tb-overdue">{when} · overdue by {-days} day{"s" if days < -1 else ""}</span>'
    if days == 0:
        return f"<span>{when} · today</span>"
    return f'<span class="tb-muted">{when} · in {days} day{"s" if days > 1 else ""}</span>'


# --- Identity and anonymity ---

def is_revealed(rc, business_card_id=None):
    if rc["visibility"] != "anonymous":
        return True
    m = store.find_match(rc["id"], business_card_id) if business_card_id else None
    return bool(m and m["status"] in model.ACCEPTED_STATUSES)


def researcher_name(rc, revealed=True):
    if not revealed:
        return f"Anonymous researcher · {rc['owner']['field']}"
    o = rc["owner"]
    return f"{o['name']} · {o['institution']}"


def business_name(bc):
    # People-centred profiles are known by their name, organisations by the organisation
    i = bc["identity"]
    if bc["profile_type"] in ("business developer", "ex-founder") or not i["organisation"]:
        return i["name"]
    return i["organisation"]


# --- Cards ---

def research_card(rc, revealed=True, show_part2=True, score=None):
    with st.container(border=True):
        top = f'<span class="tb-label">Research card · {escape(rc["status"])}</span>'
        if score is not None:
            top += f' &nbsp; {score_badge(score)}'
        md(top)
        st.markdown(f"### {rc['title'] or 'Untitled card'}")
        if revealed:
            md(f'<div class="tb-muted">{escape(researcher_name(rc))} · {escape(rc["owner"]["country"])}</div>')
        else:
            md(f'<div class="tb-muted">{escape(researcher_name(rc, False))} · {escape(rc["geography"]["country"])}<br>'
               "Identity revealed after mutual acceptance</div>")
        md(tags(rc["sectors"]))
        md(f'<div class="tb-muted">Maturity {escape(maturity_text(rc["maturity_level"]))}</div>'
           + maturity_scale(rc["maturity_level"]))

        label("The problem")
        st.write(rc["key_problem"] or "—")
        label("In plain words")
        st.write(rc["plain_explanation"] or "—")
        if rc["concrete_examples"]:
            label("What it could do")
            st.markdown("\n".join(f"- {e}" for e in rc["concrete_examples"] if e))
        label("Where something similar worked")
        st.write(rc["case_studies"] or "—")
        label("Honest feasibility")
        st.write(rc["feasibility"] or "—")

        if show_part2:
            st.divider()
            label("Business side")
            st.write(rc["market_problem"] or "—")
            c1, c2 = st.columns(2)
            c1.markdown(f"**Draft business plan**  \n{rc['draft_business_plan'] or '—'}")
            c2.markdown(f"**Go to market**  \n{rc['go_to_market'] or '—'}")
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"**R&D to date**  \n{euros(rc['rd_costs_to_date'])}")
            c2.markdown(f"**Capital needed**  \n{euros(rc['capital_needed'])}")
            c3.markdown(f"**IP**  \n{rc['ip_status']}")
            c4.markdown(f"**Equity on the table**  \n{rc['equity_expected']}")
            g = rc["geography"]
            extras = [x for x, ok in (("remote ok", g["remote"]), ("can relocate", g["relocate"])) if ok]
            md(f'<div class="tb-muted">Needs</div>{tags(rc["support_needed"]) or "—"}'
               f'<div class="tb-muted">Open to</div>{tags(rc["engagement_wanted"]) or "—"}'
               f'<div class="tb-muted">Based in {escape(g["country"])}{" · " + ", ".join(extras) if extras else ""}</div>')


def business_card(bc, score=None):
    with st.container(border=True):
        top = f'<span class="tb-label">{escape(model.PROFILE_LABELS[bc["profile_type"]])}</span>'
        if score is not None:
            top += f' &nbsp; {score_badge(score)}'
        md(top)
        st.markdown(f"### {business_name(bc)}")
        i = bc["identity"]
        md(f'<div class="tb-muted">{escape(i["name"])} · {escape(i["role"])} · {escape(i["country"])}</div>')
        md(tags(bc["sectors"]))
        lo, hi = bc["maturity_accepted"]
        md(f'<div class="tb-muted">Accepts maturity {lo} to {hi}</div>' + maturity_scale(None, (lo, hi)))
        label("Looking for")
        st.write(bc["looking_for"] or "—")
        c1, c2 = st.columns(2)
        with c1:
            md(f'<div class="tb-muted">Engagement</div>{tags(bc["engagement_type"]) or "—"}')
        with c2:
            md(f'<div class="tb-muted">Brings</div>{tags(bc["what_they_bring"]) or "—"}')
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"**IP**  \n{bc['ip_expectation']}")
        c2.markdown(f"**Equity**  \n{bc['equity_expected']}")
        c3.markdown(f"**Time**  \n{bc['time_commitment']} h / month")
        t = bc["timeline"]
        md(f'<div class="tb-muted">Geography: {escape(", ".join(bc["geography_accepted"]))}<br>'
           f'Start: {escape(t["start"] or "—")} · Signs: {escape(t["signatory"] or "—")} · Budget: {escape(t["budget"] or "—")}</div>')
        fields = model.PROFILE_FIELDS[bc["profile_type"]]
        details = []
        for key, (name, kind, _) in fields.items():
            value = bc["extra"].get(key)
            if value is None or value == "":
                continue
            if kind == "bool":
                value = "yes" if value else "no"
            elif kind == "int" and key.endswith("_eur"):
                value = euros(value)
            details.append(f"{name}: {value}")
        if details:
            md(f'<div class="tb-muted">{escape(" · ".join(details))}</div>')


# --- Matches ---

def match_cards(m):
    return store.get_card("research", m["researcher_card_id"]), store.get_card("business", m["business_card_id"])


def match_score(m):
    rc, bc = match_cards(m)
    return matching.score_pair(rc, bc) if rc and bc else None


def direction(m, viewer):
    return "sent" if m["initiated_by"] == viewer else "received"


def counterpart(m, viewer):
    rc, bc = match_cards(m)
    if viewer == "research":
        return business_name(bc)
    return rc["owner"]["name"] if is_revealed(rc, bc["id"]) else "Anonymous researcher"


def open_match(match_id):
    st.session_state.selected_match = match_id
    st.switch_page(MATCH_PAGE)


def match_table(matches, viewer, key):
    if not matches:
        md('<div class="tb-muted">Nothing here yet.</div>')
        return
    rows = []
    for m in matches:
        rc, bc = match_cards(m)
        s = match_score(m)
        theirs = bc if viewer == "research" else rc
        rows.append({
            "Counterpart": counterpart(m, viewer),
            "Score": s["mutual"] if s else None,
            "Status": m["status"],
            "Sector": ", ".join(theirs["sectors"]),
            "Equity": theirs["equity_expected"],
            "Geography": ", ".join(bc["geography_accepted"]) if viewer == "research" else rc["geography"]["country"],
            ("Your card" if viewer == "research" else "Research"): rc["title"],
        })
    # A fresh key after each click so the selection does not re-trigger on return
    nonce = st.session_state.setdefault("table_nonce", 0)
    event = st.dataframe(
        pd.DataFrame(rows), hide_index=True, use_container_width=True,
        on_select="rerun", selection_mode="single-row", key=f"{key}_{nonce}",
        column_config={"Score": st.column_config.NumberColumn(format="%d", width="small")},
    )
    if event.selection.rows:
        st.session_state.table_nonce += 1
        open_match(matches[event.selection.rows[0]]["id"])
    md('<div class="tb-muted">Click a row to open the match.</div>')


# --- Time guard (researcher side) ---

def weekly_cap():
    cards = store.my_cards("research")
    return max((c["hours_per_week_available"] for c in cards), default=0)


def committed_hours():
    return sum(model.STATUS_HOURS.get(m["status"], 0) for m in store.my_matches("research"))


def time_guard_warning():
    """Text of the warning if accepting one more match would exceed the cap, else None."""
    cap, used = weekly_cap(), committed_hours()
    if used + model.STATUS_HOURS["contacted"] > cap:
        return (f"Your time guard is reached: {used} of {cap} hours a week are already committed. "
                "Accepting adds about 1 hour a week.")
    return None
