from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load Hugging Face sentiment model
sentiment_pipeline = pipeline("sentiment-analysis")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    user_text = request.form["msg"]
    result = sentiment_pipeline(user_text)[0]
    label = result["label"]
    score = result["score"]

    if label == "POSITIVE":
        sentiment = f"Positive 😊 ({score:.2f})"
        reply = "That's awesome! I'm glad you're feeling good."
    elif label == "NEGATIVE":
        sentiment = f"Negative 😞 ({score:.2f})"
        reply = "I'm sorry to hear that. Want to talk more about it?"
    else:
        sentiment = f"Neutral 😐 ({score:.2f})"
        reply = "Alright, noted."

    return jsonify({"sentiment": sentiment, "response": reply})
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
