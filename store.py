# Every "would be a database later" read and write lives here.
# State is seeded from data/*.json into st.session_state and resets on reload.
import json
from datetime import date, timedelta
from pathlib import Path

import streamlit as st

import model

DATA = Path(__file__).parent / "data"


def today():
    return date.today()


def _offset_to_date(offset):
    return None if offset is None else (today() + timedelta(days=offset)).isoformat()


def _load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def init():
    if "db" in st.session_state:
        return
    matches = _load("matches.json")["matches"]
    for m in matches:
        m["created_at"] = _offset_to_date(m["created_at"])
        m["last_action_at"] = _offset_to_date(m["last_action_at"])
        m["next_action"]["due"] = _offset_to_date(m["next_action"]["due"])
        for entry in m["log"]:
            entry["at"] = _offset_to_date(entry["at"])
    st.session_state.db = {
        "research": {c["id"]: c for c in _load("researcher_cards.json")},
        "business": {c["id"]: c for c in _load("business_cards.json")},
        "matches": {m["id"]: m for m in matches},
        "personas": _load("personas.json"),
        "counter": 100,
    }


def _db():
    return st.session_state.db


def _new_id(prefix):
    _db()["counter"] += 1
    return f"{prefix}{_db()['counter']}"


# --- Personas and cards ---

def persona(role):
    return _db()["personas"][role]


def all_cards(role):
    return list(_db()[role].values())


def published_cards(role):
    return [c for c in all_cards(role) if c["status"] == "published"]


def get_card(role, card_id):
    return _db()[role].get(card_id)


def card_owner_name(role, card):
    return card["owner"]["name"] if role == "research" else card["identity"]["name"]


def my_cards(role):
    name = persona(role)["name"]
    return [c for c in all_cards(role) if card_owner_name(role, c) == name]


def save_card(role, card):
    if not card.get("id"):
        card["id"] = _new_id("r" if role == "research" else "b")
    _db()[role][card["id"]] = card
    return card["id"]


def delete_card(role, card_id):
    _db()[role].pop(card_id, None)
    key = "researcher_card_id" if role == "research" else "business_card_id"
    for m in list(_db()["matches"].values()):
        if m[key] == card_id:
            _db()["matches"].pop(m["id"])


# --- Matches ---

def all_matches():
    return list(_db()["matches"].values())


def get_match(match_id):
    return _db()["matches"].get(match_id)


def my_matches(role):
    key = "researcher_card_id" if role == "research" else "business_card_id"
    ids = {c["id"] for c in my_cards(role)}
    return [m for m in all_matches() if m[key] in ids]


def find_match(researcher_card_id, business_card_id):
    for m in all_matches():
        if m["researcher_card_id"] == researcher_card_id and m["business_card_id"] == business_card_id:
            return m
    return None


def create_match(researcher_card_id, business_card_id, initiated_by, author, note=""):
    existing = find_match(researcher_card_id, business_card_id)
    if existing and existing["status"] != model.DECLINED:
        return existing
    m = model.new_match(researcher_card_id, business_card_id, initiated_by, today().isoformat())
    m["id"] = _new_id("m")
    m["next_action"]["due"] = (today() + timedelta(days=7)).isoformat()
    if note:
        m["log"].append({"at": today().isoformat(), "who": author, "text": note})
    _db()["matches"][m["id"]] = m
    return m


def update_match(match_id, **fields):
    m = _db()["matches"][match_id]
    m.update(fields)
    m["last_action_at"] = today().isoformat()
    return m


def add_log(match_id, who, text):
    m = _db()["matches"][match_id]
    m["log"].append({"at": today().isoformat(), "who": who, "text": text})
    m["last_action_at"] = today().isoformat()
