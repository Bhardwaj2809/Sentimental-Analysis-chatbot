from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    user_text = request.form["msg"]
    blob = TextBlob(user_text)
    sentiment_score = blob.sentiment.polarity

    if sentiment_score > 0:
        sentiment = f"Positive 😊 ({sentiment_score:.2f})"
        reply = "That's awesome! I'm glad you're feeling good."
    elif sentiment_score < 0:
        sentiment = f"Negative 😞 ({sentiment_score:.2f})"
        reply = "I'm sorry to hear that. Want to talk more about it?"
    else:
        sentiment = f"Neutral 😐 ({sentiment_score:.2f})"
        reply = "Alright, noted."

    return jsonify({"sentiment": sentiment, "response": reply})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
