# ⚽ Football Fixtures Agent

Ek AI agent jo aap ke sawal samajh kar live football fixtures, results aur points table batata hai — Pakistan time mein.

**Example sawal**
- aaj ke football matches kya hain?
- Champions League ke upcoming matches batao
- Real Madrid ka agla match kab hai?
- Premier League ki table dikhao

## Setup
1. Free API key lein: https://www.football-data.org/client/register
2. Anthropic API key lein: https://console.anthropic.com
3. Install & run:
```bash
pip install -r requirements.txt
cp .env.example .env      # dono keys .env mein daalein
python football_agent.py
```

## Kaise kaam karta hai
- Claude sawal samajhta hai aur decide karta hai kaunsa tool chalana hai
- `get_matches` → date range / competition / team ke hisaab se fixtures
- `get_standings` → league table
- Times UTC se Asia/Karachi mein convert hote hain

## Limits (free tier)
- 10 requests per minute
- Ek call mein max 10 din ka range
- Major leagues + Champions League covered (code mein `COMPETITIONS` list dekhein)
