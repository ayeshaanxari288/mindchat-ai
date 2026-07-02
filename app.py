import streamlit as st
import google.generativeai as genai
import time
import json
from datetime import datetime

st.set_page_config(
    page_title="MindChat AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700;800&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #0d0d1a;
    font-family: 'Nunito', sans-serif;
}

.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(124,58,237,0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(59,130,246,0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, rgba(236,72,153,0.1) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1a 0%, #12122a 100%) !important;
    border-right: 1px solid rgba(124,58,237,0.3) !important;
}

section[data-testid="stSidebar"] * {
    font-family: 'Nunito', sans-serif !important;
}

.app-header {
    text-align: center;
    padding: 28px 20px 22px;
    background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(59,130,246,0.1));
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 24px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}

.app-header::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent 0deg, rgba(124,58,237,0.05) 60deg, transparent 120deg);
    animation: rotate 8s linear infinite;
}

@keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.app-header h1 {
    font-family: 'Fredoka One', cursive;
    font-size: 38px;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    position: relative;
    z-index: 1;
    margin-bottom: 6px;
}

.app-header p {
    color: #6b7280;
    font-size: 13px;
    font-weight: 600;
    position: relative;
    z-index: 1;
}

.header-badges {
    display: flex;
    gap: 8px;
    justify-content: center;
    margin-top: 10px;
    position: relative;
    z-index: 1;
    flex-wrap: wrap;
}

.badge { padding: 4px 12px; border-radius: 50px; font-size: 11px; font-weight: 700; }
.badge-purple { background: rgba(124,58,237,0.2); color: #a78bfa; border: 1px solid rgba(124,58,237,0.3); }
.badge-blue   { background: rgba(59,130,246,0.2);  color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
.badge-pink   { background: rgba(236,72,153,0.2);  color: #f472b6; border: 1px solid rgba(236,72,153,0.3); }
.badge-green  { background: rgba(34,197,94,0.2);   color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }

.chat-box {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 24px;
    padding: 20px;
    min-height: 380px;
    max-height: 460px;
    overflow-y: auto;
    margin-bottom: 14px;
    scrollbar-width: thin;
    scrollbar-color: rgba(124,58,237,0.3) transparent;
}

.chat-box::-webkit-scrollbar { width: 4px; }
.chat-box::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.3); border-radius: 4px; }

.empty-state { text-align: center; padding: 50px 20px; }

.empty-icon {
    font-size: 60px;
    display: block;
    margin-bottom: 14px;
    animation: float 3s ease-in-out infinite;
}

@keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }

