import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "Please enter symptoms."})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI medical assistant. Give simple, safe, helpful advice. Do not give dangerous instructions."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})


@app.route("/dashboard-data")
def dashboard():
    return jsonify({
        "visits": 120,
        "users": 45,
        "reports": 30
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
