# Card generation from an abstract. Calls Claude when a key is available,
# otherwise falls back to a pre-written stub so the demo never blocks.
# The API key is never printed, logged, displayed or put in a URL.
import json
import os
import time

import streamlit as st

import model

MODEL = "claude-opus-5-5"
KEY_PLACEHOLDER = "sk-ant-your-key-here"
SESSION_KEY = "anthropic_api_key_input"

DEMO_ABSTRACT = (
    "We report a graphene-oxide membrane with sub-nanometre channels stabilised by "
    "cross-linking with bio-based diamines. In forward osmosis tests on synthetic "
    "brackish water, the membrane rejected 97.8% of NaCl while delivering a water flux "
    "2.3 times higher than commercial polyamide membranes, at 40% lower specific energy "
    "consumption. Membranes of 25 cm2 remained stable over 300 hours of continuous "
    "operation. Fouling behaviour in real feed water and scale-up of the casting "
    "process remain to be investigated."
)


def key_source():
    try:
        if st.secrets.get("ANTHROPIC_API_KEY", KEY_PLACEHOLDER) != KEY_PLACEHOLDER:
            return "secrets"
    except Exception:  # no secrets.toml at all
        pass
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "environment"
    if st.session_state.get(SESSION_KEY):
        return "session"
    return None


def _api_key():
    source = key_source()
    if source == "secrets":
        return st.secrets["ANTHROPIC_API_KEY"]
    if source == "environment":
        return os.environ["ANTHROPIC_API_KEY"]
    if source == "session":
        return st.session_state[SESSION_KEY]
    return None


def render_key_input():
    source = key_source()
    if source in ("secrets", "environment"):
        st.caption(f"Claude API key loaded from {source}.")
        return
    st.text_input("Anthropic API key (optional)", type="password", key=SESSION_KEY,
                  help="Kept in this browser session only, never saved. Without a key, "
                       "card generation runs in demo mode.")


PROMPT = """You turn a researcher's abstract into a Trustpont card that business people
(industry, investors, business developers) can read. Write plainly: no equations, no acronyms,
no jargon. Be honest about limits. Output ONLY a JSON object with exactly these keys:

"title": short, jargon-free (max 12 words)
"key_problem": the problem this research addresses in its field (2 sentences)
"plain_explanation": 3 to 5 sentences a non-specialist understands
"concrete_examples": list of 2 or 3 short strings, what it could do in practice
"case_studies": where something similar already worked (2 sentences, say if unsure)
"feasibility": one honest paragraph on what works and what is still open
"market_problem": the problem addressed within a market (2 sentences)
"draft_business_plan": 2 sentences
"go_to_market": 2 sentences
"rd_costs_to_date": integer euros, a rough estimate
"capital_needed": integer euros, a rough estimate
"support_needed": list, values from {support}
"engagement_wanted": list, values from {engagement}
"ip_status": one of {ip}
"equity_expected": one of {equity}

Sectors chosen by the researcher: {sectors}
Maturity level: {maturity} ({maturity_label})

Abstract:
{text}"""


def _clean(raw, sectors, maturity):
    def pick(value, allowed, default):
        return value if value in allowed else default

    def pick_list(values, allowed):
        return [v for v in (values or []) if v in allowed]

    def to_int(value):
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return 0

    return {
        "title": str(raw.get("title", "")).strip(),
        "key_problem": str(raw.get("key_problem", "")).strip(),
        "plain_explanation": str(raw.get("plain_explanation", "")).strip(),
        "concrete_examples": [str(x) for x in raw.get("concrete_examples", [])][:3],
        "case_studies": str(raw.get("case_studies", "")).strip(),
        "feasibility": str(raw.get("feasibility", "")).strip(),
        "market_problem": str(raw.get("market_problem", "")).strip(),
        "draft_business_plan": str(raw.get("draft_business_plan", "")).strip(),
        "go_to_market": str(raw.get("go_to_market", "")).strip(),
        "rd_costs_to_date": to_int(raw.get("rd_costs_to_date")),
        "capital_needed": to_int(raw.get("capital_needed")),
        "support_needed": pick_list(raw.get("support_needed"), model.SUPPORT_NEEDED),
        "engagement_wanted": pick_list(raw.get("engagement_wanted"), model.ENGAGEMENT_TYPES),
        "ip_status": pick(raw.get("ip_status"), model.IP_STATUS, "no protection yet"),
        "equity_expected": pick(raw.get("equity_expected"), model.EQUITY_RESEARCH, "negotiable"),
        "sectors": sectors,
        "maturity_level": maturity,
    }


