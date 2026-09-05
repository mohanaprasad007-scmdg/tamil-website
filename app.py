from flask import Flask, jsonify, request, send_from_directory
import random
import os

app = Flask(__name__)

MODEL = "gpt-5.6-luna"

ideas = [
    {
        "title": "💡 Website Idea",
        "message": "Build a portfolio and showcase your projects."
    },
    {
        "title": "🚀 Coding Challenge",
        "message": "Create a calculator with HTML, CSS and JavaScript."
    },
    {
        "title": "🎨 Creative Idea",
        "message": "Design a Tamil-themed landing page."
    },
    {
        "title": "🤖 AI Project",
        "message": "Create an AI chatbot for your Tamil website."
    },
    {
        "title": "📚 Learning Idea",
        "message": "Learn one new Python concept and build a tiny program."
    }
]


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# =========================
# OTHER FILES / PAGES
# =========================

@app.route("/<path:filename>")
def files(filename):
    return send_from_directory(".", filename)


# =========================
# EXPLORE API
# =========================

@app.route("/api/explore")
def explore():
    return jsonify(random.choice(ideas))


# =========================
# AI TAMIL ASSISTANT
# =========================

@app.route("/api/ai", methods=["POST"])
def ai_assistant():

    try:

        data = request.get_json(silent=True) or {}

        message = str(
            data.get("message", "")
        ).strip()

        if not message:
            return jsonify({
                "success": False,
                "error": "Please enter a question."
            }), 400

        if len(message) > 1000:
            return jsonify({
                "success": False,
                "error": "Please keep your question under 1000 characters."
            }), 400


        # Check API key only when AI is requested
        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            return jsonify({
                "success": False,
                "error": "AI service is not configured on the server."
            }), 500


        # Import OpenAI only when needed
        from openai import OpenAI

        client = OpenAI(
            api_key=api_key
        )


        instructions = """
You are Tamil AI Assistant, the friendly AI guide
for a website called "தமிழ்".

Your main purpose is to help users learn about:

• Tamil language
• Tamil history
• Tamil culture
• Tamil literature
• Sangam literature
• Thirukkural
• Tamil festivals
• Tamil food
• Tamil architecture
• Tamil arts
• Tamil music
• Tamil people and traditions
• Tamil heritage

Rules:

1. Be friendly and educational.
2. Answer Tamil questions naturally in Tamil.
3. Answer English questions in English.
4. If the user mixes Tamil and English, you may naturally mix both.
5. Give clear and easy-to-understand answers.
6. Do not invent historical facts.
7. If something is uncertain, clearly say that it is uncertain.
8. When explaining Thirukkural, provide the meaning clearly.
9. Keep normal answers reasonably concise.
10. Use headings and bullet points when useful.
11. Encourage users to explore Tamil heritage.
"""


        response = client.responses.create(
            model=MODEL,
            instructions=instructions,
            input=message,
            max_output_tokens=600
        )


        answer = response.output_text.strip()


        if not answer:
            answer = "மன்னிக்கவும். பதில் கிடைக்கவில்லை."


        return jsonify({
            "success": True,
            "answer": answer
        })


    except Exception as error:

        print("AI ERROR:", error)

        return jsonify({
            "success": False,
            "error": "AI service is temporarily unavailable. Please try again."
        }), 500


# =========================
# HEALTH CHECK
# =========================

@app.route("/api/health")
def health():

    return jsonify({
        "status": "online",
        "ai": bool(
            os.environ.get("OPENAI_API_KEY")
        )
    })


# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get("PORT", 5000)
        ),
        debug=False
        )
