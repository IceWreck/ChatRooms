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
    return render_template("/chat.html")

@socketio.on("client_emit")
def message(message_data):
    message_text = message_data["text"]
    message_channel =message_data["channel"]
    # send the message back to the channel it came from
    emit("server_emit", {"text": message_text, "channel":message_channel}, broadcast=True)
