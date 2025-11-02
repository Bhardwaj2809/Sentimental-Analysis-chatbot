import streamlit as st
from textblob import TextBlob
from datetime import datetime
import time
import random

# --- Page Config ---
st.set_page_config(page_title="💬 Modern Chatbot", page_icon="💬", layout="wide")

# --- Initialize Session ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- CSS for modern chat ---
st.markdown("""
<style>
body {
    background-color: #0f1117;
    color: #fff;
    font-family: 'Segoe UI', sans-serif;
}
#chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #2c313c;
    background-color: #1b1e27;
    scroll-behavior: smooth;
}
.chat-box {
    padding: 14px 20px;
    border-radius: 20px;
    margin: 8px 0;
    max-width: 70%;
    word-wrap: break-word;
    transition: all 0.3s ease;
}
.user-msg {
    background-color: #2c313c;
    text-align: right;
    float: right;
    clear: both;
}
.bot-msg {
    background-color: #3a3f4c;
    float: left;
    clear: both;
}
.keyword {
    background-color: #44475a;
    padding: 2px 6px;
    border-radius: 4px;
}
.sentiment {
    font-size: 0.8em;
    opacity: 0.7;
}
.mood {
    font-size: 0.8em;
    opacity: 0.7;
    color: #f0c674;
}
.typing {
    font-style: italic;
    opacity: 0.7;
}
</style>
""", unsafe_allow_html=True)

# --- Mood detection ---
def detect_mood(text):
    keywords = {
        "happy": ["happy","glad","joy","excited"],
        "sad": ["sad","unhappy","down"],
        "tired": ["tired","sleepy","exhausted"],
        "frustrated": ["frustrated","annoyed","upset"],
        "neutral": []
    }
    for mood, words in keywords.items():
        for word in words:
            if word.lower() in text.lower():
                return mood
    return "neutral"

# --- Bot reply ---
def generate_reply(mood, last_user=None):
    responses = {
        "happy":["Yay! You seem happy! 😄","Awesome! Keep smiling! 🌟"],
        "sad":["I'm here to listen. 💛","Oh no! Want to talk?"],
        "tired":["Maybe take a break ☕","Rest is important! 😴"],
        "frustrated":["Take a deep breath 💨","I understand. Let's calm down."],
        "neutral":["Alright 😐","Got it!"]
    }
    reply = random.choice(responses.get(mood, ["Okay."]))
    if last_user:
        reply += f" Earlier you said: '{last_user}'"
    return reply

# --- Keyword Highlighting ---
def highlight_keywords(text):
    words = text.split()
    highlighted = []
    for word in words:
        if word.lower() in ["happy","sad","tired","excited","angry","relaxed"]:
            highlighted.append(f"<span class='keyword'>{word}</span>")
        else:
            highlighted.append(word)
    return " ".join(highlighted)

# --- Render Chat ---
def render_chat(typing_text=None):
    container = st.container()
    container.markdown('<div id="chat-container">', unsafe_allow_html=True)
    for chat in st.session_state.history:
        # User message
        container.markdown(f"""
        <div class="chat-box user-msg">
            🧑‍💬 {highlight_keywords(chat['user'])} 
            <div class="sentiment">*{chat['sentiment']}*</div> 
            <div class="mood">({chat['mood']})</div>
        </div>
        """, unsafe_allow_html=True)
        # Bot message
        if chat['bot']:
            container.markdown(f"""
            <div class="chat-box bot-msg">
                🤖 {chat['bot']} 
                <div class="mood">({chat['mood']})</div>
            </div>
            """, unsafe_allow_html=True)
    # Typing animation
    if typing_text:
        container.markdown(f"""
        <div class="chat-box bot-msg typing">
            🤖 {typing_text}
        </div>
        """, unsafe_allow_html=True)
    container.markdown('</div>', unsafe_allow_html=True)
    # Smooth scroll
    st.markdown("""
        <script>
        var chatContainer = document.getElementById('chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;
        </script>
    """, unsafe_allow_html=True)

# --- UI ---
st.title("💬 Modern Chatbot")
st.write("Smooth scrolling, typing animation, keyword highlighting.")

user_input = st.text_input("Type your message here...")

if user_input:
    blob = TextBlob(user_input)
    sentiment_score = blob.sentiment.polarity
    sentiment = "😊 Positive" if sentiment_score > 0 else "😞 Negative" if sentiment_score < 0 else "😐 Neutral"
    mood = detect_mood(user_input)
    last_user_msg = st.session_state.history[-1]["user"] if st.session_state.history else None
    bot_reply = generate_reply(mood, last_user_msg)

    # Add user message first
    st.session_state.history.append({"user": user_input, "bot": "", "sentiment": sentiment, "mood": mood})

    # Typing animation
    for i in range(1, len(bot_reply)+1):
        render_chat(typing_text=bot_reply[:i])
        time.sleep(0.02)

    # Replace typing with final bot message
    st.session_state.history[-1]["bot"] = bot_reply
    render_chat()

# Initial render
if not user_input:
    render_chat()
