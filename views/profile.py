from datetime import date
from html import escape

import streamlit as st

import model
import store
import ui

role = ui.role()
persona = store.persona(role)
prof = store.profile(role)
cards = store.my_cards(role)
matches = store.my_matches(role)

TZ = ["Europe/Lisbon (WET)", "Europe/London (GMT)", "Europe/Rome (CET)", "Europe/Berlin (CET)", "Europe/Paris (CET)", "Europe/Madrid (CET)",
      "Europe/Amsterdam (CET)", "Europe/Stockholm (CET)", "Europe/Warsaw (CET)", "Europe/Athens (EET)", "Europe/Helsinki (EET)"]
LANGS = ["English", "Italian", "German", "French", "Spanish", "Dutch", "Portuguese", "Polish", "Swedish", "Norwegian", "Finnish", "Bulgarian", "Slovenian"]
CHANNELS = ["Email", "Video call", "Phone"]
RESPONSE = ["Within 24 hours", "Within 3 days", "Within a week"]

# (key, label, kind, options/help). The card already holds name, institution, field, sectors and maturity: none of that is repeated here.
SPEC = {
    "research": {
        "About you": [
            ("bio", "Short bio", "area", "Two or three sentences, in plain language. Shown to business after a match is accepted."),
            ("languages", "Languages", "multi", LANGS),
            ("timezone", "Time zone", "select", TZ),
        ],
        "Academic": [
            ("orcid", "ORCID iD", "text", "Format 0000-0000-0000-0000"),
            ("supervisor", "Supervisor", "text", ""),
            ("lab", "Lab or group", "text", ""),
            ("scholar", "Google Scholar or publications page", "text", ""),
            ("website", "Personal or lab website", "text", ""),
            ("publications", "Peer-reviewed publications", "number", ""),
            ("patents", "Patents filed", "number", ""),
            ("tto_name", "Technology Transfer Office", "text", "Who validates your cards"),
            ("tto_email", "TTO contact email", "text", ""),
        ],
        "Contact & availability": [
            ("email", "Email", "text", "Revealed only after both sides accept"),
            ("phone", "Phone (optional)", "text", ""),
            ("channel", "Preferred way to talk", "select", CHANNELS),
            ("office_hours", "When you are free to talk", "text", "e.g. Tue and Thu, 14:00-17:00"),
            ("response", "Usual reply time", "select", RESPONSE),
        ],
        "Preferences": [
            ("default_visibility", "Default visibility for new cards", "select", model.VISIBILITY),
            ("n_request", "Email me when I receive a new match request", "check", ""),
            ("n_deadline", "Remind me of next steps that are due", "check", ""),
            ("n_digest", "Weekly digest of new profiles that fit my cards", "check", ""),
        ],
    },
    "business": {
        "About you": [
            ("bio", "Short bio", "area", "Two or three sentences. Shown to researchers after a match is accepted."),
            ("languages", "Languages", "multi", LANGS),
            ("timezone", "Time zone", "select", TZ),
        ],
        "Organisation": [
            ("legal_name", "Legal name", "text", ""),
            ("website", "Website", "text", ""),
            ("linkedin", "LinkedIn page", "text", ""),
            ("hq", "Headquarters (city)", "text", ""),
            ("founded", "Year founded", "number", ""),
        ],
        "Process & team": [
            ("decision_weeks", "Typical time from first call to decision (weeks)", "number", ""),
            ("nda_ready", "We can sign an NDA straight away", "check", "Shown as a badge on your card"),
            ("legal_name_contact", "Legal contact for NDA and IP", "text", ""),
            ("legal_email", "Legal contact email", "text", ""),
            ("team", "Colleagues who also follow your matches (one per line)", "area", "Name, role"),
        ],
        "Contact & availability": [
            ("email", "Email", "text", "Revealed only after both sides accept"),
            ("phone", "Phone (optional)", "text", ""),
            ("channel", "Preferred way to talk", "select", CHANNELS),
            ("office_hours", "When you are free to talk", "text", ""),
            ("response", "Usual reply time", "select", RESPONSE),
        ],
        "Preferences": [
            ("n_request", "Email me when I receive a new match request", "check", ""),
            ("n_deadline", "Remind me of next steps that are due", "check", ""),
            ("n_digest", "Weekly digest of new researchers that fit my card", "check", ""),
        ],
    },
}[role]

# Completeness counts the fields that help the other side decide to trust you
TRACKED = ["bio", "languages", "email", "office_hours", "orcid", "supervisor", "lab", "tto_email"] if role == "research" else \
          ["bio", "languages", "email", "office_hours", "website", "legal_name", "legal_email", "linkedin"]


def filled(v):
    return bool(v) if not isinstance(v, (int, float)) or isinstance(v, bool) else v > 0


