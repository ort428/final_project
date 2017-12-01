from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
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
db = SQL("sqlite:///maxwell.db")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM history WHERE id = :id", id=session["user_id"])

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

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

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        if not request.form.get("password"):
            return apology("must provide password")

        if not request.form.get("confirmation"):
            return apology("must provide confirmation")

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")

        # Insert username and password into database
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash);", username=request.form.get(
            "username"), hash=generate_password_hash(request.form.get("password")))

        session["user_id"] = result

        if result == None:
            return apology("username already exists")

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Search for rooms"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure search fields are submitted
        if not request.form.get("room_type"):
            return apology("must provide room type")

        if not request.form.get("attendance")
            return apology("must provide attendance")

        if not request.form.get("start_time"):
            return apology("must provide start time")

        if not request.form.get("end_time"):
            return apology("must provide end time")

        result = db.execute("SELECT * FROM max WHERE seating_capacity > :seating_capacity", seating_capacity = request.form.get("seating_capacity"))


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
