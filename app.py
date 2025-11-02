import streamlit as st
from textblob import TextBlob
from datetime import datetime
import time
import random

st.set_page_config(page_title="💬 Advanced 3D Chatbot", page_icon="💬", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

# --- CSS ---
st.markdown("""
<style>
body { background-color: #0e1117; color: #fff; font-family: 'Segoe UI', sans-serif; }
.chat-box { padding: 12px 18px; border-radius: 20px; margin: 6px 0; max-width: 70%; display: inline-block; word-wrap: break-word; transition: all 0.3s ease; opacity:0; transform: translateY(20px); }
.chat-box.show { opacity:1; transform: translateY(0); }
.user-msg { background-color: #1e2128; text-align: right; float: right; clear: both; }
.bot-msg { background-color: #2c313c; float: left; clear: both; }
.user-msg:hover { background-color: #292c34; transform: scale(1.03); }
.bot-msg:hover { background-color: #3a3f4c; transform: scale(1.03); }
.sentiment { font-size: 0.8em; opacity: 0.7; }
.mood { font-size: 0.8em; opacity: 0.7; color: #f0c674; }
.time { font-size: 0.7em; opacity: 0.5; }
.keyword { background-color: #44475a; padding: 2px 5px; border-radius: 4px; }
.stDivider { border-top: 1px solid #333; margin: 10px 0; }
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

# --- Display messages ---
def add_user_message(message, sentiment, mood, time_str):
    st.markdown(f"""
    <div class="chat-box user-msg show">
        🧑‍💬 {highlight_keywords(message)} <div class="sentiment">*{sentiment}*</div> <div class="mood">({mood})</div>
    </div>
    """, unsafe_allow_html=True)

def add_bot_message(message, time_str, typing=True):
    placeholder = st.empty()
    if typing:
        displayed_text = ""
        for char in message:
            displayed_text += char
            placeholder.markdown(f"""
            <div class="chat-box bot-msg show">
                🤖 {displayed_text} <div class="time">(typing...)</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.02)
    placeholder.markdown(f"""
    <div class="chat-box bot-msg show">
        🤖 {message} <div class="time">(at {time_str})</div>
    </div>
    """, unsafe_allow_html=True)
    return placeholder

# --- Streamlit layout ---
st.title("💬 Advanced Chatbot with 3D Buddy")
st.write("Hi! Chat with me and watch my buddy react!")

user_input = st.chat_input("Type your message here...")

if user_input:
    blob = TextBlob(user_input)
    sentiment_score = blob.sentiment.polarity
    sentiment = "😊 Positive" if sentiment_score > 0 else "😞 Negative" if sentiment_score < 0 else "😐 Neutral"
    mood = detect_mood(user_input)
    timestamp = datetime.now().strftime("%H:%M")
    last_user_msg = st.session_state.history[-1]["user"] if st.session_state.history else None
    bot_reply = generate_reply(mood, last_user_msg)

    st.session_state.history.append({"user": user_input, "bot": bot_reply, "sentiment": sentiment, "mood": mood, "time": timestamp})

    add_user_message(user_input, sentiment, mood, timestamp)
    add_bot_message(bot_reply, timestamp)

for chat in st.session_state.history[::-1]:
    add_user_message(chat['user'], chat['sentiment'], chat.get("mood","neutral"), chat['time'])
    if chat["bot"]:
        add_bot_message(chat['bot'], chat['time'], typing=False)
    st.divider()

# --- 3D Buddy ---
last_mood = st.session_state.history[-1]['mood'] if st.session_state.history else 'neutral'

html_code = """
<html>
  <head>
    <style>body{margin:0;overflow:hidden;}</style>
  </head>
  <body>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r152/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.152.0/examples/js/loaders/GLTFLoader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.152.0/examples/js/controls/DragControls.js"></script>
    <script>
      window.addEventListener('DOMContentLoaded', ()=>{
        let scene = new THREE.Scene();
        let camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 0.1, 1000);
        let renderer = new THREE.WebGLRenderer({alpha:true});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        let light = new THREE.DirectionalLight(0xffffff,1);
        light.position.set(1,2,3);
        scene.add(light);

        let loader = new THREE.GLTFLoader();
        let buddy;
        loader.load('assets/CuteRobot.glb',
            function(gltf){
                buddy = gltf.scene;
                buddy.scale.set(1.5,1.5,1.5);
                buddy.position.set(0,-1,0);
                scene.add(buddy);
                console.log('✅ GLB loaded successfully!');
            },
            undefined,
            function(error){
                console.error('❌ Error loading GLB:', error);
                let geometry = new THREE.BoxGeometry();
                let material = new THREE.MeshStandardMaterial({color:0xff0000});
                buddy = new THREE.Mesh(geometry, material);
                scene.add(buddy);
            }
        );

        camera.position.z = 5;

        function animate(){
            requestAnimationFrame(animate);
            if(buddy){
                const mood = '""" + last_mood + """';
                if(mood==='happy') buddy.rotation.y +=0.05;
                else if(mood==='sad') buddy.rotation.x = 0.1*Math.sin(Date.now()*0.005);
                else if(mood==='tired') buddy.rotation.z = 0.02*Math.sin(Date.now()*0.005);
                else if(mood==='frustrated') buddy.position.y = 0.1*Math.sin(Date.now()*0.01);
            }
            renderer.render(scene,camera);
        }
        animate();
      });
    </script>
  </body>
</html>
"""

st.components.v1.html(html_code, height=600)
