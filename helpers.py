import csv
from datetime import datetime, date
import pytz
#import requests
import subprocess
import urllib
import uuid
import sqlite3
from sqlite3 import Error

from flask import redirect, render_template, session
from functools import wraps




def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def createCounter(length):
    session['counterList'] = []
    for i in range(length):
        session['counterList'].append(i)

    session['currentNumber'] = session['counterList'][0]

def incrementCounter():
    if session['currentNumber'] == session['counterList'][-1]:
        session['currentNumber'] = session['counterList'][0]
    else:
        session['currentNumber'] += 1

def decrementCounter():
    if session['currentNumber'] == session['counterList'][0]:
        session['currentNumber'] = session['counterList'][-1]
    else:
        session['currentNumber'] -= 1