from flask import Flask, request, render_template, redirect
import queries as q

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/checkin", methods=["GET", "POST"])
def checkin():
    if request.method == "GET":
        return render_template("checkin.html")
    elif request.method == "POST":
        name = request.form.get("name")
        tableInfo = q.get_table_info_by_name(name) #returns a dictionary of table info if not found returns None
        if tableInfo is not None:
            return render_template("checked.html",tableInfo=tableInfo)
        else:
            return render_template("error.html", error="Table Was Not found")

@app.route("/table", methods=["GET", "POST"])
def table():
    count=30
    if request.method == "GET":
        return render_template("table.html", count=count)
    elif request.method == "POST":
        id = request.form.get("table_id")
        id = int(id)
        tableInfo = q.get_table_info_by_id(id)
        return render_template("display.html", tableInfo=tableInfo, admin=False)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    count=30
    if request.method == "GET":
        return render_template("tableA.html", count=count)
    elif request.method == "POST":
        id = request.form.get("table_id")
        id = int(id)
        tableInfo = q.get_table_info_by_id(id)
        return render_template("display.html", tableInfo=tableInfo, admin=True)

@app.route("/success/<int:id>", methods=["POST"])
def success(id):
    tables = q.get_tables()
    tables[id-1]["checked"] = []
    tables[id-1]["notChecked"] = tables[id-1]["people"].copy() 
    for i in tables[id-1]["people"]:
        if request.form.get(i) == "on":
            tables[id-1]["checked"].append(i)
            tables[id-1]["notChecked"].remove(i)
    q.load_tables(tables)
    return redirect("/table")