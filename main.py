import streamlit as st
from flask import Flask, render_template, request, jsonify
from app.chat import chat_app, get_gemini_response
from app.vision import vision_app
from app.movies import display_movies
from app.database import init_db, save_message, get_chat_history, clear_chat_history

app = Flask(__name__)

# Sample movies data
sample_movies = [
    {"title": "Inception", "year": 2010, "poster_url": "https://source.unsplash.com/random/200x300/?inception"},
    {"title": "The Shawshank Redemption", "year": 1994, "poster_url": "https://source.unsplash.com/random/200x300/?prison"},
    {"title": "The Godfather", "year": 1972, "poster_url": "https://source.unsplash.com/random/200x300/?mafia"},
    {"title": "The Dark Knight", "year": 2008, "poster_url": "https://source.unsplash.com/random/200x300/?batman"},
    {"title": "Pulp Fiction", "year": 1994, "poster_url": "https://source.unsplash.com/random/200x300/?crime"},
    {"title": "Forrest Gump", "year": 1994, "poster_url": "https://source.unsplash.com/random/200x300/?running"},
]

@app.route('/')
def home():
    return render_template('index.html', content=render_template('home.html', movies=sample_movies[:6]))

@app.route('/browse')
def browse():
    movies = display_movies() or sample_movies
    return render_template('index.html', content=render_template('browse.html', movies=movies))

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        if 'poster' not in request.files:
            return 'No file part'
        file = request.files['poster']
        if file.filename == '':
            return 'No selected file'
        if file:
            # Process the image using vision_app function
            result = vision_app(file)
            return render_template('index.html', content=render_template('scan_result.html', result=result))
    return render_template('index.html', content=render_template('scan.html'))

@app.route('/chat')
def chat():
    return render_template('index.html', content=render_template('chat.html'))

@app.route('/chat_message', methods=['POST'])
def chat_message():
    message = request.json['message']
    response = get_gemini_response(message)
    save_message("user", message)
    save_message("bot", response)
    return jsonify({'response': response})

@app.route('/get_chat_history')
def get_history():
    history = get_chat_history()
    return jsonify(history)

@app.route('/clear_chat_history', methods=['POST'])
def clear_history():
    clear_chat_history()
    return jsonify({'status': 'success'})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
