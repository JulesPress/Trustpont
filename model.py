# Data model: fixed vocabularies and empty-card factories. Plain dicts only.

SECTORS = [
    "Energy", "Health & biotech", "Agri-food", "Mobility & transport",
    "Advanced materials", "Software & AI", "Semiconductors & electronics",
    "Environment & water", "Construction", "Finance & insurance",
    "Space & defence", "Manufacturing & robotics",
]

# Broad families, used by the matching for a partial sector match
SECTOR_FAMILY = {
    "Energy": "infrastructure", "Mobility & transport": "infrastructure", "Construction": "infrastructure",
    "Health & biotech": "life", "Agri-food": "life", "Environment & water": "life",
    "Advanced materials": "deeptech", "Semiconductors & electronics": "deeptech",
    "Space & defence": "deeptech", "Manufacturing & robotics": "deeptech",
    "Software & AI": "digital", "Finance & insurance": "digital",
}

MATURITY = {
    1: "Concept validated on paper",
    2: "Proof of concept in lab",
    3: "Working prototype",
    4: "Tested in real conditions (pilot)",
    5: "Ready to industrialise",
}

STATUSES = ["not contacted", "contacted", "meeting scheduled", "active collaboration", "closed"]
DECLINED = "declined"
ALL_STATUSES = STATUSES + [DECLINED]
# A match counts as mutually accepted once it has left "not contacted"
ACCEPTED_STATUSES = ["contacted", "meeting scheduled", "active collaboration", "closed"]
# Rough weekly hours a match costs a researcher, used by the time guard
STATUS_HOURS = {"contacted": 1, "meeting scheduled": 2, "active collaboration": 5}

SUPPORT_NEEDED = ["capital", "engineering", "market access", "data", "industrial site",
                  "legal/IP help", "full co-founding team"]
WHAT_THEY_BRING = ["capital", "data", "site/lab access", "engineering", "market knowledge",
                   "network", "legal/IP support"]
# Which business contribution covers which researcher need
NEED_COVERED_BY = {
    "capital": {"capital"}, "engineering": {"engineering"},
    "market access": {"market knowledge", "network"}, "data": {"data"},
    "industrial site": {"site/lab access"}, "legal/IP help": {"legal/IP support"},
    "full co-founding team": {"network"},
}
ENGAGEMENT_TYPES = ["pilot", "research contract", "licence", "invest", "hire", "mentor", "co-found"]

IP_STATUS = ["no protection yet", "patent pending", "patent granted", "trade secret", "open publication"]
IP_EXPECTATION = ["licence ok", "sector exclusivity", "full ownership", "flexible"]
# Researcher IP situations each business expectation can work with
IP_COMPATIBLE = {
    "licence ok": {"no protection yet", "patent pending", "patent granted", "trade secret"},
    "sector exclusivity": {"patent pending", "patent granted"},
    "full ownership": {"no protection yet"},
    "flexible": set(IP_STATUS),
}

EQUITY_RESEARCH = ["none", "up to 10%", "10-25%", "25-50%", "negotiable"]
EQUITY_BUSINESS = ["none", "up to 10%", "10-25%", "25-50%", "flexible"]
EQUITY_ORDER = ["none", "up to 10%", "10-25%", "25-50%"]

COUNTRIES = ["Austria", "Belgium", "Bulgaria", "Denmark", "Finland", "France", "Germany",
             "Italy", "Netherlands", "Norway", "Poland", "Portugal", "Slovenia", "Spain",
             "Sweden", "Switzerland"]
EUROPE_WIDE = "Europe-wide"

VISIBILITY = ["public", "anonymous", "private"]
CARD_STATUS = ["draft", "published", "paused"]
TTO_STATUS = ["not requested", "pending", "approved"]

CRITERIA = ["sector", "maturity", "equity_ip", "geography", "engagement", "resources"]
CRITERIA_LABELS = {
    "sector": "Sector", "maturity": "Maturity", "equity_ip": "Equity & IP expectation",
    "geography": "Geography", "engagement": "Engagement type",
    "resources": "Resources (brought vs needed)",
}
WEIGHT_LEVELS = {"Must have": 5, "Important": 3, "Nice to have": 1}
DEFAULT_WEIGHTS = {c: "Important" for c in CRITERIA}