def _call_claude(key, text, sectors, maturity):
    import anthropic  # imported lazily so the app runs even without the package

    client = anthropic.Anthropic(api_key=key)
    prompt = PROMPT.format(
        support=model.SUPPORT_NEEDED, engagement=model.ENGAGEMENT_TYPES,
        ip=model.IP_STATUS, equity=model.EQUITY_RESEARCH,
        sectors=", ".join(sectors) or "not specified",
        maturity=maturity, maturity_label=model.MATURITY[maturity], text=text,
    )
    # Fallbacks re-run the request on another model if this one declines it
    response = client.beta.messages.create(
        model=MODEL, max_tokens=16000,
        output_config={"effort": "low"},
        betas=["server-side-fallback-2026-07-01"], fallbacks="default",
        messages=[{"role": "user", "content": prompt}],
    )
    if response.stop_reason == "refusal":
        raise ValueError("the model declined this abstract")
    body = "".join(b.text for b in response.content if b.type == "text")
    return json.loads(body[body.index("{"): body.rindex("}") + 1])


def _error_message(exc):
    # Fixed messages only: never echo exception text that could carry request details
    name = type(exc).__name__
    if name == "AuthenticationError":
        return "the API key was rejected"
    if name == "RateLimitError":
        return "the API rate limit was reached"
    if name in ("APIConnectionError", "APITimeoutError"):
        return "the API could not be reached"
    if name == "ModuleNotFoundError":
        return "the anthropic package is not installed"
    if isinstance(exc, ValueError):
        return "the answer could not be read as a card"
    return "the API returned an error"


def generate_card_from_abstract(text, sectors, maturity):
    """Returns the Part 1 and Part 2 fields, plus "_mode" ("ai" or "demo") and "_notice"."""
    key = _api_key()
    if key:
        try:
            card = _clean(_call_claude(key, text, sectors, maturity), sectors, maturity)
            return {**card, "_mode": "ai", "_notice": ""}
        except Exception as exc:
            notice = f"Claude could not generate the card ({_error_message(exc)}), so it was generated in demo mode."
    else:
        notice = "No API key configured: this card was generated in demo mode."
    time.sleep(2)
    return {**_stub(text, sectors, maturity), "_mode": "demo", "_notice": notice}


def _stub(text, sectors, maturity):
    if "membrane" in text.lower() or "desalination" in text.lower():
        card = {
            "title": "A membrane that makes drinking water from salty water with less energy",
            "key_problem": "Turning brackish or sea water into drinking water uses a lot of energy, "
                           "mostly to push water through membranes. Energy is now the largest cost of desalination plants.",
            "plain_explanation": "We made an ultra-thin filter from a carbon material with tiny channels "
                                 "that let water through but block salt. Water passes more than twice as "
                                 "fast as through today's filters, so the same plant needs less pressure "
                                 "and less electricity. In the lab, the filter kept working for 300 hours "
                                 "without losing performance.",
            "concrete_examples": [
                "Cut the electricity bill of brackish-water treatment plants in southern Europe",
                "Small solar-powered units for islands and remote sites",
                "Treat salty industrial process water so it can be reused",
            ],
            "case_studies": "Filters of this type replaced older technologies in water treatment during the "
                            "1990s once their energy savings were proven. Several research groups have shown "
                            "similar carbon membranes, but few have tested stability over hundreds of hours.",
            "feasibility": "The filter works on small lab samples with synthetic water. Two things are not "
                           "proven yet: how it behaves with real, dirty feed water, and whether it can be "
                           "produced in large sheets at a reasonable cost. Both need a partner with a pilot "
                           "site and manufacturing know-how.",
            "market_problem": "Water utilities and industrial sites in water-stressed regions need more fresh "
                              "water but face rising energy costs. Membrane suppliers compete on energy efficiency.",
            "draft_business_plan": "License the membrane recipe to an established membrane manufacturer, with "
                                   "a joint development phase to adapt it to their production lines.",
            "go_to_market": "Run a six-month pilot on real brackish water with one utility, then use the data "
                            "to negotiate a licence with a membrane producer.",
            "rd_costs_to_date": 260000,
            "capital_needed": 900000,
            "support_needed": ["industrial site", "engineering", "data"],
            "engagement_wanted": ["pilot", "research contract", "licence"],
            "ip_status": "no protection yet",
            "equity_expected": "negotiable",
        }
    else:
        first = text.strip().split(".")[0][:90] or "Untitled research"
        card = {
            "title": first,
            "key_problem": "Describe here, in two sentences, the problem this research solves in its field.",
            "plain_explanation": text.strip()[:600],
            "concrete_examples": ["A first concrete application", "A second concrete application"],
            "case_studies": "Where has something similar already worked?",
            "feasibility": "What already works, and what still needs to be proven?",
            "market_problem": "Which market has this problem, and what does it cost them today?",
            "draft_business_plan": "Licence, spin-off or research contract?",
            "go_to_market": "Who would be the first partner or customer?",
            "rd_costs_to_date": 0,
            "capital_needed": 0,
            "support_needed": [],
            "engagement_wanted": ["research contract"],
            "ip_status": "no protection yet",
            "equity_expected": "negotiable",
        }
    return _clean(card, sectors, maturity)
