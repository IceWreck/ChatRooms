import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_socketio import SocketIO, emit
from flask_session import Session
from models import *
from functionality import login_required
from werkzeug.security import check_password_hash, generate_password_hash



app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# TODO: make a seperate file for routes


@app.route("/")
def index():
    return redirect('/chat')

@app.route("/register", methods=["GET", "POST"])
def register():
    # Forget existing user sessions
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # TODO: Replace this with a form validation function

        # Ensure username was submitted
        if not request.form.get("username"):
            return "must provide username"
        # Ensure password was submitted
        elif not request.form.get("password"):
            return"must provide password"
        # Ensure password was submitted
        elif not request.form.get("cpassword"):
            return "must provide confirmation"
        # Check if both passwords are same
        if request.form.get("password") != request.form.get("cpassword"):
            return "passwords don't match"
        username = request.form.get("username")
        password = request.form.get("password")
        # Query database for username
        user_exists = Users.query.filter_by(name=username).count()
        if user_exists == 1:
            return "Sorry, username has already been taken."
        # not taken; proceed
        new_user = Users(name=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        # Now that the user is in the db, log them in
        user_in_db = Users.query.filter_by(name=username).first()
        session["user_id"] = user_in_db.id
        # Redirect user to home
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget existing user sessions
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # TODO: Replace this with a form validation function

        # Ensure username was submitted
        if not request.form.get("username"):
            return "must provide username"
        # Ensure password was submitted
        elif not request.form.get("password"):
            return"must provide password"
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Log them in
        user_in_db = Users.query.filter_by(name=username).first()
        if not user_in_db or not check_password_hash(user_in_db.password, password):
            return "Invalid user/pass"
        session["user_id"] = user_in_db.id

        # Redirect user to home
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("loginpage.html")

@app.route("/chat")
@login_required
def chat():
    return render_template("/chat.html")

@socketio.on("client_emit")
def message(message_data):
    message_text = message_data["text"]
    message_channel =message_data["channel"]
    # send the message back to the channel it came from
    emit("server_emit", {"text": message_text, "channel":message_channel}, broadcast=True)
