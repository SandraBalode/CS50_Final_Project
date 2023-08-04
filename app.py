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

    # if this is the first time in this session then set last created as default value
    if not session["lastActivePlan"]:
        temp = db.execute("""
                            SELECT id FROM plans
                            WHERE user_id=?
                            ORDER BY id DESC
                            LIMIT 1;
                """, (session["user_id"],))
        lap = temp.fetchone()
        session['lastActivePlan'] = lap['id']


    if request.method == "POST":
        form_data = request.form

        """ logic for createPlan and delete plan buttons """
        if 'submitBtn' in form_data:
            button_value = form_data['submitBtn']

            if button_value == 'createPlan':
                new_plan_name = request.form.get('plan-name')

                if new_plan_name:
                    # Only proceed with insertion if new_plan_name is not empty
                    db.execute("""
                            INSERT INTO plans (name, user_id)
                            VALUES( ?, ? )
                    """, (new_plan_name, session["user_id"]))

                connection.commit()
                
                #set a new lastActive plan
                temp = db.execute("""
                            SELECT id FROM plans
                            WHERE user_id=?
                            ORDER BY id DESC
                            LIMIT 1;
                """, (session["user_id"],))
                lap = temp.fetchone()
                session['lastActivePlan'] = lap['id']
                
                return redirect("/my_workouts")
            
            if button_value == 'deletePlan':
                to_delete_plan = request.form.get('plans')
                db.execute("""
                        DELETE FROM plan_details
                        WHERE plan_id=?
                """, (to_delete_plan,))

                db.execute("""
                        DELETE FROM plans
                        WHERE id=?
                """, (to_delete_plan,))

                connection.commit()
                return redirect("/my_workouts")
            

            if button_value == 'addExc':

                selectedExcId = request.form.get('excOptions')
                set_count = request.form.get('setCount')

                rep_count = request.form.get('repCount')
                if rep_count is None:
                    print('rep_count is none')
                    rep_count = None

                weight = request.form.get('weight')
                if weight is None:
                    weight = None

                duration = request.form.get('duration')
                if duration is None:
                    duration = None

                db.execute("""
                        INSERT INTO plan_details (exc_id, plan_id, set_count, rep_count, weight, duration)
                        VALUES(?, ?, ?, ?, ?, ?)
                    """, (selectedExcId, session['lastActivePlan'], set_count, rep_count, weight, duration))

                connection.commit()
                return redirect("/my_workouts")
            
        
        if 'selectPlanBtn' in form_data:
            
            session["lastActivePlan"] = form_data['selectPlanBtn']

            return redirect("/my_workouts")
        

        if 'removeExc' in form_data:
            
            excToRemove = form_data['removeExc']
            db.execute("""
                    DELETE FROM plan_details
                    WHERE plan_id=? AND exc_id=?;
                """, (session["lastActivePlan"], excToRemove))
            
            connection.commit()            
            return redirect("/my_workouts")



    
    # Querry for list of plans
    temp = db.execute('SELECT * FROM plans WHERE user_id=?', (session["user_id"],))
    plans = temp.fetchall()
    length = len(plans)


    # Querry for currently active plans details
    temp = db.execute("""
                WITH exc AS (
                SELECT * FROM excercises
                )
                SELECT * FROM plan_details
                LEFT JOIN exc
                ON plan_details.exc_id = exc.id
                WHERE plan_details.plan_id = ?;
            """, (session["lastActivePlan"],))
    plan_details = temp.fetchall()
    exc_count = len(plan_details)
    
    temp = db.execute("SELECT name FROM plans WHERE id=?", (session["lastActivePlan"],))
    activePlanName = temp.fetchone()
    
    temp = db.execute("SELECT * FROM muscles;")
    muscles = temp.fetchall()

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
    exercises = temp.fetchall()


    return render_template("my_workouts.html", plans=plans, length=length, exc_count=exc_count, 
                           plan_details=plan_details, activePlanName=activePlanName['name'], 
                           muscles=muscles, exercises=exercises)


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
