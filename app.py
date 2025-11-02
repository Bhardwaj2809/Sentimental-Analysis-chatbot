import streamlit as st
from textblob import TextBlob
from datetime import datetime

# --- Page setup ---
st.set_page_config(page_title="💬 Sentiment Analysis Chatbot", page_icon="💬", layout="centered")

# --- Custom CSS for dark mode and chat bubbles ---
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #fff;
    font-family: 'Segoe UI', sans-serif;
}
.chat-box {
    padding: 10px 15px;
    border-radius: 15px;
    margin: 5px 0;
    max-width: 70%;
    display: inline-block;
    word-wrap: break-word;
}
.user-msg {
    background-color: #1e2128;
    text-align: right;
}
.bot-msg {
    background-color: #2c313c;
}
.sentiment {
    font-size: 0.8em;
    opacity: 0.7;
}
.time {
    font-size: 0.7em;
    opacity: 0.5;
}
.stDivider {
    border-top: 1px solid #333;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("💬 Sentiment Analysis Chatbot")
st.write("Hi! I'm your mood analyzer. Type something below 👇")

# --- Chat history ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- User input ---
user_input = st.chat_input("Type your message here...")

# --- Handle input ---
if user_input:
    blob = TextBlob(user_input)
    sentiment_score = blob.sentiment.polarity

    if sentiment_score > 0:
        sentiment = "😊 Positive"
        bot_reply = "That's awesome! I'm glad you're feeling good!"
    elif sentiment_score < 0:
        sentiment = "😞 Negative"
        bot_reply = "I'm sorry to hear that. Want to talk more about it?"
    else:
        sentiment = "😐 Neutral"
        bot_reply = "Alright, noted."

    st.session_state.history.append(
        {"user": user_input, "sentiment": sentiment, "bot": bot_reply, "time": datetime.now().strftime("%H:%M")}
    )

# --- Display chat messages ---
for chat in st.session_state.history[::-1]:
    st.markdown(f"""
    <div class="chat-box user-msg">
        🧑‍💬 {chat['user']} <div class="sentiment">*{chat['sentiment']}*</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="chat-box bot-msg">
        🤖 {chat['bot']} <div class="time">(at {chat['time']})</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
