import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

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
    # stores needed variables from database in a dictionary
    stock = db.execute(
        "SELECT stock_symbol, stock_name, SUM(number_of_shares) as stock_number FROM purchases GROUP BY stock_name HAVING id = :user_id", user_id=session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

    # initializing price and total lists
    current_price = []
    current_total = []
    total = 0

    # iterates over dictionary combined with lookup function to get current pricing and total on stocks, then updates lists
    for i in stock:
        current_price.append(round(lookup(i["stock_symbol"])["price"], 2))
        current_total.append(i["stock_number"] * round(lookup(i["stock_symbol"])["price"], 2))

    # calculated length of lists
    length = len(current_price)

    # calculates total worth of stocks
    total = sum(current_total)

    return render_template("index.html", current_price=current_price, total=total, stock=stock, current_total=current_total, length=length, cash_remaining=cash[0]["cash"])


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":

        # get info from user
        share_bought = lookup(request.form.get("symbol"))
        number_of_shares_bought = (request.form.get("shares"))

        # checks to see if user input data correctly
        if not share_bought or not number_of_shares_bought or not str(number_of_shares_bought).isdigit() or float(number_of_shares_bought) <= 0 or float(number_of_shares_bought) * 10 % 10 != 0:
            return apology("Please make sure information entered is correct", 400)

        # calculates relevant info
        else:
            stock_price = round((share_bought["price"]), 2)
            stock_cost = (stock_price * int(number_of_shares_bought))
            cash_info = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
            cash = cash_info[0]["cash"]

            # verify that there is enough funds
            if cash < stock_cost:
                return apology("Not enough funds for transaction", 400)

            # updates database
            else:
                # update database
                db.execute("UPDATE users SET cash = cash - :stock_cost WHERE id = :user_id",
                           stock_cost=stock_cost,  user_id=session["user_id"])
                db.execute("INSERT INTO purchases (id, stock_name, stock_symbol, number_of_shares, stock_price, date_of_transaction, bought_or_sold) VALUES (:user_id, :stock_name, :stock_symbol, :number_of_shares_bought, :stock_price, :date_of_transaction, :bought_or_sold)",
                           user_id=session["user_id"], stock_name=share_bought["name"], stock_symbol=share_bought["symbol"], number_of_shares_bought=number_of_shares_bought, stock_price=share_bought["price"], date_of_transaction=datetime.now(), bought_or_sold="buy")

                # sends user to index
                return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    # gets username via get
    username = request.args.get("username")
    data_containing_username = db.execute("SELECT username FROM users WHERE username = :username", username=username)
    # checks to see if username is taken and is appropriate length
    if data_containing_username == [] and len(username) > 0:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():

     # render index
    history = db.execute("SELECT * FROM purchases WHERE id = :user_id", user_id=session["user_id"])

    return render_template("history.html", history=history, message="Here is a history of your transactions")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Changes user's password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("new_password_confirmation"):
            return apology("must provide new password confirmation", 405)

        # Ensure password was submitted
        elif not request.form.get("new_password"):
            return apology("must provide password", 406)

         # Ensure password was submitted
        elif not request.form.get("current_password"):
            return apology("must provide current password", 407)

        elif request.form.get("new_password_confirmation") != request.form.get("new_password"):
            return apology("make sure new password and confirmation match", 403)

        # Query database for old hash
        else:
            database_hash = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=session["user_id"])

            # checks to see if old password is correct
            if check_password_hash(database_hash[0]["hash"], request.form.get("current_password")):

                # generates new hash updates hash in database for user
                new_hash = generate_password_hash(request.form.get("new_password"))
                db.execute("UPDATE users SET hash = :new_hash WHERE id = :user_id", new_hash=new_hash,  user_id=session["user_id"])

                # shows success template
                return render_template("success.html", message="You have changed your password")

            else:
                return apology("current password is incorrect", 404)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_password.html")


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
            return apology("invalid username and/or password", 404)

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

    if request.method == "POST":

        # get info from user
        quote = lookup(request.form.get("symbol"))

        if not quote:
            return apology("Please make sure stock symbol is corret", 400)

        # retrieve and display stock information
        else:
            return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # makes sure user inputs all data correctly
        if not request.form.get("username"):
            return apology("please enter a username")

        elif not request.form.get("password"):
            return apology("please enter a password")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")

        # insert data into table
        hash = generate_password_hash(request.form.get("password"))

        user_info = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                               username=request.form.get("username"), hash=hash)

        # checks to see if you username is unique
        if not user_info:
            return apology("username is already taken. please choose a different username")

        # confirms registration
        else:
            # Remember which user has logged in
            session["user_id"] = user_info

            return render_template("success.html", message="You are registered")

    elif request.method == "GET":

        return render_template("register.html")


@app.route("/add_funds", methods=["GET", "POST"])
@login_required
def add_funds():
    """Adds funds to portfolio"""

    if request.method == "POST":
        cash_added = request.form.get("add_funds")

        if not cash_added or not str(cash_added).isdigit() or float(cash_added) <= 0 or float(cash_added) * 100 % 10 != 0:
            return apology("Please make sure cash is entered as USD", 400)

        db.execute("UPDATE users SET cash = cash + :cash_added WHERE id = :user_id",
                   cash_added=cash_added,  user_id=session["user_id"])

        return redirect("/")

    else:
        return render_template("add_funds.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stock = db.execute(
        "SELECT stock_symbol, stock_name, SUM(number_of_shares) as stock_number FROM purchases GROUP BY stock_name HAVING id = :user_id", user_id=session["user_id"])

    if request.method == "POST":
        share_sold = lookup(request.form.get("symbol"))
        number_of_shares_sold = (request.form.get("shares"))

        if not share_sold or not number_of_shares_sold or not str(number_of_shares_sold).isdigit() or float(number_of_shares_sold) <= 0 or float(number_of_shares_sold) * 10 % 10 != 0:
            return apology("Please make sure information entered is correct", 400)

        number_of_shares_sold = int(number_of_shares_sold)
        stock_available = db.execute("SELECT SUM(number_of_shares) as stock_number_available FROM purchases WHERE id = :user_id AND stock_name = :share",
                                     user_id=session["user_id"], share=share_sold["name"])

        if number_of_shares_sold > stock_available[0]["stock_number_available"]:
            return apology("Not enough stock", 400)

        revenue_from_sale = number_of_shares_sold * share_sold["price"]

        db.execute("UPDATE users SET cash = cash + :revenue WHERE id = :user_id",
                   revenue=revenue_from_sale,  user_id=session["user_id"])
        db.execute("INSERT INTO purchases (id, stock_name, stock_symbol, number_of_shares, stock_price, date_of_transaction, bought_or_sold) VALUES (:user_id, :stock_name, :stock_symbol, :number_of_shares_sold, :stock_price, :date_of_transaction, :bought_or_sold)",
                   user_id=session["user_id"], stock_name=share_sold["name"], stock_symbol=share_sold["symbol"], number_of_shares_sold=(-number_of_shares_sold), stock_price=share_sold["price"], date_of_transaction=datetime.now(), bought_or_sold="sell")

        return redirect("/")

    else:
        return render_template("sell.html", stock=stock)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
