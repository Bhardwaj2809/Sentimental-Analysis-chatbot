import streamlit as st
from transformers import pipeline

# Load Hugging Face sentiment model
sentiment_pipeline = pipeline("sentiment-analysis")

# Streamlit App
st.set_page_config(page_title="Sentiment Chatbot", page_icon="🤖")
st.title("🤖 Sentiment Analysis Chatbot")
st.write("Type something and I’ll tell you the sentiment and respond!")

# User input
user_input = st.text_input("You:", "")

if st.button("Send") and user_input:
    # Analyze sentiment
    result = sentiment_pipeline(user_input)[0]
    label = result["label"]
    score = result["score"]

    # Determine reply based on sentiment
    if label == "POSITIVE":
        sentiment = f"Positive 😊 ({score:.2f})"
        reply = "That's awesome! I'm glad you're feeling good."
    elif label == "NEGATIVE":
        sentiment = f"Negative 😞 ({score:.2f})"
        reply = "I'm sorry to hear that. Want to talk more about it?"
    else:
        sentiment = f"Neutral 😐 ({score:.2f})"
        reply = "Alright, noted."

    # Display output
    st.markdown(f"**Sentiment:** {sentiment}")
    st.markdown(f"**Chatbot:** {reply}")
