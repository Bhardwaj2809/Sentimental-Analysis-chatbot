import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Sentiment Analysis Chatbot", page_icon="💬")

st.title("💬 Sentiment Analysis Chatbot")
st.write("Type a message and I’ll tell you the sentiment!")

user_input = st.text_input("You:", "")

if user_input:
    blob = TextBlob(user_input)
    sentiment = blob.sentiment.polarity

    if sentiment > 0:
        result = "😊 Positive"
    elif sentiment < 0:
        result = "😞 Negative"
    else:
        result = "😐 Neutral"

    st.markdown(f"**Sentiment:** {result}")
