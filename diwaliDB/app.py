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
    # return q.get_admin_info()
    return render_template("index.html")


# Table Related Routes

@app.route("/createTable")
def createTable():
    return render_template("createTb.html")

@app.route("/view", methods=["GET","POST"])
def view():
    if request.method == "POST":
        if request.form.get("action") == "C":
            tableNum = request.form.get("tableNum")
            seatsNum = request.form.get("seatsNum")
            people=""
            for i in range(1,10):
                if request.form.get(f"p{i}", False):
                    people = people + "," + request.form.get(f"p{i}").lower()
            result = q.createTable(tableNum, seatsNum, people)
            if result:
                flash(f"Table {tableNum} was successfully added", "success")
                focusNum = result
                q.add_history(session.get("name"),"Create",tableNum)
            else:
                flash(f"ERROR: Table {tableNum} was not added", "error")
                return redirect("/createTable")
        elif request.form.get("action") == "D":
            tableNum = request.form.get("tableNum") + ""
            aName = request.form.get("aName")
            tableId = request.form.get("tableId")
            table = q.get_table_by_id(tableId)
            if (tableNum == str(table["tableNum"])) and (aName == session.get("name")):
                if q.delete_table_by_id(tableId):
                    flash(f"Table {tableNum} was deleted by {session.get('name')}", "success")
                    q.add_history(session.get("name"),"Delete",tableNum)
                else:
                    flash(f"ERROR: Table {table['tableNum']} was not deleted", "error")
            else:
                flash(f"ERROR: Table {table['tableNum']} was not deleted Wrong Information", "error")
        elif request.form.get("action") == "E":
            tableNum = request.form.get("tableNum")
            seatsNum = request.form.get("seatsNum")
            people=""
            arrived=""
            id=request.form.get("id")
            for i in range(1,11):
                if request.form.get(f"p{i}", False):
                    people = people + "," + request.form.get(f"p{i}").lower()
                    if request.form.get(f"switch{i}", False):
                        arrived = arrived +"," + request.form.get(f"p{i}").lower()
            if q.editTable(tableNum, seatsNum, people, arrived, id):
                flash(f"Table {tableNum} was successfully edited", "success")
                focusNum = int(id)
                q.add_history(session.get('name'),"Edit",tableNum)
            else:
                flash(f"ERROR: Table {tableNum} was not edited", "error")
                return redirect("/createTable")
        elif request.form.get("action") == "L":
            name = request.form.get("name").lower()
            tableId = q.checkIn_by_id(name)
            if tableId:
                focusNum = tableId
                flash(f"Welcome {name.title()}", "success")
            else:
                flash(f"ERROR: {name.title()} was not found", "error")
                return redirect("/checkIn")


    tableInfo = q.get_table_info()
    tableCount = q.get_table_count()
    for i in tableInfo:
        i["people"] = list(i["people"].split(","))
        i["arrived"] = list(i["arrived"].split(","))
        if i["people"][0] == "":
            del i["people"][0]
    try:
        return render_template("view.html", tableInfo=tableInfo, tableCount=tableCount, focusNum = focusNum)
    except:
        return render_template("view.html", tableInfo=tableInfo, tableCount=tableCount)

@app.route("/edit/<int:id>")
def edit(id):
    table = q.get_table_by_id(id)
    table["people"] = list(table["people"].split(","))
    table["arrived"] = list(table["arrived"].split(","))
    del table["people"][0]
    return render_template("edit.html", table=table)

@app.route("/delete/<int:id>")
def delete(id):
    table = q.get_table_by_id(id)
    return render_template("delete.html", table=table)


@app.route("/checkIn")
def checkIn():
    return render_template("checkIn.html")

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


