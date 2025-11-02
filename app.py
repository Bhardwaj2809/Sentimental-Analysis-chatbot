from flask import Flask, render_template, request, jsonify
from textblob import TextBlob

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_text = request.form["msg"]
    blob = TextBlob(user_text)
    sentiment_score = blob.sentiment.polarity

    # Determine sentiment
    if sentiment_score > 0.1:
        sentiment = "Positive 😊"
        response = "That's great! I'm glad to hear that."
    elif sentiment_score < -0.1:
        sentiment = "Negative 😞"
        response = "I’m sorry to hear that. Want to talk more about it?"
    else:
        sentiment = "Neutral 😐"
        response = "Okay, noted."

    return jsonify({
        "sentiment": sentiment,
        "response": response
    })

if __name__ == "__main__":
    app.run(debug=True)
