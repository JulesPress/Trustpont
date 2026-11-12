"""In-memory knowledge-graph projection for an evaluated card pair."""
import json

import model


def build_match_graph(rc, bc, score, researcher_label, business_label):
    """Project two cards and their score into serializable nodes and edges."""
    researcher_id = f"researcher:{rc['id']}"
    business_id = f"business:{bc['id']}"
    assessment_id = f"assessment:{rc['id']}:{bc['id']}"
    nodes = [
        {"id": researcher_id, "kind": "card", "label": researcher_label},
        {"id": business_id, "kind": "card", "label": business_label},
        {
            "id": assessment_id,
            "kind": "assessment",
            "label": f"Match reciproco: {score['mutual']}/100",
        },
    ]
    edges = [
        {"source": assessment_id, "target": researcher_id, "label": "ricercatore"},
        {"source": assessment_id, "target": business_id, "label": "impresa"},
    ]

    families = {}
    for card_id, card, relation in (
        (researcher_id, rc, "lavora in"),
        (business_id, bc, "cerca in"),
    ):
        for sector in card["sectors"]:
            sector_id = f"sector:{sector}"
            if not any(node["id"] == sector_id for node in nodes):
                nodes.append({"id": sector_id, "kind": "sector", "label": sector})
            edges.append({"source": card_id, "target": sector_id, "label": relation})

            family = model.SECTOR_FAMILY[sector]
            family_id = f"family:{family}"
            if family not in families:
                nodes.append({"id": family_id, "kind": "family", "label": family})
                edges.append({"source": sector_id, "target": family_id, "label": "famiglia"})
                families[family] = family_id

    for criterion in model.CRITERIA:
        sub_score, explanation = score["subs"][criterion]
        evaluation_id = f"evaluation:{rc['id']}:{bc['id']}:{criterion}"
        nodes.append({
            "id": evaluation_id,
            "kind": "evaluation",
            "label": (
                f"{model.CRITERIA_LABELS[criterion]}: {sub_score:g}/1\n"
                f"Ricercatore: {rc['criteria_weights'].get(criterion, 'Important')}\n"
                f"Impresa: {bc['criteria_weights'].get(criterion, 'Important')}\n"
                f"{explanation}"
            ),
        })
        edges.append({
            "source": assessment_id,
            "target": evaluation_id,
            "label": "valutazione",
        })

    return {"nodes": nodes, "edges": edges}


def to_dot(graph):
    """Render the graph projection as Graphviz DOT for Streamlit."""
    styles = {
        "card": 'shape=box, style="rounded,filled", fillcolor="#EAF3F1"',
        "assessment": 'shape=ellipse, style=filled, fillcolor="#D2E5E1"',
        "sector": 'shape=box, style="rounded,filled", fillcolor="#F5F1E8"',
        "family": 'shape=box, style="rounded,dashed", fillcolor="#FBFAF7"',
        "evaluation": 'shape=note, style=filled, fillcolor="#FFFFFF"',
    }

    def quote(value):
        return json.dumps(str(value), ensure_ascii=False)

    lines = [
        "digraph TrustBridge {",
        '  graph [rankdir=LR, bgcolor="transparent", nodesep=0.45, ranksep=0.7];',
        '  node [fontname="Arial", fontsize=10, margin="0.14,0.10"];',
        '  edge [fontname="Arial", fontsize=8, color="#7B827F", arrowsize=0.7];',
    ]
    for node in graph["nodes"]:
        style = styles[node["kind"]]
        lines.append(f"  {quote(node['id'])} [label={quote(node['label'])}, {style}];")
    for edge in graph["edges"]:
        lines.append(
            f"  {quote(edge['source'])} -> {quote(edge['target'])} "
            f"[label={quote(edge['label'])}];"
        )
    lines.append("}")
    return "\n".join(lines)
