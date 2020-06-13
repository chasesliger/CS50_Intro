# some code taken from CS50's webtrack distribution code (general web app configuration, etc)

import os
import json
import requests

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup_weather, lookup_parks

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///weather50.db")

# Make sure NPS API key is set
if not os.environ.get("NPS_KEY"):
    raise RuntimeError("NPS_KEY not set")

# Make sure Open Weather API key is set
if not os.environ.get("Open_weather_key"):
    raise RuntimeError("Open_weather_key not set")


@app.route("/", methods=["GET","POST"])
@login_required
def index():
    """Displays User's Homepage"""
    query = db.execute("SELECT state FROM users WHERE id = :user_id", user_id = session["user_id"])

    state = str(query[0]["state"])

    print(state)

    data = lookup_parks(state)

    return render_template("index.html", data = data, state = state)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure a username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure a password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure the re-entered password was the same as the first
        elif not (request.form.get("password") == request.form.get("confirmation")):
            return apology("re-entered password does not match the first", 403)

        # Ensure a password was submitted
        elif not request.form.get("state"):
            return apology("must provide state", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username is not already taken
        if len(rows) != 0:
            return apology("that user name is already taken", 403)

        username = request.form.get("username")
        password = request.form.get("password")
        hash = generate_password_hash(password)
        state = request.form.get("state")

        db.execute("INSERT INTO users (username, hash, state) VALUES (:username, :hash, :state)", username=username, hash=hash, state=state)

        # Remember which user has logged in
        session["user_id"] = db.execute("SELECT * FROM users WHERE username = :username",
                                        username=request.form.get("username"))

        # Display that registration was successful
        return render_template("rs.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/change_state", methods=["GET", "POST"])
@login_required
def change_state():
    """Change your state"""

    # want to be able to change the user's state in the database
    if request.method == "POST":

        state = request.form.get("state")

        db.execute("UPDATE users SET state = :state WHERE id = :user_id", state=state,
                    user_id = session["user_id"])

        return redirect(url_for('index'))


    else:

        return render_template("change_state.html")

@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    """Change password"""
    if request.method == "POST":
        # password = request.form.get("passord")
        # old_hash = db.execute("SELECT hash FROM users WHERE id = :user_id",
        #                      user_id = session["user_id"])

        # if old_hash != str(generate_password_hash(password)):
        #     return apology("That is not your correct current password")

        if request.form.get("new_password") == None:
            return apology("new password cannot be blank")

        if request.form.get("new_password") != request.form.get("confirmation"):
            return apology("re-entered new password does not match the first")

        new_hash = generate_password_hash(request.form.get("new_password"))

        db.execute("UPDATE users SET hash = :new_hash WHERE id = :user_id", new_hash=new_hash,
                    user_id = session["user_id"])

        # Redirect user to home page
        flash("Password changed")
        return redirect(url_for('index'))

    else:
        return render_template("change_password.html")


@app.route("/weather", methods=["POST"])
@login_required
def weather():
    """Display weather of selected park."""
    latlong = request.form.get("latlong")
    latlong = latlong.split(",")
    data = lookup_weather(latlong[0],latlong[1])
    return render_template("weather.html", data = data)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
