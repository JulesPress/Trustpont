import unittest

import knowledge_graph


class KnowledgeGraphTests(unittest.TestCase):
    def setUp(self):
        self.researcher = {
            "id": "r1",
            "title": "Battery research",
            "sectors": ["Energy", "Advanced materials"],
            "criteria_weights": {"sector": "Must have"},
        }
        self.business = {
            "id": "b1",
            "sectors": ["Energy"],
            "criteria_weights": {"sector": "Important"},
        }
        self.score = {
            "mutual": 80,
            "subs": {
                criterion: (1.0, "good fit")
                for criterion in (
                    "sector", "maturity", "equity_ip", "geography", "engagement", "resources"
                )
            },
        }

    def test_build_match_graph_links_cards_sectors_and_criterion_scores(self):
        graph = knowledge_graph.build_match_graph(
            self.researcher, self.business, self.score, "Battery research", "Energy company"
        )

        ids = {node["id"] for node in graph["nodes"]}
        self.assertIn("researcher:r1", ids)
        self.assertIn("business:b1", ids)
        self.assertIn("sector:Energy", ids)
        self.assertIn("family:infrastructure", ids)
        self.assertIn("evaluation:r1:b1:sector", ids)
        self.assertEqual(sum(node["id"] == "sector:Energy" for node in graph["nodes"]), 1)
        relations = {
            (edge["source"], edge["target"])
            for edge in graph["edges"]
        }
        self.assertTrue({
            ("assessment:r1:b1", "researcher:r1"),
            ("assessment:r1:b1", "business:b1"),
            ("researcher:r1", "sector:Energy"),
            ("business:b1", "sector:Energy"),
        } <= relations)

    def test_to_dot_escapes_quotes_and_newlines(self):
        dot = knowledge_graph.to_dot({
            "nodes": [{"id": 'card:"1', "kind": "card", "label": 'Title "one"\nline two'}],
            "edges": [],
        })

        self.assertIn('Title \\"one\\"\\nline two', dot)
        self.assertIn('card:\\"1', dot)


if __name__ == "__main__":
    unittest.main()