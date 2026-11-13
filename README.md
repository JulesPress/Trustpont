# Trustpont

Research-to-business matchmaking prototype built during the ENGAGE.EU Expedition+ week.
PhD students and researchers publish a **card** written for business readers; companies,
business developers, ex-founders, VCs and incubators publish a card describing what they
scout for. All matching runs on these cards.

Front-end prototype only: no database, no authentication. State is seeded from `data/*.json`
into the Streamlit session; changes made during a demo persist for the session and reset on reload.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Python 3.10 or later. The app is fully usable without an API key.

## API key (optional, each teammate uses their own)

1. Local file: copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and put your key in it (git-ignored).
2. Or environment variable: `export ANTHROPIC_API_KEY=sk-ant-...` before `streamlit run app.py`.
3. Or paste it in the sidebar field: kept in your browser session only, never written to disk.
4. First hit wins, in that order. Never commit a key: `secrets.toml`, `.env` and `*.key` are git-ignored.
5. Without a key, or if the call fails, card generation runs in demo mode with a pre-written card.

## Demo path (about 3 minutes, no typing)

Landing page → *I am a researcher* → dashboard (decisions, time guard) → *My cards* → *Create a new card* →
*Generate the card* (the abstract is pre-filled) → *Continue* → *Publish* → *Browse business* →
*Send a match request* → switch the sidebar to *I am business* → the request is waiting on Lukas's dashboard.

## Files

| File | Role |
|---|---|
| `app.py` | Page setup, role-dependent navigation, sidebar |
| `model.py` | Vocabularies (sectors, maturity scale, statuses), empty-card factories |
| `store.py` | Every read and write of data. The only file to change for a real database |
| `matching.py` | Deterministic scoring, reasons and watch-out line |
| `knowledge_graph.py` | In-memory graph projection for browsing and explaining a match |
| `ai.py` | Card generation with Claude, key resolution, demo-mode stub |
| `style.py` | The single CSS block |
| `ui.py` | Shared rendering: cards, badges, match tables, time guard |
| `views/` | One file per page, shared by both roles |
| `data/` | Seed cards, matches and the two demo personas |
| `docs/matching_method.pdf` | Hand-over note on the matching algorithm |

## Judgement calls

- **Researcher cards have an `engagement_wanted` field** (pilot, licence, invest...). The brief listed
  engagement type only on business cards, but the engagement criterion needs both sides.
- **Matches store `initiated_by`, not `received`/`sent`.** The same match is "received" for one side
  and "sent" for the other, so the direction is derived from who is looking.
- **"Not contacted" means a request is waiting for an answer.** Accepting moves it to "contacted",
  which is also when an anonymous researcher's identity is revealed.
- **The time guard estimates hours from match statuses** (1 h a week per contact, 2 h with a meeting
  scheduled, 5 h for an active collaboration) against the weekly hours set on the researcher's cards.
- **Pipeline arrows only apply after acceptance.** New requests are answered from the match detail,
  so accepting always goes through the time guard and the decline reason is always recorded.
- **Seed dates are day offsets** converted at load, so "overdue" and "in 2 days" stay true whatever
  the demo date. Scores are never stored and are recomputed from the cards on every screen.
- **The knowledge graph is a temporary projection** of the selected, visible browse match. It adds
  no database or persistence layer; scores still come from `matching.py`.
- **Messages are a local log on the match**, with no backend and no email, as the brief excludes chat.
- **The business side has no consent page.** Business cards carry no confidential research, so the
  trust page is researcher-only.
