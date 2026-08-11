

import os

import httpx
import streamlit as st

import db

API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="PyCoder", page_icon=">", layout="wide")

db.init_db()

# --------------------------------------------------------------------------
# Theme — same dark/terminal palette as the Gradio UI
# --------------------------------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;500&display=swap');

    :root {
        --bg-0: #0d1117; --bg-1: #11161d; --bg-2: #1a2130;
        --border: #2a3242; --text-1: #e6edf3; --text-2: #8b949e;
        --py-blue: #4b8bbe; --py-yellow: #ffd43b;
    }
    .stApp { background: var(--bg-0); color: var(--text-1); font-family: 'Inter', sans-serif; }
    section[data-testid="stSidebar"] { background: var(--bg-1); border-right: 1px solid var(--border); }

    .pycoder-header { text-align: center; padding: 8px 0 4px; }
    .pycoder-logo {
        font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 28px;
        color: var(--text-1);
        background: linear-gradient(90deg, var(--py-blue), var(--py-yellow));
        background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .pycoder-logo::after {
        content: "_"; -webkit-text-fill-color: var(--py-yellow);
        animation: blink 1.1s steps(1) infinite;
    }
    @keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }
    .pycoder-subtitle {
        font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-2);
    }

    .settings-badge {
        font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--py-yellow);
        background: rgba(255,212,59,.08); border: 1px solid rgba(255,212,59,.25);
        padding: 2px 8px; border-radius: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = db.create_conversation()
if "messages" not in st.session_state:
    st.session_state.messages = []  # [{"role": ..., "content": ...}, ...]

# --------------------------------------------------------------------------
# Sidebar — history + status, mirroring the Gradio sidebar
# --------------------------------------------------------------------------

with st.sidebar:
    st.markdown('<div class="pycoder-logo" style="font-size:18px;">History</div>', unsafe_allow_html=True)

    conversations = db.list_conversations()
    labels = {c["id"]: c["title"] for c in conversations}

    if conversations:
        selected = st.selectbox(
            "Past conversations",
            options=[c["id"] for c in conversations],
            format_func=lambda cid: labels.get(cid, cid),
            label_visibility="collapsed",
        )
        col1, col2 = st.columns(2)
        if col1.button("Load", use_container_width=True):
            st.session_state.conversation_id = selected
            st.session_state.messages = db.get_history(selected)
            st.rerun()
        if col2.button("New chat", use_container_width=True):
            st.session_state.conversation_id = db.create_conversation()
            st.session_state.messages = []
            st.rerun()
    else:
        if st.button("New chat", use_container_width=True):
            st.session_state.conversation_id = db.create_conversation()
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:13px; color:var(--text-2);">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span>Status</span><span class="settings-badge">online</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span>Max Tokens</span><span class="settings-badge">150</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------

st.markdown(
    """
    <div class="pycoder-header">
        <span class="pycoder-logo">&gt; PyCoder</span>
        <div class="pycoder-subtitle"># your expert Python & AI pair-programmer</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Chat history render
# --------------------------------------------------------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------------------------------------------------------
# Example prompts (only shown on a fresh conversation)
# --------------------------------------------------------------------------

EXAMPLES = [
    "Write a Python function to check if a string is a palindrome.",
    "What's the difference between a list and a tuple?",
    "Show me how to read a CSV with pandas.",
    "Explain Python decorators with a short example.",
]

prompt = None
if not st.session_state.messages:
    cols = st.columns(len(EXAMPLES))
    for col, example in zip(cols, EXAMPLES):
        if col.button(example, use_container_width=True):
            prompt = example

typed = st.chat_input("Message PyCoder...")
if typed:
    prompt = typed

# --------------------------------------------------------------------------
# Send + stream the response from the FastAPI backend
# --------------------------------------------------------------------------

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    payload = {
        "message": prompt,
        "history": st.session_state.messages[:-1],
        "max_new_tokens": 150,
    }

    with st.chat_message("assistant"):
        placeholder = st.empty()
        acc_text = ""
        try:
            with httpx.stream("POST", f"{API_BASE_URL}/chat", json=payload, timeout=None) as resp:
                resp.raise_for_status()
                for chunk in resp.iter_text():
                    if not chunk:
                        continue
                    acc_text += chunk
                    placeholder.markdown(acc_text + "▌")
            placeholder.markdown(acc_text)
        except httpx.HTTPError as e:
            acc_text = f"⚠️ Couldn't reach the model API at `{API_BASE_URL}`: {e}"
            placeholder.markdown(acc_text)

    st.session_state.messages.append({"role": "assistant", "content": acc_text})
    db.add_message(st.session_state.conversation_id, "user", prompt)
    db.add_message(st.session_state.conversation_id, "assistant", acc_text)
