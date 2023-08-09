import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date
import sqlite3
from sqlite3 import Error
from helpers import apology, login_required, usd, dict_factory
from queries import getPlanDetails, getExercises, getActivePlanName, getMuscles, getPlans
from queries import getLastCreatedPlan, setNewPlan, deletePlan, addExercise, deleteExc
from queries import getPlanDetailsRow, addExcToPlanExecution

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
    if "lastActivePlan" not in session:        
        lastCreatedPlan = getLastCreatedPlan()
        session['lastActivePlan'] = lastCreatedPlan['id']


    if request.method == "POST":
        form_data = request.form

        """ logic for createPlan and delete plan buttons """
        if 'submitBtn' in form_data:
            button_value = form_data['submitBtn']

            if button_value == 'createPlan':
                new_plan_name = request.form.get('plan-name')

                # Only proceed with insertion if new_plan_name is not empty
                if new_plan_name:
                    setNewPlan(new_plan_name)
                
                #set a new lastActive plan            
                lastCreatedPlan = getLastCreatedPlan()
                session['lastActivePlan'] = lastCreatedPlan['id']
                
                return redirect("/my_workouts")
            
            if button_value == 'deletePlan':
                to_delete_plan = request.form.get('plans')
                deletePlan(to_delete_plan)

                return redirect("/my_workouts")
            

            if button_value == 'startWO':

                return redirect('/active_workout')
            

            if button_value == 'addExc':

                selectedExcId = request.form.get('excOptions')
                set_count = request.form.get('setCount')

                rep_count = request.form.get('repCount')
                if rep_count is None:
                    rep_count = None

                weight = request.form.get('weight')
                if weight is None:
                    weight = None

                duration = request.form.get('duration')
                if duration is None:
                    duration = None

                addExercise(selectedExcId, set_count, rep_count, weight, duration)
                return redirect("/my_workouts")
            
        
        if 'selectPlanBtn' in form_data:            
            session["lastActivePlan"] = form_data['selectPlanBtn']

            return redirect("/my_workouts")
        

        if 'removeExc' in form_data:            
            excToRemove = form_data['removeExc']
            deleteExc(excToRemove)       

            return redirect("/my_workouts")


    
    # Querry for list of plans
    plans = getPlans()
    length = len(plans)

    # Querry for currently active plans details
    plan_details = getPlanDetails()
    exc_count = len(plan_details)
    
    activePlanName = getActivePlanName()

    return render_template("my_workouts.html", plans=plans, length=length, exc_count=exc_count, 
                           plan_details=plan_details, activePlanName=activePlanName, 
                           muscles=getMuscles(), exercises=getExercises())


@app.route("/active_workout", methods=["GET", "POST"])
def active_workout():

    if request.method == "POST":
        form_data = request.form

        if 'removeExc' in form_data:            
            excToRemove = form_data['removeExc']
            deleteExc(excToRemove)       

            return redirect("/active_workout")
        
        if 'submitBtn' in form_data:
            button_value = form_data['submitBtn']

            if button_value =='addExc':
                selectedExcId = request.form.get('excOptions')
                set_count = request.form.get('setCount')

                rep_count = request.form.get('repCount')
                if rep_count is None:
                    rep_count = None

                weight = request.form.get('weight')
                if weight is None:
                    weight = None

                duration = request.form.get('duration')
                if duration is None:
                    duration = None

                addExercise(selectedExcId, set_count, rep_count, weight, duration)
                return redirect("/active_workout")
            

            if button_value =='finishExc':
                
                # get date (yyyy-mm-dd) and time (hh:mm:ss)
                plan_start_date = date.today()
                plan_start_time = datetime.now().strftime("%H:%M:%S")

                selected_checks = request.form.getlist('checkBtn')

                # loop through checked sets, add each to plan_execution table
                for set in selected_checks:
                    temp = set.partition('_')
                    plan_details_id = int(temp[0])
                    print(plan_details_id)
                    set_number = temp[2]

                    row = getPlanDetailsRow(plan_details_id)
                    plan_id = row[0]['plan_id']
                    exc_order = request.form.get('exc_order')
                    exc_id = row[0]['exc_id']
                    
                    set_rep_count = request.form.get('rep_count_' + set_number)
                    set_weight = request.form.get('weight_' + set_number)
                    set_duration = request.form.get('duration_' + set_number)


                    addExcToPlanExecution(plan_id, plan_start_date, plan_start_time, exc_order, exc_id, set_number,
                                    set_rep_count, set_weight, set_duration)
                    print('added')

                # should refocus to the next exc after reload
                return redirect("/active_workout")


            if button_value =='finishWO':
                # log the workout info to the history
                # redirect to this workouts generated summary.
                return redirect("/")

    plan_details = getPlanDetails()
    exc_count = len(plan_details)

    return render_template("active_workout.html", activePlanName=getActivePlanName(), exc_count=exc_count, 
                           plan_details=plan_details, exercises=getExercises(), muscles=getMuscles())



@app.route("/excercises", methods=["GET", "POST"])
def excercises():

    exercises = getExercises()
    length = len(getExercises())

    temp = db.execute("SELECT * FROM muscles;")
    muscles = temp.fetchall()

    return render_template("excercises.html", length=length, excercises=exercises, muscles=muscles)
