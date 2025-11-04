import streamlit as st
from transformers import pipeline
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")

sentiment_analyzer = load_model()
if "history" not in st.session_state:
    st.session_state["history"] = []
st.title("💬 Sentiment Analysis Chatbot 🤖")
st.write("Type your message and see how the bot reacts based on your sentiment!")
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", "")
    submitted = st.form_submit_button("Send")
if submitted and user_input:
    st.session_state.history.append({"user": user_input})
    result = sentiment_analyzer(user_input)[0]
    label = result["label"]
    score = result["score"]
    if label == "POSITIVE":
        reply = f"😊 You seem positive! I'm glad you're feeling great."
    elif label == "NEGATIVE":
        reply = f"😞 I'm sorry to hear that. Want to talk more about it?."
    else:
        reply = f"😐 Neutral mood detected. (Confidence: {score:.2f})"
    st.session_state.history.append({"bot": reply})
for chat in st.session_state.history:
    if "user" in chat:
        st.markdown(f"**🧍You:** {chat['user']}")
    if "bot" in chat:
        st.markdown(f"**🤖 Bot:** {chat['bot']}")
