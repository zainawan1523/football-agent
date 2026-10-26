"""
Football Agent - Website (custom theme)
Chalane ke liye:  streamlit run app.py
"""

import streamlit as st
from football_agent import FootballAgent, GROQ_API_KEY

st.set_page_config(page_title="Football Agent", page_icon="⚽", layout="centered")

# ------------------------------------------------------------------ CUSTOM CSS
# Colors yahan se badlo 👇
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;700&display=swap');

:root {
  --pitch-dark: #07130c;
  --pitch: #0d2416;
  --line: rgba(255,255,255,0.07);
  --neon: #b6ff3b;
  --neon-soft: rgba(182,255,59,0.15);
  --text: #eef5ea;
  --muted: #9bb3a2;
  --card: rgba(255,255,255,0.04);
  --border: rgba(255,255,255,0.10);
}

/* Poori website ka background: stadium pitch with stripes */
[data-testid="stAppViewContainer"] {
  background:
    radial-gradient(ellipse at top, rgba(182,255,59,0.10), transparent 55%),
    repeating-linear-gradient(90deg, var(--pitch) 0 80px, #0f2a1a 80px 160px);
  color: var(--text);
  font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stBottom"] > div { background: transparent; }

/* Sidebar */
[data-testid="stSidebar"] {
  background: var(--pitch-dark);
  border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] h2 {
  font-family: 'Bebas Neue', sans-serif;
  letter-spacing: 2px;
  color: var(--neon);
}

/* Buttons */
.stButton > button {
  background: var(--card);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 12px;
  text-align: left;
  transition: all .2s ease;
}
.stButton > button:hover {
  border-color: var(--neon);
  color: var(--neon);
  background: var(--neon-soft);
  transform: translateX(3px);
}

/* Hero header */
.hero {
  text-align: center;
  padding: 28px 16px 22px;
  margin-bottom: 18px;
  border: 1px solid var(--border);
  border-radius: 20px;
  background: linear-gradient(160deg, rgba(0,0,0,0.35), rgba(0,0,0,0.15));
  position: relative;
  overflow: hidden;
}
.hero::before {               /* center circle jaisa design */
  content: "";
  position: absolute;
  width: 220px; height: 220px;
  border: 2px solid var(--line);
  border-radius: 50%;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
}
.hero h1 {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 3.4rem;
  letter-spacing: 4px;
  margin: 0;
  color: var(--text);
  position: relative;
}
.hero h1 span { color: var(--neon); }
.hero p { color: var(--muted); margin: 6px 0 0; position: relative; }
.live-dot {
  display: inline-block;
  width: 8px; height: 8px;
  background: var(--neon);
  border-radius: 50%;
  margin-right: 6px;
  box-shadow: 0 0 10px var(--neon);
  animation: pulse 1.6s infinite;
}
@keyframes pulse { 50% { opacity: .3; } }

/* Chat messages */
[data-testid="stChatMessage"] {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 14px 16px;
  margin-bottom: 10px;
  backdrop-filter: blur(6px);
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li { color: var(--text); }

/* Chat input box */
[data-testid="stChatInput"] {
  border: 1px solid var(--neon) !important;
  border-radius: 14px;
  box-shadow: 0 0 18px var(--neon-soft);
}

/* Spinner color */
.stSpinner > div { border-top-color: var(--neon) !important; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------ HEADER
st.markdown(
    """
    <div class="hero">
      <h1>⚽ FOOTBALL <span>AGENT</span></h1>
      <p><span class="live-dot"></span>Fixtures · Results · Tables — Pakistan time mein</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY nahi mili. .env file ya Streamlit secrets mein daalein.")
    st.stop()

# ------------------------------------------------------------------ STATE
if "agent" not in st.session_state:
    st.session_state.agent = FootballAgent()
    st.session_state.messages = []

# ------------------------------------------------------------------ SIDEBAR
with st.sidebar:
    st.header("Quick Sawal")
    examples = [
        "📅 aaj ke football matches kya hain?",
        "🏆 Champions League ke upcoming matches",
        "⚪ Real Madrid ka agla match kab hai?",
        "📊 Premier League ki table dikhao",
        "✅ kal ke Premier League results",
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state.pending = ex[2:].strip()
    st.divider()
    if st.button("🗑️  Nayi chat", use_container_width=True):
        st.session_state.agent = FootballAgent()
        st.session_state.messages = []
        st.rerun()

# ------------------------------------------------------------------ CHAT
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="⚽" if msg["role"] == "assistant" else "🧑"):
        st.markdown(msg["content"])

question = st.chat_input("Apna sawal likhein... jaise 'aaj ke matches batao'")
if not question and st.session_state.get("pending"):
    question = st.session_state.pop("pending")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="⚽"):
        with st.spinner("Matches dhoond raha hoon..."):
            try:
                answer = st.session_state.agent.ask(question)
            except Exception as e:
                answer = f"⚠️ Error: {e}"
        st.markdown(answer or "Koi jawab nahi mila, dobara try karein.")

    st.session_state.messages.append({"role": "assistant", "content": answer})