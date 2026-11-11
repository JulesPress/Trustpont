import copy
from html import escape

import streamlit as st

import ai
import model
import store
import ui

role = ui.role()
persona = store.persona(role)
STEPS = {
    "research": ["Abstract", "Generation", "Review", "Weights & publish"],
    "business": ["Profile type", "Your card", "Weights & publish"],
}


def new_card():
    if role == "business":
        return model.new_business_card(persona["identity"])
    card = model.new_researcher_card(persona["owner"])
    card["hours_per_week_available"] = ui.weekly_cap() or card["hours_per_week_available"]
    return card


def start(card, step):
    for k in [k for k in st.session_state if k.startswith("wz_")]:
        del st.session_state[k]
    st.session_state.wizard = {"card": card, "step": step, "notice": ""}


# Coming from the dashboard "Edit" or "Add a card" buttons
if "edit_card_id" in st.session_state:
    card_id = st.session_state.pop("edit_card_id")
    if card_id:
        start(copy.deepcopy(store.get_card(role, card_id)), 3 if role == "research" else 2)
    else:
        start(new_card(), 1)

wizard = st.session_state.get("wizard")
if wizard and wizard["card"].get("owner" if role == "research" else "identity") is None:
    wizard = None  # wizard left over from the other role

# --- Card list when no wizard is open ---
if not wizard:
    st.title("My cards" if role == "research" else "My card")
    flash = st.session_state.pop("flash", None)
    if flash:
        st.success(flash)
    cards = store.my_cards(role)
    if st.button("Create a new card", type="primary"):
        start(new_card(), 1)
        st.rerun()
    if not cards:
        st.info("You have no card yet.")
    cols = st.columns(2, gap="large")
    for i, card in enumerate(cards):
        with cols[i % 2]:
            if role == "research":
                ui.research_card(card, compact=True)
            else:
                ui.business_card(card)
            if st.button("Edit this card", key=f"edit_{card['id']}"):
                start(copy.deepcopy(card), 3 if role == "research" else 2)
                st.rerun()
    st.stop()

card = wizard["card"]
step = wizard["step"]
editing = bool(card.get("id"))


def go(n):
    wizard["step"] = n
    st.rerun()


def bind(widget, field, label, **kw):
    """Keyed widget whose value lives in the card, so it survives step changes."""
    key = f"wz_{field}"
    if key not in st.session_state:
        st.session_state[key] = card[field]
    card[field] = widget(label, key=key, **kw)


st.title(("Edit card" if editing else "New card"))
ui.md('<div class="tb-muted">' + " &nbsp;·&nbsp; ".join(
    f'<b style="color:var(--teal)">{i + 1}. {s}</b>' if i + 1 == step else f"{i + 1}. {s}"
    for i, s in enumerate(STEPS[role])) + "</div>")
st.write("")


def weights_and_visibility():
    st.subheader("How much each criterion matters to you")
    ui.md('<div class="tb-muted">Your weights shape your side of the score. '
          "The other side weighs the same six criteria with their own priorities.</div>")
    for c in model.CRITERIA:
        key = f"wz_w_{c}"
        if key not in st.session_state:
            st.session_state[key] = card["criteria_weights"][c]
        value = st.segmented_control(model.CRITERIA_LABELS[c], list(model.WEIGHT_LEVELS), key=key)
        card["criteria_weights"][c] = value or "Important"


