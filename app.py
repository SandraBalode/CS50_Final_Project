import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date
import sqlite3
from sqlite3 import Error
from helpers import apology, login_required, usd, dict_factory

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure sqlite database
connection = sqlite3.connect("database.db", check_same_thread=False)
connection.row_factory = dict_factory

db = connection.cursor()

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

   return apology("TO-DO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Redirect to register, if register was pressed
        if request.form.get("register") == "register":
            return redirect("/register")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")]).fetchall()

        print(request.form.get("username"))
        print(rows)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
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
    if request.method == "POST":

        # Ensure username is entered
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password is entered
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure username does not already exist
        temp = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = temp.fetchall()
        if len(rows) == 1:
            return apology("Choose a different username", 400)

        # Ensure password confirmation matches password
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("confirmation does not match password", 400)

        # Insert the new user data into users
        username = request.form.get("username")
        hashed_psw = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, password) VALUES (?, ?);", (username, hashed_psw))
        connection.commit()

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/my_workouts", methods=["GET", "POST"])
def my_workouts():

    length = 0
    return render_template("my_workouts.html", length=length)


@app.route("/excercises", methods=["GET", "POST"])
def excercises():

    temp = db.execute(
                """
                WITH primary_muscles AS (
                SELECT exc_primary_rel.exc_id AS exc_id, muscles.name AS primary_muscle FROM exc_primary_rel
                LEFT JOIN muscles
                ON exc_primary_rel.muscle_id = muscles.id
                ),
                secondary_muscles AS (
                SELECT exc_secondary_rel.exc_id AS exc_id, muscles.name AS secondary_muscle FROM exc_secondary_rel
                LEFT JOIN muscles
                ON exc_secondary_rel.muscle_id = muscles.id
                )
                SELECT * FROM excercises
                LEFT JOIN primary_muscles
                ON excercises.id = primary_muscles.exc_id
                LEFT JOIN secondary_muscles
                ON excercises.id = secondary_muscles.exc_id
                ORDER BY excercises.name;
                """)
    excercises = temp.fetchall()
    length = len(excercises)

    temp = db.execute("SELECT * FROM muscles;")
    muscles = temp.fetchall()

    return render_template("excercises.html", length=length, excercises=excercises, muscles=muscles)