PROFILE_TYPES = ["industry", "business developer", "ex-founder", "VC", "incubator"]
PROFILE_LABELS = {
    "industry": "Industry (company)", "business developer": "Business developer",
    "ex-founder": "Ex-founder", "VC": "Venture capital", "incubator": "Incubator / Accelerator",
}

# Extra fields per business profile type: key -> (label, kind, options)
PROFILE_FIELDS = {
    "industry": {
        "company_size": ("Company size", "select", ["1-50", "50-250", "250-1000", "1000+"]),
        "has_rd_department": ("In-house R&D department", "bool", None),
        "pilot_sites": ("Sites available for pilots", "text", None),
    },
    "business developer": {
        "years_experience": ("Years of business development", "int", None),
        "past_deals": ("Tech-transfer deals closed", "int", None),
        "compensation": ("Compensation model", "select", ["success fee", "retainer", "equity", "mixed"]),
    },
    "ex-founder": {
        "companies_founded": ("Companies founded", "int", None),
        "outcome": ("Best outcome so far", "select", ["acquired", "IPO", "still running", "closed"]),
        "role_sought": ("Role sought", "select", ["advisor", "CEO co-founder", "board member"]),
    },
    "VC": {
        "fund_size_eur": ("Fund size (EUR)", "int", None),
        "stage": ("Investment stage", "select", ["pre-seed", "seed", "Series A"]),
        "ticket_eur": ("Typical ticket (EUR)", "int", None),
        "lead": ("Leads rounds", "bool", None),
    },
    "incubator": {
        "programme_format": ("Programme format", "select", ["in person", "hybrid", "remote"]),
        "duration_months": ("Duration (months)", "int", None),
        "takes_equity": ("Takes equity", "bool", None),
        "cohort_size": ("Startups per cohort", "int", None),
    },
}


def new_researcher_card(owner):
    return {
        "id": None,
        "owner": dict(owner),
        # Part 1, plain language
        "title": "", "key_problem": "", "plain_explanation": "",
        "concrete_examples": [], "case_studies": "", "feasibility": "",
        # Part 2, business
        "market_problem": "", "draft_business_plan": "", "go_to_market": "",
        "rd_costs_to_date": 0, "capital_needed": 0, "maturity_level": 1,
        "support_needed": [], "engagement_wanted": [],
        "ip_status": "no protection yet", "equity_expected": "negotiable",
        "sectors": [],
        "geography": {"country": owner.get("country", "Italy"), "remote": True, "relocate": False},
        # Meta
        "status": "draft", "visibility": "public",
        "tto_required": False, "tto_status": "not requested",
        "hours_per_week_available": 6,
        "criteria_weights": dict(DEFAULT_WEIGHTS),
        "revoked": [],
    }


def new_business_card(identity, profile_type="industry"):
    return {
        "id": None,
        "identity": dict(identity),
        "profile_type": profile_type,
        "sectors": [], "looking_for": "",
        "engagement_type": [], "maturity_accepted": [2, 4],
        "what_they_bring": [], "ip_expectation": "flexible", "equity_expected": "flexible",
        "geography_accepted": [EUROPE_WIDE],
        "timeline": {"start": "", "signatory": "", "budget": ""},
        "time_commitment": 8,
        "criteria_weights": dict(DEFAULT_WEIGHTS),
        "extra": {},
        "status": "published",
    }


def new_match(researcher_card_id, business_card_id, initiated_by, created_at):
    # initiated_by is "research" or "business"; "received"/"sent" depend on who is looking
    return {
        "id": None,
        "researcher_card_id": researcher_card_id,
        "business_card_id": business_card_id,
        "initiated_by": initiated_by,
        "status": "not contacted",
        "created_at": created_at, "last_action_at": created_at,
        "next_action": {"text": "Answer the match request", "due": None},
        "decline_reason": None,
        "log": [],
    }
