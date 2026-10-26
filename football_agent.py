"""
Football Fixtures Agent (FREE version - Groq)
---------------------------------------------
Brain: Groq (free API key, no credit card)
Data:  football-data.org (free API key)

Poochein: "aaj ke matches batao", "Champions League ke upcoming matches"
"""

import os
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

FOOTBALL_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
LOCAL_TZ = ZoneInfo(os.getenv("LOCAL_TZ", "Asia/Karachi"))
BASE_URL = "https://api.football-data.org/v4"

COMPETITIONS = {
    "CL": "UEFA Champions League",
    "PL": "Premier League (England)",
    "PD": "La Liga (Spain)",
    "SA": "Serie A (Italy)",
    "BL1": "Bundesliga (Germany)",
    "FL1": "Ligue 1 (France)",
    "DED": "Eredivisie (Netherlands)",
    "PPL": "Primeira Liga (Portugal)",
    "ELC": "Championship (England)",
    "BSA": "Brasileirao (Brazil)",
}


# ---------------------------------------------------------------- Football API
def _get(path, params=None):
    if not FOOTBALL_API_KEY:
        return {"error": "FOOTBALL_DATA_API_KEY .env mein nahi mili"}
    try:
        r = requests.get(
            f"{BASE_URL}{path}",
            headers={"X-Auth-Token": FOOTBALL_API_KEY},
            params={k: v for k, v in (params or {}).items() if v},
            timeout=15,
        )
    except requests.RequestException as e:
        return {"error": f"Network error: {e}"}
    if r.status_code == 429:
        return {"error": "Rate limit (10 requests/min). Thori der baad try karein."}
    if r.status_code != 200:
        return {"error": f"API error {r.status_code}: {r.text[:200]}"}
    return r.json()


def _to_local(utc_str):
    dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
    return dt.astimezone(LOCAL_TZ).strftime("%a %d %b, %I:%M %p")


def _slim(m):
    ft = m.get("score", {}).get("fullTime", {})
    return {
        "competition": m.get("competition", {}).get("name"),
        "home": m["homeTeam"].get("name"),
        "away": m["awayTeam"].get("name"),
        "kickoff_pkt": _to_local(m["utcDate"]),
        "status": m.get("status"),
        "score": f'{ft.get("home")}-{ft.get("away")}' if ft.get("home") is not None else None,
    }


def get_matches(date_from, date_to, competition=None, team=None):
    path = f"/competitions/{competition}/matches" if competition else "/matches"
    data = _get(path, {"dateFrom": date_from, "dateTo": date_to})
    if "error" in data:
        return data
    matches = [_slim(m) for m in data.get("matches", [])]
    if team:
        t = team.lower()
        matches = [m for m in matches if t in (m["home"] or "").lower() or t in (m["away"] or "").lower()]
    return {"count": len(matches), "matches": matches[:40]}


def get_standings(competition):
    data = _get(f"/competitions/{competition}/standings")
    if "error" in data:
        return data
    out = []
    for s in data.get("standings", []):
        if s.get("type") == "TOTAL":
            out.append({
                "group": s.get("group"),
                "table": [{"pos": r["position"], "team": r["team"]["name"], "pts": r["points"],
                           "played": r["playedGames"]} for r in s["table"]],
            })
    return {"standings": out}


TOOL_FUNCS = {"get_matches": get_matches, "get_standings": get_standings}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_matches",
            "description": "Get football fixtures/results between two dates (YYYY-MM-DD, max 10 days apart).",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_from": {"type": "string"},
                    "date_to": {"type": "string"},
                    "competition": {"type": "string", "enum": list(COMPETITIONS.keys())},
                    "team": {"type": "string", "description": "Team name filter, e.g. Barcelona"},
                },
                "required": ["date_from", "date_to"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_standings",
            "description": "Get the points table of a competition.",
            "parameters": {
                "type": "object",
                "properties": {"competition": {"type": "string", "enum": list(COMPETITIONS.keys())}},
                "required": ["competition"],
            },
        },
    },
]


def system_prompt():
    now = datetime.now(LOCAL_TZ)
    comps = ", ".join(f"{k}={v}" for k, v in COMPETITIONS.items())
    return (
        "You are a friendly football fixtures assistant.\n"
        f"Now (Pakistan time): {now.strftime('%A %d %B %Y, %I:%M %p')}. "
        f"Today UTC date: {datetime.now(timezone.utc).date()}.\n"
        f"Competitions: {comps}.\n"
        "Always call a tool for matches or tables, never guess. "
        "'Upcoming' means next 7 days. For 'today' use date_from=today, date_to=tomorrow. "
        "List each match as: Home vs Away - time (PKT). "
        "Reply in the user's language (Roman Urdu or English)."
    )


# ---------------------------------------------------------------- Agent
class FootballAgent:
    def __init__(self):
        self.client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
        self.history = []

    def ask(self, question):
        self.history.append({"role": "user", "content": question})
        for _ in range(5):  # max 5 tool rounds
            resp = self.client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "system", "content": system_prompt()}] + self.history,
                tools=TOOLS,
                tool_choice="auto",
            )
            msg = resp.choices[0].message
            if not msg.tool_calls:
                self.history.append({"role": "assistant", "content": msg.content})
                return msg.content

            self.history.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [tc.model_dump() for tc in msg.tool_calls],
            })
            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments or "{}")
                print(f"  [tool] {tc.function.name}({args})")
                result = TOOL_FUNCS[tc.function.name](**args)
                self.history.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result, ensure_ascii=False),
                })
        return "Maaf kijiye, jawab nahi mil saka. Dobara try karein."


def main():
    if not GROQ_API_KEY:
        print("GROQ_API_KEY .env mein daalein (console.groq.com se free milti hai)")
        return
    agent = FootballAgent()
    print("⚽ Football Agent (free) ready! exit likh kar band karein\n")
    while True:
        q = input("Aap: ").strip()
        if q.lower() in {"exit", "quit", "bye"}:
            break
        if q:
            print(f"\nAgent: {agent.ask(q)}\n")


if __name__ == "__main__":
    main()