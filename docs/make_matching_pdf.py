import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (KeepTogether, Paragraph, Preformatted, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

OUT = sys.argv[1]
TEAL = colors.HexColor("#14564F")
INK = colors.HexColor("#16181A")
MUTED = colors.HexColor("#6B7280")
LINE = colors.HexColor("#E4E1DA")
TINT = colors.HexColor("#EDF2F1")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Title"], fontName="Times-Bold", fontSize=21, leading=25,
                    textColor=INK, alignment=TA_LEFT, spaceAfter=2)
SUB = ParagraphStyle("SUB", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, textColor=MUTED, spaceAfter=10)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontName="Times-Bold", fontSize=13.5, leading=17,
                    textColor=TEAL, spaceBefore=10, spaceAfter=4)
P = ParagraphStyle("P", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=INK, spaceAfter=5)
CELL = ParagraphStyle("CELL", parent=P, fontSize=8.5, leading=11, spaceAfter=0)
CELLB = ParagraphStyle("CELLB", parent=CELL, fontName="Helvetica-Bold")
CODE = ParagraphStyle("CODE", parent=ss["Code"], fontName="Courier", fontSize=8.3, leading=10.5,
                      textColor=INK, backColor=TINT, borderPadding=6, leftIndent=6, rightIndent=6,
                      spaceBefore=3, spaceAfter=8)


