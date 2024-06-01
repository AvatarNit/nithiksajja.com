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
    if request.method == "POST":
        result = q.login(request.form.get("name"),request.form.get("pass"))
        if result:
            flash(f"Welcome {request.form.get('name')}, you are successfully logged in", "success")
            session["admin"] = "T"
            session["name"] = request.form.get('name')
            session["password"] = request.form.get("pass")
        else:
            flash(f"ERROR: Wrong information provided please try again", "error")
            return redirect("/admin")
    displayInfo = q.get_display_info()
    return render_template("index.html", displayInfo=displayInfo)


# History Related routes

@app.route("/history")
def history():
    history = q.get_history()
    reHistory = history[::-1]
    return render_template("history.html", history=reHistory)

@app.route("/adminHistory/<int:id>")
def adminHistory(id):
    adminInfo = q.get_admin_info_by_id(id)
    history = q.get_history_by_name(adminInfo["username"])
    return render_template("history.html", history=history)

# Admin Account Related Routes

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/logout")
def logout():
    name=session.get("name")
    session.clear()
    flash(f"Successfully Logged Out { name }", "success")
    return redirect("/")

@app.route("/addAcc")
def addAcc():
    return render_template("addAcc.html")

@app.route("/viewAcc", methods=["GET","POST"])
def viewAcc():
    if request.method == "POST":
        if request.form.get("action") == "A":
            name = request.form.get("name")
            password = request.form.get("pass")
            if q.addAccount(name,password):
                flash(f"Successfully created account for { name }", "success")
            else:
                flash(f"ERROR: Account for { name } was not created", "error")
                return redirect("/addAcc")
        elif request.form.get("action") == "E":
            name = request.form.get("name")
            password = request.form.get("pass")
            id = request.form.get("id")
            if q.editAccount(name,password,id):
                flash(f"Successfully saved changes for { name }'s account", "success")
            else:
                flash(f"ERROR: Changes for { name }'s account were not saved", "error")
        elif request.form.get("action") == "D":
            accName = request.form.get("accName") + ""
            aName = request.form.get("aName")
            id = request.form.get("id")
            adminInfo = q.get_admin_info_by_id(id)
            if (accName == adminInfo["username"]) and (aName == session.get("name")):
                if q.delete_acc_by_id(id):
                    flash(f"Account {accName} was deleted by {session.get('name')}", "success")
                else:
                    flash(f"ERROR: Account {accName} was not deleted", "error")
            else:
                flash(f"ERROR: Account {accName} was not deleted Wrong Information", "error")

    adminInfo = q.get_admin_info()
    return render_template("viewAcc.html", adminInfo=adminInfo)

@app.route("/editAcc/<int:id>")
def editAcc(id):
    adminInfo = q.get_admin_info_by_id(id)
    return render_template("editAcc.html", adminInfo=adminInfo)

@app.route("/delAcc/<int:id>")
def delAcc(id):
    adminInfo = q.get_admin_info_by_id(id)
    return render_template("delAcc.html", adminInfo=adminInfo)
