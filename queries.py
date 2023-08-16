""" 

This file is a separation for queries related to excercises and workout plans.

"""

import sqlite3
from helpers import dict_factory
from flask import redirect, render_template, session


# Configure sqlite database connection
connection = sqlite3.connect("database.db", check_same_thread=False)
connection.row_factory = dict_factory

db = connection.cursor()


# Query get methods

def getLastCreatedPlan():
    temp = db.execute("""
                            SELECT * FROM plans
                            WHERE user_id=?
                            ORDER BY id DESC
                            LIMIT 1;
                """, (session["user_id"],))
    return temp.fetchone()
                

def getPlanDetails():
    temp = db.execute("""
                WITH exc AS (
                SELECT id AS exercise_id, name, muscle_group, instructions, equipement_id FROM excercises
                ),
                primary_muscles AS (
                SELECT exc_primary_rel.exc_id AS exc_id, muscles.name AS primary_muscle FROM exc_primary_rel
                LEFT JOIN muscles
                ON exc_primary_rel.muscle_id = muscles.id
                ),
                secondary_muscles AS (
                SELECT exc_secondary_rel.exc_id AS sec_exc_id, muscles.name AS secondary_muscle FROM exc_secondary_rel
                LEFT JOIN muscles
                ON exc_secondary_rel.muscle_id = muscles.id
                )
                SELECT * FROM plan_details
                LEFT JOIN exc
                ON plan_details.exc_id = exc.exercise_id
                LEFT JOIN primary_muscles
                ON exc.exercise_id = primary_muscles.exc_id
                LEFT JOIN secondary_muscles
                ON exc.exercise_id = secondary_muscles.sec_exc_id
                WHERE plan_details.plan_id = ?;
            """, (session["lastActivePlan"],))
    return temp.fetchall()


def getExercises():
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
    return temp.fetchall()

def getActivePlanName():
    temp = db.execute("SELECT name FROM plans WHERE id=?", (session["lastActivePlan"],)).fetchone()

    if temp == None:
        temp = getLastCreatedPlan()

    name = temp['name']
    return name


def getMuscles():
    temp = db.execute("SELECT * FROM muscles;")
    return  temp.fetchall()

def getPlans():
    temp = db.execute('SELECT * FROM plans WHERE user_id=?', (session["user_id"],))
    
    return temp.fetchall()

def getPlanDetailsRow(id):
    temp = db.execute("""
        SELECT * FROM plan_details WHERE id=?
    """, (id,))
    
    return temp.fetchall()


# Query set methods

def setNewPlan(name):
    db.execute("""
                            INSERT INTO plans (name, user_id)
                            VALUES( ?, ? )
                    """, (name, session["user_id"]))

    connection.commit()
    return "New plan created."

def addExercise(selectedExcId, set_count, rep_count, weight, duration):
    db.execute("""
        INSERT INTO plan_details (exc_id, plan_id, set_count, rep_count, weight, duration)
        VALUES(?, ?, ?, ?, ?, ?)
    """, (selectedExcId, session['lastActivePlan'], set_count, rep_count, weight, duration))

    connection.commit()
    return "Exercise added."

def addExcToPlanExecution(plan_id, plan_start_date, plan_start_time, exc_id, set_number,
                                    rep_count, weight, duration):
    db.execute("""
        INSERT INTO plan_execution (plan_id, date, plan_start_time, exc_id, set_number,
                                    rep_count, weight, duration, user_id)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (plan_id, plan_start_date, plan_start_time, exc_id, set_number,
                                    rep_count, weight, duration, session.get("user_id")))
    
    connection.commit()
    return "Set added"

def incrementSet(excId):
    db.execute("""
    UPDATE plan_details
    SET set_count=set_count+1
    WHERE plan_id=?
    AND exc_id=?
    """,(session["lastActivePlan"], excId))
    
    connection.commit()
    return "Set count incremented"


# Query Delete methods

def deletePlan(planId):
    db.execute("""
            DELETE FROM plan_details
            WHERE plan_id=?
    """, (planId,))

    db.execute("""
            DELETE FROM plans
            WHERE id=?
    """, (planId,))

    connection.commit()
    return "Plan deleted."

def deleteExc(excId):
    db.execute("""
        DELETE FROM plan_details
        WHERE plan_id=? AND exc_id=?;
    """, (session["lastActivePlan"], excId))
            
    connection.commit()


