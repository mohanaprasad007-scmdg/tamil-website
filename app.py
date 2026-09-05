from flask import Flask, jsonify, send_from_directory
import random
app=Flask(__name__)
ideas=[
{"title":"💡 Website Idea","message":"Build a portfolio and showcase your projects."},
{"title":"🚀 Coding Challenge","message":"Create a calculator with HTML, CSS and JavaScript."},
{"title":"🎨 Creative Idea","message":"Design a Tamil-themed landing page."},
{"title":"🤖 AI Project","message":"Create a small AI chatbot for your website."},
{"title":"📚 Learning Idea","message":"Learn one new Python concept and build a tiny program."}]
@app.get("/")
def home(): return send_from_directory(".", "index.html")
@app.get("/api/explore")
def explore(): return jsonify(random.choice(ideas))
if __name__=="__main__": app.run(debug=True)
