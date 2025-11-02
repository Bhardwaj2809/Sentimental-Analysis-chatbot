import streamlit as st
from textblob import TextBlob
import random

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Type your message here...")

if user_input:
    blob = TextBlob(user_input)
    sentiment_score = blob.sentiment.polarity
    sentiment = "😊 Positive" if sentiment_score > 0 else "😞 Negative" if sentiment_score < 0 else "😐 Neutral"

    # Generate simple bot response
    if sentiment_score > 0.1:
        bot_reply = "That's great! I'm glad to hear that."
    elif sentiment_score < -0.1:
        bot_reply = "I’m sorry to hear that. Want to talk more about it?"
    else:
        bot_reply = "Okay, noted."

    # Save in session
    st.session_state.history.append({"user": user_input, "bot": bot_reply, "sentiment": sentiment})

# Display chat
for chat in st.session_state.history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['bot']} ({chat['sentiment']})")
