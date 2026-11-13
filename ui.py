# Rendering helpers shared by both sides of the app.
from datetime import date
from html import escape

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


def tile(name, value, unit="", sub="", icon="◎", variant=""):
    """Health Karma style bento tile: round icon, label, huge numeral, black arrow."""
    u = f"<small>{escape(unit)}</small>" if unit else ""
    sb = f'<div class="tb-sub">{escape(sub)}</div>' if sub else ""
    return (f'<div class="tb-tile {variant}"><div><div class="tb-ico">{icon}</div>'
            f'<div class="tb-tname">{escape(name)}</div></div>'
            f'<div><div class="tb-num">{escape(str(value))}{u}</div>{sb}</div><div class="tb-go">\u2197</div></div>')


def ring(score, caption=None):
    """Circular match gauge with the verdict underneath, like the 79% 'Strong match' ring in the Orion reference."""
    if score is None:
        return '<div class="tb-ring low"><div class="tb-rc"><div class="tb-rn">n/a</div></div></div>'
    level = "high" if score > 75 else "mid" if score >= 50 else "low"
    verdict = caption or {"high": "Strong match", "mid": "Possible match", "low": "Weak match"}[level]
    r = 42
    c = 2 * 3.14159 * r
    off = c * (1 - max(0, min(score, 100)) / 100)
    return (f'<div class="tb-ring {level}"><svg viewBox="0 0 100 100"><circle class="trk" cx="50" cy="50" r="{r}" fill="none" stroke-width="7"/>'
            f'<circle class="arc" cx="50" cy="50" r="{r}" fill="none" stroke-width="7" stroke-dasharray="{c:.1f}" stroke-dashoffset="{off:.1f}"/></svg>'
            f'<div class="tb-rc"><div class="tb-rn">{score}<small>%</small></div><div class="tb-rl">{escape(verdict)}</div></div></div>')


def big_score(score, sub=""):
    if score is None:
        return '<div class="tb-bigscore">n/a</div>'
    level = "high" if score > 75 else "mid" if score >= 50 else "low"
    s = f"<small>{escape(sub)}</small>" if sub else ""
    return f'<div class="tb-bigscore {level}">{score}{s}</div>'


def gauge(share, center, caption):
    """Semicircle gauge, like the credit score dial in the reference."""
    import math
    share = max(0.0, min(share, 1.0))
    r, cx, cy = 80, 100, 95
    ex, ey = cx - r * math.cos(math.pi * share), cy - r * math.sin(math.pi * share)
    big = 0
    arc = f'<path d="M {cx - r} {cy} A {r} {r} 0 {big} 1 {ex:.1f} {ey:.1f}" class="g-arc" stroke-width="10" fill="none" stroke-linecap="round"/>' if share > 0 else ""
    return (f'<div class="tb-gauge"><svg viewBox="0 0 200 105"><path d="M {cx - r} {cy} A {r} {r} 0 0 1 {cx + r} {cy}" '
            f'class="g-trk" stroke-width="10" fill="none" stroke-linecap="round"/>{arc}'
            f'<circle class="g-dot" cx="{ex:.1f}" cy="{ey:.1f}" r="5" stroke-width="2.5"/></svg>'
            f'<div class="tb-gnum">{escape(center)}</div><div class="tb-muted" style="margin-top:0.4rem">{escape(caption)}</div></div>')


def _short(text, n=120):
    text = (text or "").strip()
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + "…"


def stage_item_research(rc, score=None):
    return {"kicker": "Research", "score": score, "initial": (rc["title"] or "R")[0].upper(),
            "title": rc["title"] or "Untitled card", "sub": f"{rc['owner']['field']} · {rc['owner']['country']}"
            if rc["visibility"] != "anonymous" else f"Anonymous · {rc['owner']['field']}",
            "body": rc["key_problem"], "tags": rc["sectors"][:3],
            "left": f"Maturity {rc['maturity_level']}", "right": rc["equity_expected"] or ""}


def stage_item_business(bc, score=None):
    name = business_name(bc)
    return {"kicker": model.PROFILE_LABELS[bc["profile_type"]], "score": score, "initial": name[0].upper(),
            "title": name, "sub": f"{bc['identity']['role']} · {bc['identity']['country']}",
            "body": bc["looking_for"], "tags": bc["sectors"][:3],
            "left": f"Maturity {bc['maturity_accepted'][0]}-{bc['maturity_accepted'][1]}", "right": bc["equity_expected"] or ""}


