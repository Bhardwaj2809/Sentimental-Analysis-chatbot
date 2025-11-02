import streamlit as st
from textblob import TextBlob
from datetime import datetime
import random

st.set_page_config(page_title="💬 Advanced 3D Chatbot", page_icon="💬", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

# --- CSS ---
st.markdown("""
<style>
body { background-color: #0e1117; color: #fff; font-family: 'Segoe UI', sans-serif; }
#chat-container { max-height: 400px; overflow-y: auto; padding: 10px; border: 1px solid #333; border-radius: 10px; margin-bottom:10px; }
.chat-box { padding: 12px 18px; border-radius: 20px; margin: 6px 0; max-width: 70%; display: inline-block; word-wrap: break-word; transition: all 0.3s ease; }
.user-msg { background-color: #1e2128; text-align: right; float: right; clear: both; }
.bot-msg { background-color: #2c313c; float: left; clear: both; }
.sentiment { font-size: 0.8em; opacity: 0.7; }
.mood { font-size: 0.8em; opacity: 0.7; color: #f0c674; }
.keyword { background-color: #44475a; padding: 2px 5px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# --- Mood detection ---
def detect_mood(text):
    keywords = {
        "happy":["happy","glad","joy","excited"],
        "sad":["sad","unhappy","down"],
        "tired":["tired","sleepy","exhausted"],
        "frustrated":["frustrated","annoyed","upset"],
        "neutral":[]
    }
    for mood, words in keywords.items():
        for word in words:
            if word in text.lower():
                return mood
    return "neutral"

# --- Bot reply generator ---
def generate_reply(mood, last_user=None):
    responses = {
        "happy":["Yay! You seem happy! 😄", "Awesome! Keep smiling! 🌟"],
        "sad":["I'm here to listen. 💛", "Oh no! Do you want to talk?"],
        "tired":["Maybe take a break ☕", "Rest is important! 😴"],
        "frustrated":["Deep breath 💨", "I understand. Let's calm down."],
        "neutral":["Alright 😐", "Got it!"]
    }
    reply = random.choice(responses.get(mood, ["Okay."]))
    if last_user:
        reply += f" Earlier you said: '{last_user}'"
    return reply

# --- Highlight keywords ---
def highlight_keywords(text):
    words = text.split()
    highlighted = []
    for word in words:
        if word.lower() in ["happy","sad","tired","excited","angry","relaxed"]:
            highlighted.append(f"<span class='keyword'>{word}</span>")
        else:
            highlighted.append(word)
    return " ".join(highlighted)

# --- Chat rendering ---
def render_chat():
    chat_container = st.container()
    chat_container.markdown('<div id="chat-container">', unsafe_allow_html=True)
    for chat in st.session_state.history:
        # User message
        chat_container.markdown(f"""
        <div class="chat-box user-msg">
            🧑‍💬 {highlight_keywords(chat['user'])} <div class="sentiment">*{chat['sentiment']}*</div> <div class="mood">({chat['mood']})</div>
        </div>
        """, unsafe_allow_html=True)
        # Bot message
        chat_container.markdown(f"""
        <div class="chat-box bot-msg">
            🤖 {chat['bot']} <div class="mood">({chat['mood']})</div>
        </div>
        """, unsafe_allow_html=True)
    chat_container.markdown('</div>', unsafe_allow_html=True)
    # Auto-scroll to bottom
    st.markdown("""
        <script>
        var chatContainer = document.getElementById('chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;
        </script>
    """, unsafe_allow_html=True)

# --- Streamlit layout ---
st.title("💬 Advanced Chatbot with 3D Buddy")
st.write("Chat like ChatGPT — new messages appear at bottom!")

user_input = st.text_input("Type your message here...")

if user_input:
    blob = TextBlob(user_input)
    sentiment_score = blob.sentiment.polarity
    sentiment = "😊 Positive" if sentiment_score > 0 else "😞 Negative" if sentiment_score < 0 else "😐 Neutral"
    mood = detect_mood(user_input)
    timestamp = datetime.now().strftime("%H:%M")
    last_user_msg = st.session_state.history[-1]["user"] if st.session_state.history else None
    bot_reply = generate_reply(mood, last_user_msg)

    st.session_state.history.append({"user": user_input, "bot": bot_reply, "sentiment": sentiment, "mood": mood, "time": timestamp})

render_chat()

# --- 3D Buddy ---
last_mood = st.session_state.history[-1]['mood'] if st.session_state.history else 'neutral'

st.components.v1.html(f"""
<div id="three-container" style="width:100%; height:400px;"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r152/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.152.0/examples/js/loaders/GLTFLoader.js"></script>
<script>
const container = document.getElementById('three-container');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, container.clientWidth/container.clientHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({{alpha:true}});
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

const light = new THREE.DirectionalLight(0xffffff,1);
light.position.set(1,2,3);
scene.add(light);

const loader = new THREE.GLTFLoader();
let buddy;
loader.load('assets/CuteRobot.glb',
    function(gltf){{
        buddy = gltf.scene;
        buddy.scale.set(1.5,1.5,1.5);
        buddy.position.set(0,-1,0);
        scene.add(buddy);
    }},
    undefined,
    function(error){{
        console.error('Error loading GLB', error);
        const geometry = new THREE.BoxGeometry();
        const material = new THREE.MeshStandardMaterial({{color:0xff0000}});
        buddy = new THREE.Mesh(geometry, material);
        scene.add(buddy);
    }}
);

camera.position.z = 5;

function animate(){{
    requestAnimationFrame(animate);
    if(buddy){{
        const mood = '{last_mood}';
        if(mood==='happy') buddy.rotation.y +=0.05;
        else if(mood==='sad') buddy.rotation.x = 0.1*Math.sin(Date.now()*0.005);
        else if(mood==='tired') buddy.rotation.z = 0.02*Math.sin(Date.now()*0.005);
        else if(mood==='frustrated') buddy.position.y = 0.1*Math.sin(Date.now()*0.01);
    }}
    renderer.render(scene,camera);
}}
animate();
</script>
""", height=400)