# ===================== Researcher wizard =====================
if role == "research":
    if step == 1:
        st.subheader("Start from your abstract")
        ui.md('<div class="tb-muted">Paste an abstract or a short summary of your work. Claude drafts the '
              "card in plain language; you review every field before anything is published.</div>")
        st.session_state.setdefault("wz_abstract", ai.DEMO_ABSTRACT)
        st.session_state.setdefault("wz_sectors", ["Advanced materials", "Environment & water"])
        st.session_state.setdefault("wz_maturity", 2)
        text = st.text_area("Abstract or summary", key="wz_abstract", height=200)
        sectors = st.multiselect("Sectors (1 to 3)", model.SECTORS, key="wz_sectors", max_selections=3)
        maturity = st.select_slider("Maturity level", options=list(model.MATURITY), key="wz_maturity",
                                    format_func=ui.maturity_text)
        c1, c2 = st.columns([1, 4])
        if c1.button("Generate the card", type="primary", disabled=not (text.strip() and sectors)):
            with st.spinner("Claude is turning your abstract into a card..."):
                result = ai.generate_card_from_abstract(text, sectors, maturity)
            wizard["notice"] = result.pop("_notice")
            result.pop("_mode")
            card.update(result)
            for k in [k for k in st.session_state if k.startswith("wz_") and k[3:] in result]:
                del st.session_state[k]
            go(3)
        if c2.button("Cancel"):
            st.session_state.wizard = None
            st.rerun()

    elif step == 3:
        form, preview = st.columns([1, 1], gap="large")
        with form:
            if wizard["notice"]:
                ui.md(f'<div class="tb-notice">{escape(wizard["notice"])}</div>')
            part1, part2 = st.tabs(["Part 1 · plain language", "Part 2 · business"])
            with part1:
                bind(st.text_input, "title", "Title (short, no jargon)")
                bind(st.text_area, "key_problem", "The problem in your field", height=90)
                bind(st.text_area, "plain_explanation", "Plain explanation (3 to 5 sentences)", height=150)
                key = "wz_examples"
                if key not in st.session_state:
                    st.session_state[key] = "\n".join(card["concrete_examples"])
                examples = st.text_area("Concrete examples (one per line, 2 or 3)", key=key, height=100)
                card["concrete_examples"] = [e.strip() for e in examples.splitlines() if e.strip()][:3]
                bind(st.text_area, "case_studies", "Where something similar already worked", height=90)
                bind(st.text_area, "feasibility", "Honest feasibility", height=110)
            with part2:
                bind(st.text_area, "market_problem", "The problem within a market", height=90)
                bind(st.text_area, "draft_business_plan", "Draft business plan", height=90)
                bind(st.text_area, "go_to_market", "Go to market", height=90)
                c1, c2 = st.columns(2)
                with c1:
                    bind(st.number_input, "rd_costs_to_date", "R&D costs to date (EUR)", min_value=0, step=10000)
                with c2:
                    bind(st.number_input, "capital_needed", "Capital needed (EUR)", min_value=0, step=10000)
                bind(st.select_slider, "maturity_level", "Maturity level", options=list(model.MATURITY),
                     format_func=ui.maturity_text)
                bind(st.multiselect, "sectors", "Sectors (1 to 3)", options=model.SECTORS, max_selections=3)
                bind(st.multiselect, "support_needed", "Support needed", options=model.SUPPORT_NEEDED)
                bind(st.multiselect, "engagement_wanted", "Open to", options=model.ENGAGEMENT_TYPES)
                c1, c2 = st.columns(2)
                with c1:
                    bind(st.selectbox, "ip_status", "IP status", options=model.IP_STATUS)
                with c2:
                    bind(st.selectbox, "equity_expected", "Equity on the table", options=model.EQUITY_RESEARCH)
                geo = card["geography"]
                st.session_state.setdefault("wz_country", geo["country"])
                st.session_state.setdefault("wz_remote", geo["remote"])
                st.session_state.setdefault("wz_relocate", geo["relocate"])
                c1, c2, c3 = st.columns([2, 1, 1])
                geo["country"] = c1.selectbox("Country", model.COUNTRIES, key="wz_country")
                geo["remote"] = c2.checkbox("Remote ok", key="wz_remote")
                geo["relocate"] = c3.checkbox("Can relocate", key="wz_relocate")
            st.write("")
            c1, c2 = st.columns(2)
            if not editing and c1.button("Back to the abstract"):
                go(1)
            if c2.button("Continue", type="primary", disabled=not (card["title"].strip() and card["sectors"])):
                go(4)
        with preview:
            ui.label("Live preview · what business people will see")
            ui.research_card(card)

    elif step == 4:
        form, preview = st.columns([1, 1], gap="large")
        with form:
            weights_and_visibility()
            st.subheader("Visibility and time")
            bind(st.radio, "visibility", "Who can see this card", options=model.VISIBILITY, horizontal=True,
                 format_func={"public": "Public", "anonymous": "Anonymous until accepted",
                              "private": "Private (only me)"}.get)
            bind(st.checkbox, "tto_required", "My Technology Transfer Office must validate before publication")
            if card["tto_required"]:
                ui.md(f'<div class="tb-muted">TTO status: {escape(card["tto_status"])}. Publishing sends a '
                      "validation request if none was made.</div>")
            bind(st.number_input, "hours_per_week_available", "Hours a week I can give to matches",
                 min_value=1, max_value=40, step=1)
            st.write("")
            c1, c2, c3 = st.columns(3)
            if c1.button("Back"):
                go(3)

            def save(status):
                card["status"] = status
                if card["tto_required"] and card["tto_status"] == "not requested":
                    card["tto_status"] = "pending"
                store.save_card("research", card)
                st.session_state.wizard = None
                st.session_state.browse_card = card["id"]
                st.session_state.flash = ("Card published. Business profiles can now find it."
                                          if status == "published" else "Draft saved.")
                st.rerun()

            if c2.button("Save as draft"):
                save("draft")
            if c3.button("Publish", type="primary"):
                save("published")
        with preview:
            ui.label("Live preview")
            ui.research_card(card)

