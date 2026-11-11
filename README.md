# TrustBridge

Research-to-business matchmaking prototype built during the ENGAGE.EU Expedition+ week.
PhD students and researchers publish a **card** written for business readers; companies,
business developers, ex-founders, VCs and incubators publish a card describing what they
scout for. All matching runs on these cards.

Front-end prototype only: no database, no authentication. State lives in the Streamlit
session and resets on reload.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## API key (optional)

The app works without a key (card generation runs in demo mode).
