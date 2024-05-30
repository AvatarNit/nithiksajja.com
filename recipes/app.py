from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
import queries as q

app = Flask(__name__)
app.secret_key = "secretcode1234"

# Configure Session
app.config["SESSION_PERMENANT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

# General Routes

@app.route("/", methods=["GET","POST"])
def index():
    return render_template("index.html")