def table(rows, widths, header=True):
    data = [[Paragraph(str(c), CELLB if (header and i == 0) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.5, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if header:
        style.append(("BACKGROUND", (0, 0), (-1, 0), TINT))
    t.setStyle(TableStyle(style))
    return t


def c(text):
    return f'<font name="Courier">{text}</font>'


s = []
s.append(Paragraph("TrustBridge matching: method and code", H1))
s.append(Paragraph("Hand-over note for the teammate taking over the matching algorithm. "
                   "Branch <b>augustin/prototype</b>, file <b>matching.py</b> (about 120 lines).", SUB))

s.append(Paragraph("1. What it does", H2))
s.append(Paragraph(
    "The matching compares one <b>researcher card</b> with one <b>business card</b> and returns a score "
    "out of 100, plus short sentences explaining why. It is deterministic and explainable on purpose: "
    "no machine learning, every number can be traced back to a field on the two cards. The first version "
    "was written fast and deliberately kept simple, so expect to tune it.", P))
s.append(Paragraph(
    "Scores are <b>never stored</b>. The seed files in " + c("data/") + " contain no score; the UI calls "
    + c("score_pair()") + " every time a score is displayed, so the number always matches the current "
    "cards, including after an edit during the demo. Changing the algorithm therefore changes every "
    "screen at once, with no data migration.", P))

s.append(Paragraph("2. The six criteria", H2))
s.append(Paragraph(
    "Each criterion returns a sub-score of <b>1</b> (clear match), <b>0.5</b> (partial) or <b>0</b> (no match), "
    "together with a sentence that quotes the real values. Equity &amp; IP is the average of two halves, "
    "so it can also be 0.25 or 0.75. The vocabularies and lookup tables live in " + c("model.py") + ".", P))
W = 170 * mm
s.append(table([
    ["Criterion", "Function", "1", "0.5", "0"],
    ["Sector", c("_sector"), "At least one sector shared",
     "Different sectors but same broad family (" + c("SECTOR_FAMILY") + ": infrastructure, life, deeptech, digital)", "Otherwise"],
    ["Maturity", c("_maturity"), "Researcher level inside the business range (e.g. 3 in 2-4)", "One level outside", "Two levels outside"],
    ["Equity &amp; IP", c("_equity_ip"),
     "Equity: same bracket or either side flexible/negotiable. IP: researcher IP status is in " + c("IP_COMPATIBLE") + "[business expectation]",
     "Equity: adjacent brackets", "Equity: further apart. IP: incompatible. Final = (equity + IP) / 2"],
    ["Geography", c("_geography"), "Business accepts Europe-wide or the researcher's country",
     "Outside, but researcher open to remote work or relocation", "Otherwise"],
    ["Engagement", c("_engagement"), "2+ shared types, or every type the researcher wants",
     "Exactly one shared type", "None shared"],
    ["Resources", c("_resources"), "Every need covered by what the business brings (" + c("NEED_COVERED_BY") + ")",
     "Some needs covered", "None covered"],
], [24 * mm, 27 * mm, 42 * mm, 41 * mm, 36 * mm]))
s.append(Spacer(1, 4))
s.append(Paragraph(
    "Note: the researcher card has an " + c("engagement_wanted") + " field that the original brief did not "
    "list. It was added so that the engagement criterion exists on both sides. A full co-founding team need "
    "is considered covered when the business offers the " + c("co-found") + " engagement.", P))

s.append(Paragraph("3. From sub-scores to the displayed numbers", H2))
s.append(Paragraph(
    "On their card, each user sets every criterion to <b>Must have</b> (weight 5), <b>Important</b> (3) or "
    "<b>Nice to have</b> (1), stored as text in " + c("criteria_weights") + " and converted by " + c("weights()") + ".", P))
s.append(Preformatted(
    "one_sided = 100 * sum(weight[c] * sub[c]) / sum(weight[c])   # once per side\n"
    "mutual    = (research_score + business_score) / 2             # shown in the lists", CODE))
s.append(Paragraph(
    "Both one-sided scores are shown in the match detail: a 90/40 pair is a very different conversation "
    "from a 65/65 one. <b>Hard filter:</b> if the maturity gap is above 2 levels, " + c("score_pair()") +
    " returns <b>None</b> and the UI does not show the pair at all.", P))
s.append(Paragraph(
    "<b>Reasons</b> are the three criteria contributing the most, ranked by "
    "(researcher weight + business weight) / 2 x sub-score, ignoring criteria that scored 0. "
    "<b>Watch out</b> is the criterion with the lowest sub-score (ties go to the higher combined weight); "
    "it is None when every criterion scored 1.", P))

s.append(KeepTogether([
    Paragraph("4. Worked example (seed data)", H2),
    Paragraph("Elena's self-healing concrete coating (" + c("r1") + ") against Aurora Deep Tech Fund (" + c("b8") + ").", P),
    table([
        ["Criterion", "Sub-score", "Elena's weight", "Aurora's weight"],
        ["Sector", "1", "Must have (5)", "Must have (5)"],
        ["Maturity", "1", "Important (3)", "Important (3)"],
        ["Equity &amp; IP", "1", "Important (3)", "Must have (5)"],
        ["Geography", "1", "Nice to have (1)", "Nice to have (1)"],
        ["Engagement", "0", "Important (3)", "Important (3)"],
        ["Resources", "0.5", "Must have (5)", "Nice to have (1)"],
        ["Result", "", "14.5 / 20 = <b>72</b>", "14.5 / 18 = <b>81</b>"],
    ], [40 * mm, 30 * mm, 50 * mm, 50 * mm]),
    Spacer(1, 4),
    Paragraph("Mutual = (72 + 81) / 2 = <b>76</b>. Watch out: \"No common engagement type\" (the fund only "
              "invests, Elena wants a pilot, licence or research contract).", P),
]))
s.append(Paragraph(
    "Rounding detail: Python's " + c("round()") + " rounds halves to the even number, so 72.5 becomes 72 and "
    "76.5 becomes 76. Harmless, but worth knowing if you compare with a spreadsheet.", P))

s.append(Paragraph("5. Code map", H2))
s.append(table([
    ["Function", "Role"],
    [c("score_pair(rc, bc)"), "Only public entry point. Returns None (filtered) or a dict: mutual, research, business, subs, reasons, watch_out."],
    [c("CHECKS"), "Dict criterion -> function. Each function takes (rc, bc) and returns (sub_score, sentence)."],
    [c("weights(card)"), "Converts the card's Must have / Important / Nice to have labels into 5 / 3 / 1."],
    [c("one_sided(subs, w)"), "Weighted average out of 100."],
    [c("maturity_gap(rc, bc)"), "Distance between the researcher level and the accepted range; also used by the hard filter."],
], [45 * mm, 125 * mm]))

s.append(Paragraph("6. How to change it safely", H2))
for line in [
    "<b>Tune a rule:</b> edit one " + c("_criterion") + " function. Keep the (score, sentence) return shape; the UI relies on it.",
    "<b>Add a criterion:</b> add it to " + c("model.CRITERIA") + " and " + c("CRITERIA_LABELS") + ", write the function, register it in "
    + c("CHECKS") + ", and add a default weight to the seed cards. The card forms build their weight selectors from " + c("CRITERIA") + ".",
    "<b>Finer scores:</b> nothing forces 0 / 0.5 / 1; any value between 0 and 1 works (e.g. share of needs covered).",
    "<b>Check the seed matches:</b> run the snippet below after any change and make sure the demo pairs still look sensible.",
]:
    s.append(Paragraph("&bull; " + line, P))
s.append(Preformatted(
    "python3 -c \"\n"
    "import json, matching\n"
    "r = {c['id']: c for c in json.load(open('data/researcher_cards.json'))}\n"
    "b = {c['id']: c for c in json.load(open('data/business_cards.json'))}\n"
    "for m in json.load(open('data/matches.json'))['matches']:\n"
    "    s = matching.score_pair(r[m['researcher_card_id']], b[m['business_card_id']])\n"
    "    print(m['id'], s and (s['mutual'], s['research'], s['business']))\"", CODE))

limits = [Paragraph("7. Known limits and ideas", H2)]
for line in [
    "Sub-scores are coarse, so several pairs reach 100. Graded scores would spread the ranking.",
    "Sector families are a hand-made grouping of the 12 sectors; a small similarity matrix would be more precise.",
    "Equity semantics differ by side (what the researcher would give vs what the business expects to take); worth confirming with the team.",
    "Free text (" + c("looking_for") + ", the abstract) is ignored. Text similarity could be added later as a seventh, clearly labelled criterion, keeping the explanation readable.",
]:
    limits.append(Paragraph("&bull; " + line, P))
s.append(KeepTogether(limits))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 12 * mm, "TrustBridge - ENGAGE.EU Expedition+ - matching hand-over")
    canvas.drawRightString(190 * mm, 12 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                        topMargin=18 * mm, bottomMargin=20 * mm,
                        title="TrustBridge matching: method and code", author="TrustBridge team")
doc.build(s, onFirstPage=footer, onLaterPages=footer)
