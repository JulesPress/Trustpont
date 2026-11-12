from html import escape

import streamlit as st

import matching
import model
import store
import ui
import worldmap

role = ui.role()
persona = store.persona(role)
mine = [c for c in store.my_cards(role) if c["status"] != "draft"]

if not mine:
    st.title("Browse business" if role == "research" else "Browse research")
    ui.note("Publish a card first: scores are computed against it.")
    st.stop()


def card_label(card_id):
    c = store.get_card(role, card_id)
    return c["title"] if role == "research" else f"{model.PROFILE_LABELS[c['profile_type']]} · {ui.business_name(c)}"


ids = [c["id"] for c in mine]
current = st.session_state.get("browse_card")

# ---------- One section: a satellite map with everything floating on it ----------
with st.container(key="brtop"):
    c_card, c_filter, c_count = st.columns([3.2, 1.1, 1.3], vertical_alignment="center", gap="small")
    # Unkeyed on purpose: a keyed selectbox keeps showing a stale choice when its options change
    st.session_state.browse_card = c_card.selectbox(
        "Scores computed against", ids, index=ids.index(current) if current in ids else 0, format_func=card_label, label_visibility="collapsed")
    me = store.get_card(role, st.session_state.browse_card)
    with c_filter.popover("Filters", icon=":material/tune:", use_container_width=True):
        sectors = st.multiselect("Sector", model.SECTORS)
        if role == "research":
            types = st.multiselect("Profile type", model.PROFILE_TYPES, format_func=model.PROFILE_LABELS.get)
            accepts = st.checkbox(f"Accepts my maturity ({me['maturity_level']})")
            engagement = st.multiselect("Engagement type", model.ENGAGEMENT_TYPES)
            country = st.selectbox("Works with", ["Any country"] + model.COUNTRIES)
        else:
            maturity = st.slider("Maturity", 1, 5, (1, 5))
            ip = st.multiselect("IP status", model.IP_STATUS)
            engagement = st.multiselect("Open to", model.ENGAGEMENT_TYPES)
            country = st.selectbox("Based in", ["Any country"] + model.COUNTRIES)


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


def country_of(c):
    return c["identity"]["country"] if role == "research" else c["owner"]["country"]


by_country = {}
for r in rows:
    by_country.setdefault(country_of(r[1]), []).append(r)
picked = st.session_state.get("map_country")
if picked not in by_country:
    picked = None
c_count.markdown(f'<div class="tb-brcount"><b>{len(rows)}</b> profiles</div>', unsafe_allow_html=True)

# ---------- The map (full bleed) ----------
with st.container(key="bmap"):
    fig = worldmap.build(by_country, picked, role, st.session_state.get("theme", "warm"))
    event = st.plotly_chart(fig, on_select="rerun", selection_mode="points", key=f"map_{picked}",
                            config={"displayModeBar": False, "scrollZoom": True}, use_container_width=True)
    pts = (event or {}).get("selection", {}).get("points", []) if event else []
    if pts and pts[0].get("customdata"):
        new = pts[0]["customdata"]
        new = new[0] if isinstance(new, (list, tuple)) else new
        if new in by_country and new != picked:
            st.session_state.map_country = new
            st.rerun()

# ---------- Floating glass list of matches (reference: gradient cards, name left, picture right) ----------
shown = by_country.get(picked, []) if picked else rows
with st.container(key="brpanel"):
    head_l, head_r = st.columns([3, 1.3], vertical_alignment="center", gap="small")
    head_l.markdown(f'<div class="tb-brh"><b>{escape(picked) if picked else "All matches"}</b>'
                    f'<span>{len(shown)} profile{"s" if len(shown) != 1 else ""} · best first</span></div>', unsafe_allow_html=True)
    if picked and head_r.button("Show all", key="map_all", use_container_width=True):
        st.session_state.map_country = None
        st.rerun()
    if not shown:
        ui.md('<div class="tb-brh"><span>No profiles match these filters.</span></div>')
    for s, c, rc, bc in shown:
        existing = store.find_match(rc["id"], bc["id"])
        open_match = bool(existing and existing["status"] != model.DECLINED)
        title = ui.business_name(c) if role == "research" else c["title"]
        sector = (c["sectors"] or ["Energy"])[0]
        photo = ui.PHOTO_FOR.get(sector, "materials")
        tone = "hi" if s["mutual"] > 75 else "mid" if s["mutual"] >= 50 else "lo"
        where = country_of(c)
        with st.container(key=f"bm_{c['id']}"):
            ui.md(f'<div class="tb-bm {tone}"><div class="tb-bm-l"><div class="tb-bm-t">{escape(title)}</div><div class="tb-bm-s">{escape(sector)} · {escape(where)}</div></div>'
                  f'<div class="tb-bm-img" style="background-image:url(/app/static/photos/{photo}.jpg)"></div><div class="tb-bm-sc">{s["mutual"]}</div></div>')
            with st.container(key=f"bmb_{c['id']}"):
                if open_match:
                    if st.button("OPEN MATCH  ↗", key=f"open_{c['id']}"):
                        ui.open_match(existing["id"])
                elif st.button("SEND REQUEST  ↗", key=f"send_{c['id']}"):
                    note = (f"Hello, I think my work on \"{me['title']}\" could fit what you are scouting." if role == "research"
                            else f"Hello, {ui.business_name(me)} would like to discuss your work.")
                    m = store.create_match(rc["id"], bc["id"], role, persona["name"], note)
                    ui.open_match(m["id"])

with st.container(key="brleg"):
    ui.md('<div class="tb-brleg"><span><i class="hi"></i>Strong</span><span><i class="mid"></i>Possible</span><span><i class="lo"></i>Weak</span>'
          '<em>Click a pin · scroll to zoom</em></div>')

st.markdown("<style>.block-container { padding-bottom: 0 !important; }</style>", unsafe_allow_html=True)