done = sum(filled(prof.get(k)) for k in TRACKED)
pct = round(100 * done / len(TRACKED))
missing = [k for k in TRACKED if not filled(prof.get(k))]
LABEL = {k: lbl for tab in SPEC.values() for k, lbl, *_ in tab}

# ---------- Header ----------
verified = prof.get("verified") == "verified"
v_text = {"verified": "Verified", "pending": "Verification pending", "none": "Not verified"}[prof.get("verified", "none")]
what = "Institution" if role == "research" else "Organisation"
who_line = persona["headline"]
since = date.fromisoformat(prof["member_since"]).strftime("%b %Y")
with st.container(key="phead"):
    c1, c2 = st.columns([3, 1.1], vertical_alignment="center", gap="large")
    c1.markdown(
        f'<div class="tb-ph"><div class="tb-ph-av">{escape(persona["name"][0])}</div><div>'
        f'<div class="tb-label">{"Researcher" if role == "research" else "Industry"} profile</div>'
        f'<div class="tb-ph-n">{escape(persona["name"])}</div><div class="tb-muted">{escape(who_line)}</div>'
        f'<div class="tb-ph-chips"><span class="tb-tag">{what} {escape(v_text.lower())}</span><span class="tb-tag">Member since {since}</span></div></div></div>',
        unsafe_allow_html=True)
    c2.markdown(ui.ring(pct, "complete"), unsafe_allow_html=True)

n_live = sum(m["status"] in model.ACCEPTED_STATUSES for m in matches)
t = st.columns(3, gap="medium")
t[0].markdown(ui.tile("Cards live", sum(c["status"] == "published" for c in cards), f"of {len(cards)}", "published and visible"), unsafe_allow_html=True)
t[1].markdown(ui.tile("Conversations", n_live, "live", f"{len(matches)} matches in total"), unsafe_allow_html=True)
t[2].markdown(ui.tile("Reply time", prof.get("response", "–").replace("Within ", ""), "", "what others see"), unsafe_allow_html=True)

if missing:
    ui.note("To reach 100%, add: " + ", ".join(LABEL[k].lower() for k in missing[:4]) + ("…" if len(missing) > 4 else "") + ".")
flash = st.session_state.pop("profile_flash", None)
if flash:
    ui.note(flash)

# ---------- Verification ----------
if prof.get("verified") != "verified":
    with st.container(border=True):
        a, b = st.columns([3, 1], vertical_alignment="center")
        a.markdown(f'<div class="tb-r-t">Verify your {what.lower()}</div><div class="tb-r-s" style="white-space:normal">'
                   f'A verified profile gets answered more often. {"We check the email against your institution." if role == "research" else "We check the email domain against your organisation."}</div>',
                   unsafe_allow_html=True)
        if prof.get("verified") == "pending":
            b.button("Request sent", disabled=True, use_container_width=True, key="verify_sent")
        elif b.button("Request verification", type="primary", use_container_width=True, key="verify"):
            store.update_profile(role, verified="pending")
            st.rerun()

# ---------- Editable sections ----------
tabs = st.tabs(list(SPEC))
for tab, (title, fields) in zip(tabs, SPEC.items()):
    with tab:
        with st.form(f"pf_{role}_{title}", border=False):
            vals = {}

            def draw(host, key, label, kind, extra):
                k = f"pf_{role}_{key}"
                cur = prof.get(key)
                if kind == "text":
                    vals[key] = host.text_input(label, value=cur or "", help=extra or None, key=k)
                elif kind == "area":
                    vals[key] = host.text_area(label, value=cur or "", help=extra or None, height=110, key=k)
                elif kind == "number":
                    vals[key] = host.number_input(label, value=int(cur or 0), min_value=0, step=1, key=k)
                elif kind == "select":
                    opts = list(extra)
                    vals[key] = host.selectbox(label, opts, index=opts.index(cur) if cur in opts else 0, key=k)
                elif kind == "multi":
                    vals[key] = host.multiselect(label, extra, default=cur or [], key=k)
                elif kind == "check":
                    vals[key] = host.checkbox(label, value=bool(cur), help=extra or None, key=k)

            # long text first, then short fields two per row (so labels and inputs line up), then switches
            for f in (x for x in fields if x[2] == "area"):
                draw(st, *f)
            small = [x for x in fields if x[2] not in ("area", "check")]
            for i in range(0, len(small), 2):
                row = st.columns(2, gap="large")
                for col, f in zip(row, small[i:i + 2]):
                    draw(col, *f)
            for f in (x for x in fields if x[2] == "check"):
                draw(st, *f)
            if st.form_submit_button("Save changes", type="primary"):
                store.update_profile(role, **vals)
                st.session_state.profile_flash = f"{title} saved."
                st.rerun()
