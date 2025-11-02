import streamlit as st
from transformers import pipeline

# --------------------------
# Load model once (cached)
# --------------------------
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")

sentiment_analyzer = load_model()

# --------------------------
# Initialize session state
# --------------------------
if "history" not in st.session_state:
    st.session_state["history"] = []

# --------------------------
# App layout
# --------------------------
st.title("💬 Sentiment Analysis Chatbot 🤖")
st.write("Type your message and see how the bot reacts based on your sentiment!")

# Input form (prevents instant reruns)
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", "")
    submitted = st.form_submit_button("Send")

# --------------------------
# Process user message
# --------------------------
if submitted and user_input:
    # Add user message to chat
    st.session_state.history.append({"user": user_input})

    # Analyze sentiment
    result = sentiment_analyzer(user_input)[0]
    label = result["label"]
    score = result["score"]

    # Bot reply based on sentiment
    if label == "POSITIVE":
        reply = f"😊 You seem positive! I'm glad you're feeling great. (Confidence: {score:.2f})"
    elif label == "NEGATIVE":
        reply = f"😞 I'm sorry to hear that. Want to talk more about it? (Confidence: {score:.2f})"
    else:
        reply = f"😐 Neutral mood detected. (Confidence: {score:.2f})"

    st.session_state.history.append({"bot": reply})

# --------------------------
# Display conversation history
# --------------------------
for chat in st.session_state.history:
    if "user" in chat:
        st.markdown(f"**🧍You:** {chat['user']}")
    if "bot" in chat:
        st.markdown(f"**🤖 Bot:** {chat['bot']}")
