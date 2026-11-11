# Deterministic, explainable matching between a researcher card and a business card.
import model


def maturity_gap(rc, bc):
    level, (lo, hi) = rc["maturity_level"], bc["maturity_accepted"]
    return max(lo - level, level - hi, 0)


def _join(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def _sector(rc, bc):
    shared = [s for s in rc["sectors"] if s in bc["sectors"]]
    if shared:
        return 1, f"Both work in {_join(shared)}"
    families = {model.SECTOR_FAMILY[s] for s in bc["sectors"]}
    related = [s for s in rc["sectors"] if model.SECTOR_FAMILY[s] in families]
    if related:
        return 0.5, f"Related sectors: {_join(rc['sectors'])} vs {_join(bc['sectors'])}"
    return 0, f"No sector in common ({_join(rc['sectors'])} vs {_join(bc['sectors'])})"


def _maturity(rc, bc):
    gap, level, (lo, hi) = maturity_gap(rc, bc), rc["maturity_level"], bc["maturity_accepted"]
    if gap == 0:
        return 1, f"Maturity {level} fits their accepted range {lo}-{hi}"
    if gap == 1:
        return 0.5, f"Maturity {level} is one level outside their range {lo}-{hi}"
    return 0, f"Maturity {level} is far from their range {lo}-{hi}"


def _equity_ip(rc, bc):
    r_eq, b_eq = rc["equity_expected"], bc["equity_expected"]
    if r_eq == "negotiable" and b_eq == "flexible":
        eq, eq_text = 1, "both flexible on equity"
    elif r_eq == "negotiable" or b_eq == "flexible":
        eq, eq_text = 1, f"equity {r_eq} vs {b_eq}, one side flexible"
    elif r_eq == b_eq:
        eq, eq_text = 1, f"both expect {r_eq} equity"
    elif abs(model.EQUITY_ORDER.index(r_eq) - model.EQUITY_ORDER.index(b_eq)) == 1:
        eq, eq_text = 0.5, f"equity close ({r_eq} vs {b_eq})"
    else:
        eq, eq_text = 0, f"equity apart ({r_eq} vs {b_eq})"
    ip_ok = rc["ip_status"] in model.IP_COMPATIBLE[bc["ip_expectation"]]
    ip_text = f"IP '{rc['ip_status']}' {'suits' if ip_ok else 'does not suit'} '{bc['ip_expectation']}'"
    text = f"{eq_text}; {ip_text}"
    return (eq + ip_ok) / 2, text[0].upper() + text[1:]


def _geography(rc, bc):
    country, accepted = rc["geography"]["country"], bc["geography_accepted"]
    if model.EUROPE_WIDE in accepted or country in accepted:
        return 1, f"Based in {country}, within their area ({_join(accepted)})"
    if rc["geography"]["remote"] or rc["geography"]["relocate"]:
        return 0.5, f"Based in {country}, outside their area but open to remote work or relocation"
    return 0, f"Based in {country}, outside their area ({_join(accepted)})"


def _engagement(rc, bc):
    wanted = rc["engagement_wanted"]
    shared = [e for e in wanted if e in bc["engagement_type"]]
    if shared and (len(shared) >= 2 or len(shared) == len(wanted)):
        return 1, f"Both open to {_join(shared)}"
    if shared:
        return 0.5, f"Partial fit on engagement: {_join(shared)}"
    return 0, f"No common engagement type (wants {_join(wanted or ['nothing'])})"


def _resources(rc, bc):
    needs = rc["support_needed"]
    if not needs:
        return 1, "No specific support needed"
    bring = set(bc["what_they_bring"])
    covered = [n for n in needs if model.NEED_COVERED_BY[n] & bring
               or (n == "full co-founding team" and "co-found" in bc["engagement_type"])]
    missing = [n for n in needs if n not in covered]
    if not missing:
        return 1, f"They bring everything the work needs: {_join(covered)}"
    if covered:
        return 0.5, f"They cover part of the needs ({_join(covered)}), not {_join(missing)}"
    return 0, f"They bring none of the needed support ({_join(needs)})"


CHECKS = {"sector": _sector, "maturity": _maturity, "equity_ip": _equity_ip,
          "geography": _geography, "engagement": _engagement, "resources": _resources}


def weights(card):
    return {c: model.WEIGHT_LEVELS[card["criteria_weights"].get(c, "Important")] for c in model.CRITERIA}


def one_sided(subs, w):
    return round(100 * sum(w[c] * subs[c][0] for c in model.CRITERIA) / sum(w.values()))


def score_pair(rc, bc):
    """None when the pair fails the hard filter (maturity gap above 2)."""
    if maturity_gap(rc, bc) > 2:
        return None
    subs = {c: CHECKS[c](rc, bc) for c in model.CRITERIA}
    rw, bw = weights(rc), weights(bc)
    research, business = one_sided(subs, rw), one_sided(subs, bw)
    # Rank criteria by what they contribute under both sides' weights
    contribution = {c: (rw[c] + bw[c]) / 2 * subs[c][0] for c in model.CRITERIA}
    ranked = sorted((c for c in model.CRITERIA if subs[c][0] > 0), key=lambda c: -contribution[c])
    weakest = min(model.CRITERIA, key=lambda c: (subs[c][0], -(rw[c] + bw[c])))
    return {
        "mutual": round((research + business) / 2),
        "research": research,
        "business": business,
        "subs": subs,
        "reasons": [subs[c][1] for c in ranked[:3]],
        "watch_out": subs[weakest][1] if subs[weakest][0] < 1 else None,
    }
