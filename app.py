from flask import Flask, render_template, request, jsonify
import requests
from random import choice

app = Flask(__name__)

NEWS_API_KEY = "e674a2a0044843dbb554bad4a6c39e17"  # Replace with your NewsAPI key

def get_news(query="latest"):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "pageSize": 15,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    articles = data.get("articles", [])
    # Optionally: Only show articles where the query is in the title (for more relevant results)
    if query and query != "latest":
        articles = [a for a in articles if query.lower() in (a.get('title') or '').lower()]
    return articles

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "latest")
    articles = get_news(query)
    return render_template("index.html", articles=articles, query=query)

@app.route("/ai-chat", methods=["POST"])
def ai_chat():
    user_message = request.json.get("message", "").strip().lower()
    # --- Simple rule-based responses for demo ---
    if not user_message:
        return jsonify({"reply": "Hi! How can I help you with news today?"})
    if "hello" in user_message or "hi" in user_message:
        return jsonify({"reply": "Hello! 👋 What news are you interested in today?"})
    if "latest" in user_message or "trending" in user_message:
        return jsonify({"reply": "Try using the search box above to find the latest or trending news on any topic!"})
    if "weather" in user_message:
        return jsonify({"reply": "Sorry, I can only help with news topics right now. Try searching for political, tech, or sports news!"})
    if "who made you" in user_message or "your name" in user_message:
        return jsonify({"reply": "I'm your Green News Assistant, here to help you find and understand news articles!"})
    if "summarize" in user_message and "news" in user_message:
        return jsonify({"reply": "I can summarize the news you searched for. Please let me know the topic you'd like summarized."})
    # Fallback
    fallback = [
        "I'm here to assist you! Try asking about technology, sports, politics, or anything in the news.",
        "You can use the search bar to look up news on any topic. Or ask me for tips!",
        "I'm still learning. Please ask about news topics or try searching above!"
    ]
    return jsonify({"reply": choice(fallback)})

if __name__ == "__main__":
    app.run(debug=True)