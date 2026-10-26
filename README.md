# ⚽ Football Agent

An AI-powered football assistant that answers questions about **today's matches, upcoming fixtures, results and league tables** — in **Roman Urdu or English**, with kickoff times in **Pakistan time (PKT)**.

### 🔴 Live Demo: [zain-football-agent.streamlit.app](https://zain-football-agent.streamlit.app/)

<!-- Screenshot: apni website ka screenshot "screenshot.png" naam se repo mein upload karo -->
![Football Agent screenshot](screenshot.png)

---

## ✨ Features

- 💬 **Natural chat** — ask in Roman Urdu or English, just like talking to a friend
- 📅 **Fixtures** — today's, tomorrow's or this week's matches
- 🏆 **Competition filter** — Champions League, Premier League, La Liga and more
- ⚪ **Team search** — "Real Madrid ka agla match kab hai?"
- ✅ **Results** — scores of finished matches
- 📊 **Standings** — live league tables
- 🕒 **Local time** — all kickoff times converted from UTC to Pakistan time
- 🎨 **Custom UI** — night-stadium theme with custom CSS on Streamlit

## 💬 Example Questions

| Ask this | Agent does |
|---|---|
| aaj ke football matches kya hain? | Lists all of today's fixtures |
| Champions League ke upcoming matches batao | Next 7 days of UCL matches |
| Real Madrid ka agla match kab hai? | Finds Real Madrid's next game |
| Premier League ki table dikhao | Shows current standings |
| kal ke Premier League results | Shows yesterday's scores |

## 🧠 How It Works

```
User question
     │
     ▼
┌─────────────────┐   decides which tool to call
│   Groq LLM      │ ─────────────────────────────┐
│ (gpt-oss-120b)  │                              ▼
└─────────────────┘              ┌──────────────────────────┐
     ▲                           │  Tools (Python)          │
     │   match data (JSON)       │  • get_matches()         │
     └───────────────────────────│  • get_standings()       │
                                 └────────────┬─────────────┘
                                              ▼
                                   football-data.org API
```

1. The user asks a question in the chat.
2. The LLM understands it and picks the right **tool** (function calling).
3. The tool fetches live data from **football-data.org**.
4. The LLM turns the data into a clean, friendly answer.

## 🛠️ Tech Stack

| Part | Technology |
|---|---|
| Language | Python |
| AI / LLM | Groq API (`openai/gpt-oss-120b`) with tool calling |
| Football data | [football-data.org](https://www.football-data.org/) API |
| Web app | Streamlit + custom CSS |
| Deployment | Streamlit Community Cloud |

## 🏆 Supported Competitions

UEFA Champions League · Premier League · La Liga · Serie A · Bundesliga · Ligue 1 · Eredivisie · Primeira Liga · EFL Championship · Brasileirão

## 🚀 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/zainawan1523/football-agent.git
cd football-agent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Get free API keys**
- Groq: [console.groq.com](https://console.groq.com/)
- Football data: [football-data.org/client/register](https://www.football-data.org/client/register)

**4. Create a `.env` file**
```
GROQ_API_KEY=your_groq_key
FOOTBALL_DATA_API_KEY=your_football_data_key
LOCAL_TZ=Asia/Karachi
GROQ_MODEL=openai/gpt-oss-120b
```

**5. Run**
```bash
streamlit run app.py          # web app
python football_agent.py      # terminal version
```

## 📁 Project Structure

```
football-agent/
├── .streamlit/
│   └── config.toml        # dark theme colors
├── app.py                 # Streamlit website (UI + custom CSS)
├── football_agent.py      # Agent logic, tools and API calls
├── requirements.txt
└── README.md
```

## ⚠️ Limitations

- Free API tier: 10 requests per minute
- Max 10-day date range per query
- No player stats, lineups or live minute-by-minute updates (yet)

## 🔮 Future Ideas

- Top scorers
- Match reminders
- Team logos in answers
- Live score updates

---

👨‍💻 Built by **Zain Awan** · [GitHub](https://github.com/zainawan1523)
