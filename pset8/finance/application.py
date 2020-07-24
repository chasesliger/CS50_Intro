import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # get current cash on hand
    cash = db.execute("SELECT * FROM users WHERE id=:user_id",
                      user_id=session["user_id"])[0]["cash"]

    # initialize net worth so we don't get an error if its a new user
    net_worth = cash

    # get stock info
    query = db.execute("SELECT * FROM stocks WHERE user_id=:user_id",
                       user_id=session["user_id"])

    # make a list of the stocks
    stocks = []

    # iterate over query and add info to list in the form of a dictionary for each stock
    for row in query:
        symbol = row["symbol"]
        shares = row["shares"]
        stock_info = lookup(symbol)

        stock_dict = {
            "symbol": symbol,
            "name": stock_info["name"],
            "shares": shares,
            "price": stock_info["price"],
            "total": shares*stock_info["price"]
        }

        stocks.append(stock_dict)

    # calculate the net worth with a for loop
    sum_of_stocks = 0
    for stock in stocks:
        total = stock["price"] * stock["shares"]
        sum_of_stocks = sum_of_stocks + total
    net_worth = cash + sum_of_stocks

    return render_template("index.html", stocks=stocks, cash=cash, net_worth=net_worth)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        lookup_value = lookup(symbol)

        # check to make sure the symbol is valid
        if lookup_value == None:
            return (apology("Sorry, that is not a valid stock symbol..."))
        # check to make sure the user put in a number greater than 0 for stocks to buy
        elif shares <= 0:
            return (apology("Sorry, you must input 1 or more to buy a stock"))

        # make a query to find out how much money the user has in their account
        cash_query = db.execute("SELECT cash FROM users WHERE id = :user_id",
                                user_id=session["user_id"])
        cash = float(cash_query[0]["cash"])
        price = shares * float(lookup_value["price"])

        if price > cash:
            return apology("Sorry, you don't have enough money for that transaction...")

        # update user's balance (cash - price)
        db.execute("UPDATE users SET cash = :new_balance WHERE id = :user_id", new_balance=(cash-price), user_id=session["user_id"])

        # check to see if stock is alreay owned
        owned_query = db.execute("SELECT * FROM stocks WHERE symbol = :symbol AND user_id = :user_id",
                                 symbol=symbol, user_id=session["user_id"])
        if len(owned_query) != 0:
            prev_shares = owned_query[0]["shares"]
            new_shares = prev_shares + shares
            db.execute("UPDATE stocks SET shares = :new_shares WHERE user_id = :user_id AND symbol=:symbol",
                       new_shares=new_shares, user_id=session["user_id"], symbol=symbol)

        # otherwise create a new row in stocks for the symbol and user
        else:
            db.execute("INSERT INTO stocks(user_id, symbol, shares) VALUES (:user_id, :symbol, :shares)", user_id=session["user_id"],
                       symbol=symbol, shares=shares)

        # update history table
        db.execute("INSERT INTO history(user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)", user_id=session["user_id"],
                   symbol=symbol, shares=shares, price=float(lookup_value["price"]))

        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    query = db.execute("SELECT * FROM history WHERE user_id = :user_id", user_id=session["user_id"])

    transactions = []
    # iterate over query and add info to list in the form of a dictionary for each stock
    for row in query:
        symbol = row["symbol"]
        shares = row["shares"]
        price = row["price"]
        time = row["time"]

        trans_dict = {
            "symbol": symbol,
            "shares": shares,
            "price": price,
            "time": time
        }

        transactions.append(trans_dict)

    return render_template("history.html", transactions=transactions)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == ("POST"):
        symbol = request.form.get("symbol")
        lookup_value = lookup(symbol)
        if lookup_value == None:
            return apology("Sorry, that is not a valid stock symbol...")
        else:
            message = "A share of " + lookup_value["name"] + " " + lookup_value["symbol"] + \
                " costs $" + str(lookup_value["price"]) + "."
            return render_template("quoted.html", message=message)

    else:
        return render_template("quote.html")


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

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username is not already taken
        if len(rows) != 0:
            return apology("that user name is already taken", 403)

        username = request.form.get("username")
        password = request.form.get("password")
        hash = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hash)

        # Remember which user has logged in
        session["user_id"] = db.execute("SELECT * FROM users WHERE username = :username",
                                        username=request.form.get("username"))

        # Redirect user to home page
        flash("Registered!")
        return redirect("index.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == ("POST"):
        # if post get symbols and shares from form
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # check to make sure user entered a positive number for shares
        if not int(shares) > 0:
            return apology("Sorry, you must enter a positive integer")

        # query for number of shares
        shares_query = db.execute("SELECT * FROM stocks WHERE user_id = :user_id AND symbol= :symbol",
                                  user_id=session["user_id"], symbol=symbol)

        current_shares = int(shares_query[0]["shares"])

        if current_shares < shares:
            return apology("Sorry, you don't own that many stocks in the company")

        cash_query = db.execute("SELECT * FROM users WHERE id = :user_id",
                                user_id=session["user_id"])
        current_cash = float(cash_query[0]["cash"])

        price = lookup(symbol)["price"] * shares
        new_shares = current_shares - shares

        # update number of shares
        db.execute("UPDATE stocks SET shares = :new_shares WHERE user_id = :user_id AND symbol=:symbol",
                   new_shares=new_shares, user_id=session["user_id"], symbol=symbol)

        new_balance = round(current_cash + price, 2)
        # update user's balance (current_cash + price)
        db.execute("UPDATE users SET cash = :new_balance WHERE id = :user_id", new_balance=new_balance, user_id=session["user_id"])

        # update history table

        db.execute("INSERT INTO history(user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)", user_id=session["user_id"],
                   symbol=symbol, shares=shares * (-1), price=float(price))

        # flash sold message and redirect user to the homepage
        flash("Sold!")
        return render_template("index.html")
    else:
        stocks = db.execute("SELECT symbol FROM stocks WHERE user_id=:user_id",
                            user_id=session["user_id"])
        return render_template("sell.html", stocks=stocks)

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
        return redirect("index.html")



    else:
        return render_template("change_password.html")

    return (apology("TODO"))

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
