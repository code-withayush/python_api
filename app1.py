from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from waitress import serve
import os
import logging
app = Flask(__name__)
CORS(app)
from dotenv import load_dotenv
import os

load_dotenv() 
# 🔹 Set your Google Gemini API Key here

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))




# Choose a model
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def index():
    return render_template("3.html")

@app.route("/generate", methods=["POST"])
def generate_story():
    data = request.get_json()
    genre = data.get("genre", "Fantasy")
    theme = data.get("theme", "Hope")
    character = data.get("character", "Hero")

    prompt = f"Write a short, creative story idea. Genre: {genre}, Theme: {theme}, Main Character: {character}."

    try:
        response = model.generate_content(prompt)
        story_idea = response.text.strip()
        return jsonify({"storyIdea": story_idea})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     print("🚀 Flask server starting...")
#     app.run(debug=True, port=5000)

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    print("🚀 Flask server starting...")
    serve(app, host="0.0.0.0", port=8080)
