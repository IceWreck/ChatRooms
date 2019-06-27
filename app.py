import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/")
def index():
    return redirect('/chat')


@app.route("/chat")
def chat():
    return render_template("/sample.html")

@socketio.on("client_emit")
def message(message_data):
    message_text = message_data["text"]
    emit("server_emit", {"text": message_text}, broadcast=True)
