import streamlit as st
from transformers import pipeline

# --------------------------
# Initialize session state
# --------------------------
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

if "mood" not in st.session_state:
    st.session_state["mood"] = None

if "history" not in st.session_state:
    st.session_state["history"] = []

# --------------------------
# Define input clearing callback
# --------------------------
def clear_input():
    st.session_state.user_input = ""

# --------------------------
# Layout
# --------------------------
st.title("Sentiment Analysis Chatbot 🤖")

user_input = st.text_input(
    "Type your message here:",
    key="user_input",
    on_change=clear_input
)

if user_input:
    # Append user message to history
    st.session_state.history.append({"user": user_input})
    
    # Run sentiment analysis
    sentiment_analyzer = pipeline("sentiment-analysis")
    result = sentiment_analyzer(user_input)[0]
    
    # Store mood in session state
    st.session_state.mood = result['label']
    
    # Append bot response to history
    st.session_state.history.append({"bot": f"Mood detected: {result['label']} ({result['score']:.2f})"})

# --------------------------
# Display conversation history
# --------------------------
st.subheader("Conversation History")
for chat in st.session_state.history:
    if "user" in chat:
        st.markdown(f"**You:** {chat['user']}")
    if "bot" in chat:
        st.markdown(f"**Bot:** {chat['bot']}")