.empty-title { font-family: 'Fredoka One', cursive; font-size: 20px; color: #4b5563; margin-bottom: 6px; }
.empty-sub   { color: #374151; font-size: 13px; font-weight: 600; }

.suggestion-chips { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; margin-top: 16px; }
.chip {
    background: rgba(124,58,237,0.1);
    border: 1px solid rgba(124,58,237,0.2);
    color: #a78bfa;
    border-radius: 50px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 700;
}

.user-row { display: flex; justify-content: flex-end; margin: 12px 0; animation: slide-left 0.3s ease; }
@keyframes slide-left { from { opacity:0; transform:translateX(20px); } to { opacity:1; transform:translateX(0); } }

.ai-row { display: flex; justify-content: flex-start; gap: 10px; margin: 12px 0; align-items: flex-end; animation: slide-right 0.3s ease; }
@keyframes slide-right { from { opacity:0; transform:translateX(-20px); } to { opacity:1; transform:translateX(0); } }

.user-bubble {
    background: linear-gradient(135deg, #7c3aed, #6d28d9);
    color: white;
    border-radius: 20px 20px 4px 20px;
    padding: 12px 16px;
    max-width: 65%;
    font-size: 14px;
    line-height: 1.65;
    box-shadow: 0 4px 20px rgba(124,58,237,0.35);
    word-wrap: break-word;
}

.ai-avatar {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #60a5fa, #3b82f6);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    box-shadow: 0 4px 12px rgba(96,165,250,0.4);
    flex-shrink: 0;
}

.ai-bubble {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    color: #e2e8f0;
    border-radius: 4px 20px 20px 20px;
    padding: 12px 16px;
    max-width: 65%;
    font-size: 14px;
    line-height: 1.7;
    word-wrap: break-word;
}

.msg-time { font-size: 10px; color: #374151; margin-top: 3px; text-align: right; }
.ai-time  { font-size: 10px; color: #374151; margin-top: 3px; }

.token-bar-wrap {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 12px;
}

.token-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 6px;
}

.token-bar-key   { color: #6b7280; letter-spacing: 1px; text-transform: uppercase; }
.token-bar-value { color: #a78bfa; }

.token-bar-bg {
    background: rgba(255,255,255,0.06);
    border-radius: 50px;
    height: 6px;
    overflow: hidden;
}

.token-bar-fill {
    height: 100%;
    border-radius: 50px;
    transition: width 0.5s ease;
}

.warning-banner {
    background: rgba(234,179,8,0.1);
    border: 1px solid rgba(234,179,8,0.3);
    border-radius: 12px;
    padding: 10px 14px;
    margin-bottom: 12px;
    font-size: 13px;
    color: #fbbf24;
    font-weight: 700;
    text-align: center;
}

.exam-box {
    background: rgba(34,197,94,0.06);
    border: 1px solid rgba(34,197,94,0.2);
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 14px;
}

.exam-title {
    font-family: 'Fredoka One', cursive;
    font-size: 16px;
    color: #4ade80;
    margin-bottom: 10px;
}

.exam-step {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    margin-bottom: 8px;
    font-size: 13px;
    color: #9ca3af;
    font-weight: 600;
}

.exam-num {
    background: rgba(34,197,94,0.2);
    color: #4ade80;
    border-radius: 50%;
    width: 22px; height: 22px;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px;
    font-weight: 800;
    flex-shrink: 0;
}

.exam-pass {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.3);
    border-radius: 8px;
    padding: 6px 12px;
    color: #4ade80;
    font-size: 12px;
    font-weight: 700;
    text-align: center;
    margin-top: 8px;
}

.exam-pending {
    background: rgba(107,114,128,0.1);
    border: 1px solid rgba(107,114,128,0.2);
    border-radius: 8px;
    padding: 6px 12px;
    color: #6b7280;
    font-size: 12px;
    font-weight: 700;
    text-align: center;
    margin-top: 8px;
}

textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(124,58,237,0.3) !important;
    border-radius: 16px !important;
    color: #e2e8f0 !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 15px !important;
}

textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}

textarea::placeholder { color: #4b5563 !important; }
textarea, .stTextArea textarea { color: #ffffff !important; caret-color: #a78bfa !important; }

div.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 13px !important;
    font-family: 'Fredoka One', cursive !important;
    font-size: 17px !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
    transition: all 0.2s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(124,58,237,0.55) !important;
}

.sidebar-logo  { text-align:center; font-size:42px; margin-bottom:4px; animation: float 3s ease-in-out infinite; }
.sidebar-brand { font-family:'Fredoka One',cursive; font-size:20px; background:linear-gradient(135deg,#a78bfa,#60a5fa); -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-align:center; margin-bottom:3px; }
.sidebar-sub   { color:#4b5563; font-size:11px; text-align:center; margin-bottom:12px; font-weight:600; }

.stat-row { display:flex; gap:8px; margin-bottom:12px; }
.stat-box { flex:1; background:rgba(124,58,237,0.1); border:1px solid rgba(124,58,237,0.2); border-radius:10px; padding:10px 6px; text-align:center; }
.stat-num { font-family:'Fredoka One',cursive; font-size:24px; color:#a78bfa; }
.stat-lbl { font-size:9px; color:#6b7280; font-weight:700; letter-spacing:1px; text-transform:uppercase; }

.memory-panel { background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:12px; margin-top:10px; }
.memory-panel-title { font-family:'Fredoka One',cursive; font-size:13px; color:#a78bfa; margin-bottom:7px; }
.memory-row { display:flex; justify-content:space-between; padding:4px 0; border-bottom:1px solid rgba(255,255,255,0.04); font-size:11px; }
.memory-row:last-child { border-bottom:none; }
.memory-key { color:#6b7280; font-weight:600; }
.memory-val { color:#a78bfa; font-weight:700; }

label { color:#6b7280 !important; font-size:11px !important; font-weight:700 !important; letter-spacing:1px !important; text-transform:uppercase !important; }
div[data-baseweb="select"] > div { background:rgba(255,255,255,0.04) !important; border:1px solid rgba(124,58,237,0.3) !important; border-radius:10px !important; color:#e2e8f0 !important; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 18px !important; padding-bottom: 8px !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────
MAX_HISTORY    = 20
TOKEN_LIMIT    = 1000000
WARN_THRESHOLD = 0.75
GEMINI_MODEL   = "gemini-2.0-flash"

# API Key — safely from secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = None

PERSONAS = {
    "🤖 Smart Assistant": "You are a helpful, friendly and smart AI assistant. Answer clearly and concisely.",
    "🐍 Python Tutor":    "You are an expert Python tutor. Explain with simple examples and code snippets.",
    "✍️ Creative Writer": "You are a creative writing genius. Help craft beautiful stories, poems and content.",
    "📚 Study Buddy":     "You are a patient, encouraging study partner. Break down complex topics simply.",
    "💼 Career Advisor":  "You are a professional career advisor. Give practical, motivating career guidance.",
    "🌟 Life Coach":      "You are a warm and motivating life coach. Help users reflect and grow positively.",
}

SUGGESTIONS = [
    "Tell me about yourself",
    "Help me write a poem",
    "Explain Machine Learning",
    "What career should I choose?",
]

# ── Session state ─────────────────────────────────────
if "messages"     not in st.session_state: st.session_state.messages     = []
if "total_turns"  not in st.session_state: st.session_state.total_turns  = 0
if "total_tokens" not in st.session_state: st.session_state.total_tokens = 0
if "exam_step"    not in st.session_state: st.session_state.exam_step    = 0
if "exam_passed"  not in st.session_state: st.session_state.exam_passed  = False
if "show_exam"    not in st.session_state: st.session_state.show_exam    = False


# ── Core functions ────────────────────────────────────
def get_response(user_msg, history, system_prompt):
    """
    Artificial Memory Loop:
    Input(Mt U Ht-1) -> Gemini API -> Response(Rt)
    Full history sent every turn to create stateful behavior.
    """
    if not API_KEY:
        return None, 0, "API key not found. Please add GEMINI_API_KEY to Streamlit Secrets."
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=system_prompt,
        )

        # Build history in Gemini format — role-content objects
        gemini_history = []
        for m in history:
            role = "user" if m["role"] == "user" else "model"
            gemini_history.append({
                "role":  role,
                "parts": [m["content"]]
            })

        # Start stateful chat with full history
        chat     = model.start_chat(history=gemini_history)
        response = chat.send_message(user_msg)

        # Token count
        tokens_used = 0
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            tokens_used = getattr(response.usage_metadata, "total_token_count", 0)

        return response.text, tokens_used, None

    except Exception as e:
        return None, 0, str(e)


def sliding_window(msgs, limit=MAX_HISTORY):
    """
    FIFO Sliding Window Algorithm:
    Drop oldest message pairs when limit exceeded.
    Prevents context window overflow and token budget exhaustion.
    """
    if len(msgs) > limit:
        excess = len(msgs) - limit
        if excess % 2:
            excess += 1
        msgs = msgs[excess:]
    return msgs


def export_chat():
    lines = [
        "MindChat AI — Conversation Export",
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "=" * 50,
        "",
    ]
    for msg in st.session_state.messages:
        role = "You" if msg["role"] == "user" else "MindChat AI"
        lines.append(f"[{msg.get('time', '')}] {role}:")
        lines.append(msg["content"])
        lines.append("")
    return "\n".join(lines)


def check_memory_exam(user_msg, ai_reply):
    """
    3-Step Memory Exam (from PDF):
    Step 1: State Initialization  — user tells name
    Step 2: Context Distraction   — large volume generation
    Step 3: State Extraction      — AI recalls name from history
    """
    msg_lower   = user_msg.lower()
    reply_lower = ai_reply.lower()

    if st.session_state.exam_step == 0:
        if "my name is" in msg_lower or "i am " in msg_lower or "call me" in msg_lower:
            st.session_state.exam_step = 1

    elif st.session_state.exam_step == 1:
        if any(w in msg_lower for w in ["poem", "story", "write", "explain", "tell me about", "what is"]):
            st.session_state.exam_step = 2

    elif st.session_state.exam_step == 2:
        if "my name" in msg_lower or "what is my name" in msg_lower or "do you remember my name" in msg_lower:
            for m in st.session_state.messages:
                if m["role"] == "user" and (
                    "my name is" in m["content"].lower() or
                    "call me"    in m["content"].lower()
                ):
                    words = m["content"].lower().split()
                    for i, w in enumerate(words):
                        if w in ["is", "me", "am"] and i + 1 < len(words):
                            name = words[i + 1].strip(".,!?")
                            if name in reply_lower:
                                st.session_state.exam_passed = True
                                st.session_state.exam_step   = 3
                                return
            st.session_state.exam_step = 3


# ── SIDEBAR ──────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🧠</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-brand">MindChat AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Project 1 — DecodeLabs 2026</div>', unsafe_allow_html=True)

    token_pct = min((st.session_state.total_tokens / TOKEN_LIMIT) * 100, 100) if TOKEN_LIMIT > 0 else 0
    bar_color = "#ef4444" if token_pct > 75 else "#f59e0b" if token_pct > 50 else "#a78bfa"

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-box"><div class="stat-num">{len(st.session_state.messages)}</div><div class="stat-lbl">Messages</div></div>
        <div class="stat-box"><div class="stat-num">{st.session_state.total_turns}</div><div class="stat-lbl">Turns</div></div>
        <div class="stat-box"><div class="stat-num">{st.session_state.total_tokens}</div><div class="stat-lbl">Tokens</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="token-bar-wrap">
        <div class="token-bar-label">
            <span class="token-bar-key">Context Window Usage</span>
            <span class="token-bar-value">{token_pct:.1f}%</span>
        </div>
        <div class="token-bar-bg">
            <div class="token-bar-fill" style="width:{token_pct}%; background:{bar_color};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    persona       = st.selectbox("AI Persona", list(PERSONAS.keys()))
    system_prompt = st.text_area("System Instructions", value=PERSONAS[persona], height=80)

    st.markdown(f"""
    <div class="memory-panel">
        <div class="memory-panel-title">Memory Architecture</div>
        <div class="memory-row"><span class="memory-key">Algorithm</span><span class="memory-val">FIFO Sliding Window</span></div>
        <div class="memory-row"><span class="memory-key">Window Size</span><span class="memory-val">{MAX_HISTORY} messages</span></div>
        <div class="memory-row"><span class="memory-key">Stored Now</span><span class="memory-val">{len(st.session_state.messages)}</span></div>
        <div class="memory-row"><span class="memory-key">State Type</span><span class="memory-val">In-Memory Array</span></div>
        <div class="memory-row"><span class="memory-key">Warn At</span><span class="memory-val">{int(WARN_THRESHOLD*100)}% usage</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🧪 Run Memory Exam"):
        st.session_state.show_exam   = not st.session_state.show_exam
        st.session_state.exam_step   = 0
        st.session_state.exam_passed = False

    if st.session_state.messages:
        st.download_button(
            label     = "💾 Export Chat",
            data      = export_chat(),
            file_name = f"mindchat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime      = "text/plain",
        )

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages     = []
        st.session_state.total_turns  = 0
        st.session_state.total_tokens = 0
        st.session_state.exam_step    = 0
        st.session_state.exam_passed  = False
        st.rerun()


# ── MAIN UI ──────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>🧠 MindChat AI</h1>
    <p>Custom AI Chatbot with Stateful Memory — DecodeLabs Batch 2026</p>
    <div class="header-badges">
        <span class="badge badge-purple">Memory Enabled</span>
        <span class="badge badge-blue">Gemini 1.5 Flash</span>
        <span class="badge badge-pink">Sliding Window</span>
        <span class="badge badge-green">Token Tracking</span>
    </div>
</div>
""", unsafe_allow_html=True)

# API key missing warning
if not API_KEY:
    st.error("GEMINI_API_KEY not found! Please add it to Streamlit Secrets → Settings → Secrets.")
    st.stop()

# Context window overflow warning
if token_pct >= WARN_THRESHOLD * 100:
    st.markdown(f"""
    <div class="warning-banner">
        Context window is {token_pct:.0f}% full — oldest messages will be pruned by the sliding window algorithm
    </div>
    """, unsafe_allow_html=True)

# Memory exam panel
if st.session_state.show_exam:
    step   = st.session_state.exam_step
    passed = st.session_state.exam_passed

    step1_done = "✅" if step >= 1 else "⏳"
    step2_done = "✅" if step >= 2 else "⏳"
    step3_done = "✅" if step >= 3 else "⏳"

    result_html = (
        '<div class="exam-pass">MEMORY VERIFIED — AI Successfully Recalled!</div>'
        if passed else
        '<div class="exam-pass">Test in progress...</div>'
        if step > 0 else
        '<div class="exam-pending">Start chatting to begin the exam</div>'
    )

    st.markdown(f"""
    <div class="exam-box">
        <div class="exam-title">🧪 Memory Exam — 3 Step Verification</div>
        <div class="exam-step"><div class="exam-num">1</div><div>{step1_done} Tell the AI your name (e.g. "My name is Ayesha")</div></div>
        <div class="exam-step"><div class="exam-num">2</div><div>{step2_done} Distract it — ask for a poem or explain a topic</div></div>
        <div class="exam-step"><div class="exam-num">3</div><div>{step3_done} Ask "What is my name?" — AI should recall from memory</div></div>
        {result_html}
    </div>
    """, unsafe_allow_html=True)

# Chat area
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

if not st.session_state.messages:
    chips = "".join([f'<span class="chip">{s}</span>' for s in SUGGESTIONS])
    st.markdown(f"""
    <div class="empty-state">
        <span class="empty-icon">💬</span>
        <div class="empty-title">Start a Conversation!</div>
        <div class="empty-sub">I remember everything we discuss</div>
        <div class="suggestion-chips">{chips}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        t = msg.get("time", "")
        c = msg["content"].replace("\n", "<br>")
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="user-row">
                <div>
                    <div class="user-bubble">{c}</div>
                    <div class="msg-time">{t}</div>
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ai-row">
                <div class="ai-avatar">🤖</div>
                <div>
                    <div class="ai-bubble">{c}</div>
                    <div class="ai-time">{t}</div>
                </div>
            </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input
user_input = st.text_area(
    "message",
    placeholder      = "Ask me anything — I remember our whole conversation!",
    height           = 80,
    label_visibility = "collapsed",
    key              = "msg_input",
)

col1, col2 = st.columns([3, 1])

with col1:
    send = st.button("✨ Send Message")

with col2:
    if st.button("🎲 Random"):
        st.rerun()

if send:
    msg_text = user_input.strip()
    if not msg_text:
        st.warning("Please type something first! Empty messages are blocked by the Structural Validation Gate.")
    else:
        now = time.strftime("%I:%M %p")

        # Step 1: Ingest & Append — add user message to history
        st.session_state.messages.append({
            "role":    "user",
            "content": msg_text,
            "time":    now,
        })

        # Step 2: Apply FIFO sliding window
        st.session_state.messages = sliding_window(st.session_state.messages)

        # Step 3: Transmit & Record — send full history to Gemini
        history_so_far = st.session_state.messages[:-1]

        with st.spinner("MindChat is thinking..."):
            reply, tokens, err = get_response(msg_text, history_so_far, system_prompt)

        if err:
            st.error(f"Error: {err}")
            st.session_state.messages.pop()
        else:
            # Step 4: Append AI response to history
            st.session_state.messages.append({
                "role":    "assistant",
                "content": reply,
                "time":    time.strftime("%I:%M %p"),
            })
            st.session_state.total_turns  += 1
            st.session_state.total_tokens += tokens
            check_memory_exam(msg_text, reply)
            st.rerun()

st.markdown("""
<div style="text-align:center; margin-top:12px; color:#1f2937;
font-family:'Fredoka One',cursive; font-size:12px;">
    MindChat AI &nbsp;|&nbsp; Project 1 — Custom AI Chatbot with Memory &nbsp;|&nbsp; DecodeLabs 2026
</div>
""", unsafe_allow_html=True)