def _glass(it, pos):
    if it is None:
        return '<div class="tb-gc empty"></div>'
    cls = {"-1": "side left", "0": "", "1": "side right"}[str(pos)]
    score = f'Match <b>{it["score"]}</b>' if it["score"] is not None else ""
    tg = "".join(f"<span>{escape(t)}</span>" for t in it["tags"])
    return (f'<div class="tb-gc {cls}"><div class="tb-gtop"><span>{escape(it["kicker"])}</span><span>{score}</span></div>'
            f'<div class="tb-gmid"><div class="tb-av">{escape(it["initial"])}</div><div class="tb-gname">{escape(it["title"])}</div>'
            f'<div class="tb-gsub">{escape(it["sub"])}</div><div class="tb-gbody">{escape(_short(it["body"]))}</div>'
            f'<div class="tb-gtags">{tg}</div></div>'
            f'<div class="tb-gfoot"><span>{escape(it["left"])}</span><b>{escape(it["right"])}</b></div></div>')


_STAGE_HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
:root{__VARS__}
*{box-sizing:border-box;margin:0}
html,body{height:100%;background:transparent;font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','SF Pro Text',system-ui,'Helvetica Neue',Arial,sans-serif;font-synthesis:none;color:#fff;overflow:hidden}
.stage{position:relative;height:100%;border-radius:28px;overflow:hidden;background:var(--stage-bg)}
.orb{display:none;position:absolute;border-radius:50%;filter:blur(60px);opacity:.40;animation:drift 14s ease-in-out infinite alternate}
.o1{width:300px;height:300px;background:#00A4FF;left:-60px;top:-80px}
.o2{width:340px;height:340px;background:#00E7FF;right:-80px;bottom:-120px;animation-delay:-5s}
.o3{width:220px;height:220px;background:#0040FF;right:22%;top:-90px;animation-delay:-9s}
@keyframes drift{from{transform:translate(0,0) scale(1)}to{transform:translate(50px,30px) scale(1.15)}}
h2{position:absolute;top:26px;left:0;right:0;text-align:center;font-weight:600;font-size:30px;letter-spacing:-.035em;z-index:5;color:var(--t)}
.track{position:absolute;left:0;right:0;top:92px;bottom:70px;perspective:1300px}
.card{position:absolute;left:50%;top:50%;width:300px;height:320px;margin:-160px 0 0 -150px;padding:16px 20px;border-radius:22px;
 background:var(--card-ov),var(--bgimg) center/cover;
 border:1px solid var(--card-bd);box-shadow:0 18px 44px rgba(10,30,15,.30),inset 0 1px 0 rgba(255,255,255,.28);
 display:flex;flex-direction:column;will-change:transform,opacity;user-select:none}
.top{display:flex;justify-content:space-between;font-size:12px;color:rgba(255,255,255,.6)}
.top b{color:#fff;font-weight:600}
.mid{flex:1;text-align:center;margin-top:14px}
.av{width:58px;height:58px;border-radius:50%;background:rgba(255,255,255,.22);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);margin:0 auto 10px;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:600}
.name{font-size:17px;font-weight:600;letter-spacing:-.02em;line-height:1.2}
.sub{font-size:12.5px;color:rgba(255,255,255,.55);margin:3px 0 9px}
.body{font-size:12.5px;color:rgba(255,255,255,.8);line-height:1.45;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
.tags{margin-top:9px}.tags span{display:inline-block;font-size:11px;padding:1px 9px;margin:0 3px 3px 0;border-radius:99px;background:rgba(255,255,255,.14)}
.foot{display:flex;justify-content:space-between;font-size:11.5px;color:rgba(255,255,255,.55)}.foot b{color:#fff}
.nav{position:absolute;bottom:20px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:10px;z-index:6}
.btn{width:22px;height:22px;padding:0;display:flex;align-items:center;justify-content:center;border:none;background:transparent;color:var(--t);opacity:.5;cursor:pointer;transition:opacity .2s}
.btn svg{width:13px;height:13px;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.btn:hover{opacity:1}
.pager{display:flex;align-items:center;gap:6px}
.dot{width:5px;height:5px;padding:0;border:none;border-radius:99px;background:var(--t);opacity:.22;cursor:pointer;transition:width .3s ease,opacity .3s ease}
.dot.on{width:16px;opacity:.85}
</style></head><body><div class="stage"><div class="orb o1"></div><div class="orb o2"></div><div class="orb o3"></div>
<h2 id="t"></h2><div class="track" id="track"></div>
<div class="nav"><button class="btn" id="prev" aria-label="Previous"><svg viewBox="0 0 16 16"><path d="M10 3 5 8l5 5"/></svg></button><div class="pager" id="pager"></div><button class="btn" id="next" aria-label="Next"><svg viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></button></div></div>
<script>
const items=__ITEMS__, n=items.length, track=document.getElementById('track'), pager=document.getElementById('pager');
document.getElementById('t').textContent=__TITLE__;
const MEADOWS=['green','mist','green','mist'];
const els=items.map((it,i)=>{const c=document.createElement('div');c.className='card';c.style.setProperty('--bgimg','url(/app/static/meadow/'+MEADOWS[i%4]+'.jpg)');
 const mk=(t,cls,txt)=>{const e=document.createElement(t);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e};
 const top=mk('div','top');top.append(mk('span',0,it.kicker));const sc=mk('span');if(it.score!=null){sc.append('Match ');sc.append(mk('b',0,it.score))}top.append(sc);
 const mid=mk('div','mid');mid.append(mk('div','av',it.initial),mk('div','name',it.title),mk('div','sub',it.sub),mk('div','body',it.body));
 const tg=mk('div','tags');(it.tags||[]).forEach(t=>tg.append(mk('span',0,t)));mid.append(tg);
 const f=mk('div','foot');f.append(mk('span',0,it.left),mk('b',0,it.right));c.append(top,mid,f);track.append(c);
 return c});
const dotEls=items.map((_,i)=>{const d=document.createElement('button');d.className='dot';d.setAttribute('aria-label','Card '+(i+1));d.onclick=()=>{target=Math.round(target)+wrap(i-Math.round(target))};pager.append(d);return d});
let pos=0,target=0,hover=false,down=null,last=performance.now();
const wrap=v=>{v=((v%n)+n)%n;return v>n/2?v-n:v};
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
function render(){const cur=((Math.round(pos)%n)+n)%n;
 els.forEach((c,i)=>{const d=wrap(i-pos),a=Math.abs(d);
  const x=d*250,z=-Math.min(a,2.5)*140,ry=Math.max(-52,Math.min(52,-d*30)),s=1-Math.min(a,2)*.05;
  c.style.transform=`translateX(${x}px) translateZ(${z}px) rotateY(${ry}deg) scale(${s})`;
  c.style.opacity=a>2.4?0:(1-Math.max(0,a-.2)*.28);c.style.zIndex=100-Math.round(a*10);c.style.pointerEvents=a>2.4?'none':'auto'});
 dotEls.forEach((e,i)=>e.classList.toggle('on',i===cur))}
function tick(t){const dt=Math.min(t-last,50)/1000;last=t;pos+=(target-pos)*(1-Math.pow(.0009,dt));render();requestAnimationFrame(tick)}
let timer=setInterval(()=>{if(!hover&&!down&&!reduce&&n>1)target+=1},3200);
const st=document.querySelector('.stage');st.onmouseenter=()=>hover=true;st.onmouseleave=()=>hover=false;
document.getElementById('next').onclick=()=>target=Math.round(target)+1;
document.getElementById('prev').onclick=()=>target=Math.round(target)-1;
st.onpointerdown=e=>{down={x:e.clientX,t:target}};
st.onpointermove=e=>{if(down)target=down.t-(e.clientX-down.x)/250};
window.onpointerup=()=>{if(down){target=Math.round(target);down=null}};
if(n<2){document.querySelector('.nav').style.display='none'}
requestAnimationFrame(tick);
</script></body></html>"""


def card_stage(items, key, title="", height=500):
    """Auto-rotating 3D carousel of glass cards (JS in an iframe): drifts on its own, pauses on hover, drag or arrows to move."""
    if not items:
        return None
    import json
    import streamlit.components.v1 as components
    safe = json.dumps(items).replace("</", "<\\/")
    themes = {
        "warm": "--stage-bg:linear-gradient(rgba(14,30,18,.10),rgba(14,30,18,.22)),url(/app/static/meadow/green.jpg) center/cover;--card-ov:linear-gradient(rgba(16,34,20,.34),rgba(16,34,20,.50));--card-bd:rgba(255,255,255,.32);--t:#FFFFFF;--t2:rgba(255,255,255,.86);--bb:rgba(255,255,255,.55);--bhc:#1E3A22;",
        "azure": "--stage-bg:linear-gradient(rgba(6,14,40,.45),rgba(6,14,40,.60)),url(/app/static/meadow/mist.jpg) center/cover;--card-ov:linear-gradient(rgba(8,16,44,.42),rgba(8,16,44,.60));--card-bd:rgba(190,205,255,.30);--t:#FFFFFF;--t2:#DCE6FF;--bb:rgba(255,255,255,.45);--bhc:#0A1636;",
    }
    vars_ = themes.get(st.session_state.get("theme", "warm"), themes["warm"])
    page = _STAGE_HTML.replace("__VARS__", vars_).replace("__ITEMS__", safe).replace("__TITLE__", json.dumps(title).replace("</", "<\\/"))
    if hasattr(st, "iframe"):  # newer Streamlit; components.v1.html is deprecated there
        st.iframe(page, height=height)
    else:
        components.html(page, height=height)
    return 0


PIPE_LABELS = {"not contacted": "Requested", "contacted": "Contacted", "meeting scheduled": "Meeting",
               "active collaboration": "Active", "closed": "Closed", "declined": "Declined"}


def stage_flow(counts):
    """Minimal progress line: five stages, one number each. Declined is shown quietly at the end."""
    steps = model.STATUSES
    cells = "".join(f'<div class="tb-sf{" on" if counts.get(x) else ""}"><b>{counts.get(x, 0)}</b><span>{PIPE_LABELS[x]}</span></div>'
                    for x in steps)
    d = counts.get(model.DECLINED, 0)
    return f'<div class="tb-flow">{cells}</div><div class="tb-muted" style="margin-top:0.5rem">{d} declined</div>'


def tags(items):
    return "".join(f'<span class="tb-tag">{escape(str(i))}</span>' for i in items)


def note(text):
    # Single-accent replacement for st.info / st.success / st.warning
    md(f'<div class="tb-note">{escape(text)}</div>')


def label(text):
    md(f'<div class="tb-label">{escape(text)}</div>')


def euros(n):
    return f"EUR\u00a0{n:,.0f}".replace(",", "\u00a0")


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

def _text(t):
    return escape(t or "—").replace("\n", "<br>")


def _block(label_, body, wide=False):
    return f'<div class="tb-block{" wide" if wide else ""}"><div class="tb-label">{escape(label_)}</div><div>{body}</div></div>'


def _fact(label_, value):
    return f'<div class="tb-fact"><div class="tb-label">{escape(label_)}</div><div class="tb-fv">{escape(str(value))}</div></div>'


def _head(kicker, title, sub, score, initial):
    sc = f'<div class="tb-chs">{score_badge(score)}</div>' if score is not None else ""
    return (f'<div class="tb-ch"><div class="tb-avl">{escape((initial or "?")[0].upper())}</div>'
            f'<div class="tb-chm"><div class="tb-label">{kicker}</div><div class="tb-ct">{escape(title)}</div>'
            f'<div class="tb-muted">{sub}</div></div>{sc}</div>')


# --- Poster card (My cards): a peak rising out of clouds, glass chips, white pill + round arrow ---

def _art(seed):
    """Deterministic mountain-above-clouds picture: every card gets its own summit, ridge line and cloud bank."""
    import hashlib
    import random
    h = hashlib.md5(seed.encode()).hexdigest()
    r = random.Random(int(h[:8], 16))
    uid = h[:6]
    W, H = 400, 330
    px = r.randint(150, 250)            # summit x
    py = r.randint(70, 120)             # summit y
    base = 250
    # main peak: jagged left slope, jagged right slope
    left = [(px, py)]
    x, y = px, py
    while x > 20:
        x -= r.randint(18, 34); y += r.randint(10, 30)
        left.append((x, min(y, base)))
    right = [(px, py)]
    x, y = px, py
    while x < 380:
        x += r.randint(18, 34); y += r.randint(8, 26)
        right.append((x, min(y, base)))
    lit_pts = [left[0]] + left[1:] + [(left[-1][0], base + 20), (px + 8, base + 20)]
    pts = " ".join(f"{a},{b}" for a, b in lit_pts)
    shade_pts = " ".join(f"{a},{b}" for a, b in [right[0]] + right[1:] + [(right[-1][0], base + 20), (px + 8, base + 20)])
    snow = " ".join(f"{a},{b}" for a, b in [(px, py), left[1], (px - 12, py + 30), (px - 3, py + 21), (px + 7, py + 34), (px + 17, py + 25), right[1]])
    # far ridge
    ridge = "M0 200 " + " ".join(f"L{i * 40} {200 - r.randint(10, 60)}" for i in range(1, 11)) + f" L400 {H} L0 {H} Z"
    clouds_back = "".join(f'<ellipse cx="{r.randint(0, 400)}" cy="{r.randint(205, 245)}" rx="{r.randint(60, 120)}" ry="{r.randint(16, 28)}"/>' for _ in range(6))
    clouds_front = "".join(f'<ellipse cx="{r.randint(-20, 420)}" cy="{r.randint(255, 330)}" rx="{r.randint(80, 160)}" ry="{r.randint(24, 46)}"/>' for _ in range(7))
    sparks = "".join(
        f'<path d="M{sx} {sy - 4} L{sx + 1.2} {sy - 1.2} L{sx + 4} {sy} L{sx + 1.2} {sy + 1.2} L{sx} {sy + 4} L{sx - 1.2} {sy + 1.2} L{sx - 4} {sy} L{sx - 1.2} {sy - 1.2} Z"/>'
        for sx, sy in ((r.randint(20, 380), r.randint(28, 110)) for _ in range(r.randint(3, 5))))
    return (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs>'
            f'<linearGradient id="s{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--art-sky-top)"/><stop offset="1" style="stop-color:var(--art-sky-bottom)"/></linearGradient>'
            f'<radialGradient id="g{uid}" cx="{px / W:.2f}" cy="{(py + 40) / H:.2f}" r=".55"><stop offset="0" style="stop-color:var(--art-glow)" stop-opacity=".85"/><stop offset="1" style="stop-color:var(--art-glow)" stop-opacity="0"/></radialGradient>'
            f'<filter id="b{uid}"><feGaussianBlur stdDeviation="9"/></filter></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#s{uid})"/><rect width="{W}" height="{H}" fill="url(#g{uid})"/>'
            f'<path d="{ridge}" style="fill:var(--art-ridge)" opacity=".55"/>'
            f'<g style="fill:var(--art-cloud)" filter="url(#b{uid})" opacity=".55">{clouds_back}</g>'
            f'<polygon points="{pts}" style="fill:var(--art-lit)"/><polygon points="{shade_pts}" style="fill:var(--art-shade)"/>'
            f'<polygon points="{snow}" style="fill:var(--art-snow)" opacity=".92"/>'
            f'<g style="fill:var(--art-cloud)" filter="url(#b{uid})" opacity=".95">{clouds_front}</g>'
            f'<g style="fill:var(--art-star)" opacity=".8">{sparks}</g></svg>')


PHOTO_FOR = {  # sector -> photo in static/photos
    "Energy": "energy", "Health & biotech": "health", "Agri-food": "agri", "Mobility & transport": "mobility", "Advanced materials": "materials",
    "Software & AI": "software", "Semiconductors & electronics": "software", "Environment & water": "environment", "Construction": "construction",
    "Finance & insurance": "finance", "Space & defence": "space", "Manufacturing & robotics": "construction",
}


def poster_card(card, role):
    first = (card["sectors"] or ["Energy"])[0]
    photo = PHOTO_FOR.get(first, "materials")
    if role == "research":
        title = card["title"] or "Untitled card"
        kicker = f'Maturity {card["maturity_level"]} of 5'
        stage = model.MATURITY[card["maturity_level"]]
        sub = card["key_problem"]
        who = card["owner"]["name"]
        level = card["maturity_level"]
        chip = card["status"] if card["visibility"] == "public" else f'{card["status"]} · {card["visibility"]}'
    else:
        title = business_name(card)
        kicker = model.PROFILE_LABELS[card["profile_type"]]
        stage = f'Accepts maturity {card["maturity_accepted"][0]}-{card["maturity_accepted"][1]}'
        sub = card["looking_for"]
        who = card["identity"]["name"]
        level = card["maturity_accepted"][1]
        chip = card["status"]
    steps = "".join(f'<i class="{"on" if i <= level else ""}"></i>' for i in range(1, 6))
    sectors = "".join(f"<span>{escape(s)}</span>" for s in card["sectors"][:3])
    spark = '<svg viewBox="0 0 16 16" class="tb-sp"><path d="M8 0l1.6 6.4L16 8l-6.4 1.6L8 16l-1.6-6.4L0 8l6.4-1.6z"/></svg>'
    html = (f'<div class="tb-poster"><div class="tb-photo" style="background-image:url(/app/static/photos/{photo}.jpg)"></div><div class="tb-pshade"></div>'
            f'<div class="tb-ptop"><div><div class="tb-pk">{escape(kicker)}</div><div class="tb-steps5">{steps}</div></div>'
            f'<span class="tb-pchip">{escape(chip)}</span></div>'
            f'<div class="tb-pbot"><div class="tb-glass"><div class="tb-pstage">{spark}{escape(stage)}</div><div class="tb-ptitle">{escape(title)}</div>'
            f'<div class="tb-psub">{escape(_short(sub, 100))}</div><div class="tb-psec">{sectors}</div>'
            f'<div class="tb-pfoot"><span>{escape(who)}</span></div></div><div class="tb-pcta"></div><span class="tb-parrow">&#8599;</span></div></div>')
    md(html)


def research_card(rc, revealed=True, show_part2=True, score=None, compact=False):
    who = (f'{escape(researcher_name(rc))} · {escape(rc["owner"]["country"])}' if revealed else
           f'{escape(researcher_name(rc, False))} · {escape(rc["geography"]["country"])} · identity revealed after mutual acceptance')
    title = rc["title"] or "Untitled card"
    html = _head(f'Research card · {escape(rc["status"])}', title, who, score, title)
    html += (f'<div class="tb-chips">{tags(rc["sectors"])}</div>'
             f'<div class="tb-muted">Maturity {escape(maturity_text(rc["maturity_level"]))}</div>{maturity_scale(rc["maturity_level"])}')
    blocks = [_block("The problem", _text(rc["key_problem"]), wide=compact)]
    if not compact:
        blocks += [_block("In plain words", _text(rc["plain_explanation"]))]
        if rc["concrete_examples"]:
            items = "".join(f"<li>{escape(e)}</li>" for e in rc["concrete_examples"] if e)
            blocks.append(_block("What it could do", f"<ul>{items}</ul>"))
        blocks += [_block("Where something similar worked", _text(rc["case_studies"])),
                   _block("Honest feasibility", _text(rc["feasibility"]))]
    html += f'<div class="tb-blocks">{"".join(blocks)}</div>'
    if not compact and show_part2:
        g = rc["geography"]
        extras = [x for x, ok in (("remote ok", g["remote"]), ("can relocate", g["relocate"])) if ok]
        html += '<div class="tb-label" style="margin-top:1.2rem">Business side</div>'
        html += (f'<div class="tb-blocks">{_block("Market problem", _text(rc["market_problem"]), True)}'
                 f'{_block("Draft business plan", _text(rc["draft_business_plan"]))}'
                 f'{_block("Go to market", _text(rc["go_to_market"]))}</div>')
        html += (f'<div class="tb-facts">{_fact("R&D to date", euros(rc["rd_costs_to_date"]))}'
                 f'{_fact("Capital needed", euros(rc["capital_needed"]))}{_fact("IP", rc["ip_status"])}'
                 f'{_fact("Equity on the table", rc["equity_expected"])}</div>')
        html += (f'<div class="tb-muted" style="margin-top:0.8rem">Needs</div>{tags(rc["support_needed"]) or "—"}'
                 f'<div class="tb-muted">Open to</div>{tags(rc["engagement_wanted"]) or "—"}'
                 f'<div class="tb-muted">Based in {escape(g["country"])}{" · " + ", ".join(extras) if extras else ""}</div>')
    with st.container(border=True):
        md(html)


def business_card(bc, score=None):
    i = bc["identity"]
    name = business_name(bc)
    lo, hi = bc["maturity_accepted"]
    html = _head(escape(model.PROFILE_LABELS[bc["profile_type"]]), name,
                 f'{escape(i["name"])} · {escape(i["role"])} · {escape(i["country"])}', score, name)
    html += (f'<div class="tb-chips">{tags(bc["sectors"])}</div>'
             f'<div class="tb-muted">Accepts maturity {lo} to {hi}</div>{maturity_scale(None, (lo, hi))}')
    html += f'<div class="tb-blocks">{_block("Looking for", _text(bc["looking_for"]), True)}'
    html += (f'{_block("Engagement", tags(bc["engagement_type"]) or "—")}{_block("Brings", tags(bc["what_they_bring"]) or "—")}</div>')
    html += (f'<div class="tb-facts three">{_fact("IP", bc["ip_expectation"])}{_fact("Equity", bc["equity_expected"])}'
             f'{_fact("Time / month", str(bc["time_commitment"]) + "\u00a0h")}</div>')
    t = bc["timeline"]
    html += (f'<div class="tb-muted" style="margin-top:0.8rem">Geography: {escape(", ".join(bc["geography_accepted"]))}<br>'
             f'Start: {escape(t["start"] or "—")} · Signs: {escape(t["signatory"] or "—")} · Budget: {escape(t["budget"] or "—")}</div>')
    details = []
    for key, (fname, kind, _) in model.PROFILE_FIELDS[bc["profile_type"]].items():
        value = bc["extra"].get(key)
        if value is None or value == "":
            continue
        if kind == "bool":
            value = "yes" if value else "no"
        elif kind == "int" and key.endswith("_eur"):
            value = euros(value)
        details.append(f"{fname}: {value}")
    if details:
        html += f'<div class="tb-muted">{escape(" · ".join(details))}</div>'
    with st.container(border=True):
        md(html)


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
    nonce = st.session_state.setdefault("table_nonce", 0)
    columns = list(rows[0])
    widths = [1.5, 0.6, 1, 1, 1, 1.2, 1.5, 0.8]
    headers = st.columns(widths)
    for column, heading in zip(headers, columns):
        column.caption(heading)
    for index, row in enumerate(rows):
        cells = st.columns(widths)
        for column, heading in zip(cells[:-1], columns):
            column.write(row[heading])
        if cells[-1].button("Open", key=f"{key}_{nonce}_{index}", use_container_width=True):
            st.session_state.table_nonce += 1
            open_match(matches[index]["id"])


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


# --- Dashboard widgets (stats-hero layout) ---

def band_gauge(scores, avg):
    """Score strip: three soft zones, one dot per match, a marker for the average (like the credit-score strip)."""
    dots = ""
    for i, s in enumerate(scores):
        top = (20, 52, 34, 62, 26)[i % 5]
        dots += f'<i style="left:{s}%;top:{top}%"></i>'
    marker = (f'<div class="tb-bg-mark" style="left:{avg}%"><span>&#9660;</span><b></b></div>'
              f'<div class="tb-bg-val" style="left:{avg}%">{avg}</div>') if avg is not None else ""
    return (f'<div class="tb-bg"><div class="tb-bg-zones"><div class="z1"></div><div class="z2"></div><div class="z3"></div>{dots}{marker}</div>'
            f'<div class="tb-bg-axis"><span style="left:0">0</span><span style="left:50%">50</span><span style="left:75%">75</span><span style="left:100%">100</span></div></div>')


def _smooth(pts):
    """Catmull-Rom to cubic Bezier path through the points."""
    if len(pts) < 3:
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d


def score_chart(rows):
    """rows: [(label, mutual, researcher, business)] in time order. Black main line, two faint lines, lime bubble on the best match."""
    W, H, L, R, T, B = 420, 190, 34, 12, 26, 34
    n = len(rows)
    lo, hi = 0, 100
    X = lambda i: L + (W - L - R) * (i / max(n - 1, 1))
    Y = lambda v: T + (H - T - B) * (1 - (v - lo) / (hi - lo))
    grid = "".join(f'<line x1="{L}" x2="{W - R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" class="cg"/><text x="{L - 8}" y="{Y(v) + 4:.1f}" class="ct" text-anchor="end">{v}</text>' for v in (0, 25, 50, 75, 100))
    series = lambda k: _smooth([(X(i), Y(r[k])) for i, r in enumerate(rows)])
    best = max(range(n), key=lambda i: rows[i][1])
    bx, by = X(best), Y(rows[best][1])
    labels = "".join(f'<text x="{X(i):.1f}" y="{H - 10}" class="ct" text-anchor="middle">{escape(rows[i][0][:9])}</text>' for i in (0, n - 1) if n > 1)
    return (f'<svg viewBox="0 0 {W} {H}" class="tb-chart">{grid}<path d="{series(2)}" class="cl2"/><path d="{series(3)}" class="cl3"/><path d="{series(1)}" class="cl1"/>'
            f'<line x1="{bx:.1f}" x2="{bx:.1f}" y1="{by + 14:.1f}" y2="{H - B + 6}" class="cb"/><path d="M{bx - 4:.1f},{H - B + 14} L{bx + 4:.1f},{H - B + 14} L{bx:.1f},{H - B + 7} Z" class="cm"/>'
            f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="15" class="cbub"/><text x="{bx:.1f}" y="{by + 4:.5}" text-anchor="middle" class="cbt">{rows[best][1]}</text>{labels}</svg>'
            f'<div class="tb-legend"><span><i class="l1"></i>Mutual</span><span><i class="l2"></i>Researcher weights</span><span><i class="l3"></i>Business weights</span></div>')


def match_gcard(name, mine, score, status, next_text, due_text):
    tone = "hi" if (score or 0) > 75 else "mid" if (score or 0) >= 50 else "lo"
    s = "n/a" if score is None else score
    return (f'<div class="tb-gc2 {tone}"><div class="tb-gc2-top"><div class="tb-gc2-ring"></div>'
            f'<div class="tb-gc2-name">{escape(name)}</div></div>'
            f'<div class="tb-gc2-row"><div><div class="tb-gc2-l">Match score</div><div class="tb-gc2-n">{s}<small>/100</small></div></div>'
            f'<div class="tb-gc2-r"><div class="tb-gc2-l">Stage</div><div class="tb-gc2-s">{escape(status)}</div></div></div>'
            f'<div class="tb-gc2-dots"></div>'
            f'<div class="tb-gc2-foot"><div><div class="tb-gc2-l">Next step</div><div class="tb-gc2-t">{escape(_short(next_text or "No next step", 60))}</div></div>'
            f'<div class="tb-gc2-d">{due_text}</div></div></div>')


def flow_diagram(counts):
    """Pipeline as a river: glowing strands run left to right through the five stages, thicker where more matches are."""
    steps = model.STATUSES
    W, H = 1000, 230
    xs = [90 + i * (W - 180) / (len(steps) - 1) for i in range(len(steps))]
    cy = 108
    n = [counts.get(s, 0) for s in steps]
    paths, nodes = "", ""
    for i in range(len(steps) - 1):
        # strands: several thin curves per link, spread by how many matches continue
        k = max(1, min(n[i + 1] + n[i], 6))
        for j in range(k):
            off = (j - (k - 1) / 2) * 7
            x0, x1 = xs[i] + 24, xs[i + 1] - 24
            mid = (x0 + x1) / 2
            paths += (f'<path d="M{x0:.0f},{cy + off * 0.4:.1f} C{mid:.0f},{cy + off * 1.6:.1f} {mid:.0f},{cy + off * 1.6:.1f} {x1:.0f},{cy + off * 0.4:.1f}" '
                      f'class="fl{" live" if n[i + 1] else ""}" style="animation-delay:{-(i * 0.7 + j * 0.35):.2f}s"/>')
    for i, s in enumerate(steps):
        on = n[i] > 0
        r = 24 + min(n[i], 6) * 1.6
        nodes += (f'<g class="fn{" on" if on else ""}"><circle cx="{xs[i]:.0f}" cy="{cy}" r="{r + 10:.0f}" class="fh"/><circle cx="{xs[i]:.0f}" cy="{cy}" r="{r:.0f}" class="fc"/>'
                  f'<text x="{xs[i]:.0f}" y="{cy + 8}" text-anchor="middle" class="fnum">{n[i]}</text>'
                  f'<text x="{xs[i]:.0f}" y="{cy + 62}" text-anchor="middle" class="flab">{escape(PIPE_LABELS[s].upper())}</text></g>')
    d = counts.get(model.DECLINED, 0)
    return (f'<div class="tb-river"><svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet">{paths}{nodes}</svg>'
            f'<div class="tb-river-foot"><span>{sum(n)} matches in the river</span><span>{d} declined</span></div></div>')


def stage_track(status):
    """Five small dots showing how far a match has travelled."""
    if status == model.DECLINED:
        return '<div class="tb-track5 off"><i></i><i></i><i></i><i></i><i></i><em>declined</em></div>'
    idx = model.STATUSES.index(status)
    dots = "".join(f'<i class="{"on" if k <= idx else ""}{" cur" if k == idx else ""}"></i>' for k in range(5))
    return f'<div class="tb-track5">{dots}<em>{escape(PIPE_LABELS[status])}</em></div>'


def cycle_section():
    """Culture -> Trust -> Value -> Culture: the self-feeding loop behind Trustpont, drawn as one calm diagram."""
    import math
    cx, cy, r, nr = 200, 190, 128, 40
    ang = {"Culture": -90, "Trust": 30, "Value": 150}
    pt = lambda a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
    order = ["Culture", "Trust", "Value"]
    gap = math.degrees(nr + 10) / r
    arcs = ""
    for i, k in enumerate(order):
        a0, a1 = ang[k] + gap, ang[order[(i + 1) % 3]] - gap
        if a1 < a0:
            a1 += 360
        (x0, y0), (x1, y1) = pt(a0), pt(a1)
        arcs += f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}" class="cy-arc" marker-end="url(#cyHead)" style="animation-delay:{-i * 1.1:.1f}s"/>'
    nodes = ""
    for k in order:
        x, y = pt(ang[k])
        nodes += f'<g class="cy-n"><circle cx="{x:.1f}" cy="{y:.1f}" r="{nr + 8}" class="cy-h"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{nr}" class="cy-c"/><text x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle" class="cy-t">{k}</text></g>'
    svg = (f'<svg viewBox="0 0 400 380" class="tb-cy" role="img" aria-label="Culture leads to Trust, Trust to Value, Value back to Culture">'
           '<defs><marker id="cyHead" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M1,1 L8,5 L1,9" class="cy-ah"/></marker></defs>'
           f'{arcs}{nodes}<text x="200" y="186" text-anchor="middle" class="cy-mid">one loop</text><text x="200" y="204" text-anchor="middle" class="cy-mid2">each feeds the next</text></svg>')
    rows = [("Culture", "Systems and institutions keep researchers and business apart. Changing the system is where it starts."),
            ("Trust", "Once the two worlds begin to collaborate, trust builds between them."),
            ("Value", "Trust turns relationships into value for both sides and for society, which in turn feeds a new culture.")]
    items = "".join(f'<div class="cy-i"><i>{n + 1}</i><div><b>{h}</b><span>{t}</span></div></div>' for n, (h, t) in enumerate(rows))
    md(f'<section class="tb-cycle"><div class="cy-l"><div class="tb-label">Why Trustpont</div><h2>Three problems, one loop</h2>{items}</div><div class="cy-r">{svg}</div></section>')
