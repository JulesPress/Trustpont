from functools import lru_cache
from pathlib import Path

import streamlit as st
from PIL import Image

STATIC = Path(__file__).parent / "static" / "partners"

# Official names of the ENGAGE.EU alliance members. The logos are the official files (Wikimedia Commons, each university's own site),
# turned into single-colour white shapes so they read as one calm row, like a client-logo marquee.
PARTNERS = [
    ("ENGAGE.EU", "European University", "engage"),
    ("University of Mannheim", "Germany", "mannheim"),
    ("Université Toulouse Capitole", "France", "toulouse"),
    ("LUISS Guido Carli", "Italy", "luiss"),
    ("NHH Norwegian School of Economics", "Norway", "nhh"),
    ("University of National and World Economy", "Bulgaria", "unwe"),
    ("WU Vienna University of Economics and Business", "Austria", "wu"),
    ("Ramon Llull University", "Spain", "ramon-llull"),
    ("Tilburg University", "Netherlands", "tilburg"),
    ("Hanken School of Economics", "Finland", "hanken"),
    ("University of St.Gallen", "Switzerland", "st-gallen"),
]


@lru_cache(maxsize=None)
def _height_rem(slug):
    """Optical balance: wide wordmarks sit lower, seals and squares sit taller."""
    w, h = Image.open(STATIC / f"{slug}.png").size
    r = w / h
    return round(1.3 * (1.35 if r >= 4.5 else 1.75 if r >= 3 else 2.3 if r >= 1.8 else 2.9 if r >= 1.3 else 3.1 if r >= 0.8 else 3.5), 2)


def render():
    items = ""
    for name, sub, slug in PARTNERS:
        items += (f'<div class="tb-pt" title="{name}"><div class="tb-pt-logo"><img src="/app/static/partners/{slug}.png" alt="{name}" '
                  f'style="height:{_height_rem(slug)}rem"></div><div class="tb-pt-name">{name}</div></div>')
    st.markdown(
        f'''<section class="tb-alliance">
  <div class="tb-alliance-head"><b>The ENGAGE.EU alliance</b><span>Ten European universities, one network. Trustpont was built during the ENGAGE.EU Expedition+ week.</span></div>
  <div class="tb-marquee" aria-label="ENGAGE.EU member universities"><div class="tb-track">{items}{items}</div></div>
</section>''', unsafe_allow_html=True)