# ===================== Business wizard =====================
else:
    if step == 1:
        st.subheader("What kind of profile are you?")
        blurbs = {
            "industry": "A company scouting technologies for pilots, research contracts or licences.",
            "business developer": "You take research to market and look for a technology to carry.",
            "ex-founder": "You built a company before and look for the next one to co-found or advise.",
            "VC": "You invest in early-stage spin-offs.",
            "incubator": "You run a programme that helps researchers start a company.",
        }
        st.session_state.setdefault("wz_profile_type", card["profile_type"])
        choice = st.radio("Profile type", model.PROFILE_TYPES, key="wz_profile_type",
                          format_func=lambda t: f"{model.PROFILE_LABELS[t]} · {blurbs[t]}",
                          label_visibility="collapsed")
        c1, c2 = st.columns([1, 4])
        if c1.button("Continue", type="primary"):
            if choice != card["profile_type"]:
                card["extra"] = {}
            card["profile_type"] = choice
            go(2)
        if c2.button("Cancel"):
            st.session_state.wizard = None
            st.rerun()

    elif step == 2:
        form, preview = st.columns([1, 1], gap="large")
        with form:
            ui.label(model.PROFILE_LABELS[card["profile_type"]])
            ident = card["identity"]
            c1, c2 = st.columns(2)
            st.session_state.setdefault("wz_org", ident["organisation"])
            st.session_state.setdefault("wz_role", ident["role"])
            st.session_state.setdefault("wz_id_country", ident["country"])
            ident["organisation"] = c1.text_input("Organisation", key="wz_org")
            ident["role"] = c2.text_input("Your role", key="wz_role")
            ident["country"] = st.selectbox("Country", model.COUNTRIES, key="wz_id_country")
            bind(st.multiselect, "sectors", "Sectors (1 to 3)", options=model.SECTORS, max_selections=3)
            bind(st.text_area, "looking_for", "What problem or capability are you scouting?", height=100)
            bind(st.multiselect, "engagement_type", "How you want to engage", options=model.ENGAGEMENT_TYPES)
            key = "wz_maturity_accepted"
            if key not in st.session_state:
                st.session_state[key] = tuple(card["maturity_accepted"])
            card["maturity_accepted"] = list(st.slider("Maturity you accept", 1, 5, key=key))
            lo, hi = card["maturity_accepted"]
            ui.md(f'<div class="tb-muted">From "{model.MATURITY[lo]}" to "{model.MATURITY[hi]}"</div>')
            bind(st.multiselect, "what_they_bring", "What you bring", options=model.WHAT_THEY_BRING)
            c1, c2 = st.columns(2)
            with c1:
                bind(st.selectbox, "ip_expectation", "IP expectation", options=model.IP_EXPECTATION)
            with c2:
                bind(st.selectbox, "equity_expected", "Equity expected", options=model.EQUITY_BUSINESS)
            bind(st.multiselect, "geography_accepted", "Geography accepted",
                 options=[model.EUROPE_WIDE] + model.COUNTRIES)
            t = card["timeline"]
            c1, c2, c3 = st.columns(3)
            for col, field, label in ((c1, "start", "Can start"), (c2, "signatory", "Who signs"),
                                      (c3, "budget", "Budget range")):
                st.session_state.setdefault(f"wz_t_{field}", t[field])
                t[field] = col.text_input(label, key=f"wz_t_{field}")
            bind(st.number_input, "time_commitment", "Time you can give (hours a month)", min_value=1, step=1)

            st.divider()
            ui.label(f"Specific to {model.PROFILE_LABELS[card['profile_type']]}")
            for field, (label, kind, options) in model.PROFILE_FIELDS[card["profile_type"]].items():
                key = f"wz_x_{field}"
                if key not in st.session_state:
                    default = {"bool": False, "int": 0, "text": "", "select": options and options[0]}[kind]
                    st.session_state[key] = card["extra"].get(field, default)
                if kind == "select":
                    card["extra"][field] = st.selectbox(label, options, key=key)
                elif kind == "bool":
                    card["extra"][field] = st.checkbox(label, key=key)
                elif kind == "int":
                    card["extra"][field] = st.number_input(label, min_value=0, step=1, key=key)
                else:
                    card["extra"][field] = st.text_input(label, key=key)
            st.write("")
            c1, c2 = st.columns(2)
            if c1.button("Back to profile type"):
                go(1)
            if c2.button("Continue", type="primary", disabled=not card["sectors"]):
                go(3)
        with preview:
            ui.label("Live preview · what researchers will see")
            ui.business_card(card)

    elif step == 3:
        form, preview = st.columns([1, 1], gap="large")
        with form:
            weights_and_visibility()
            st.write("")
            c1, c2, c3 = st.columns(3)
            if c1.button("Back"):
                go(2)

            def save(status):
                card["status"] = status
                store.save_card("business", card)
                st.session_state.wizard = None
                st.session_state.flash = ("Card published. Researchers can now find you."
                                          if status == "published" else "Draft saved.")
                st.rerun()

            if c2.button("Save as draft"):
                save("draft")
            if c3.button("Publish", type="primary"):
                save("published")
        with preview:
            ui.label("Live preview")
            ui.business_card(card)
