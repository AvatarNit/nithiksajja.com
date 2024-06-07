from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_session import Session
import queries as q
import os

app = Flask(__name__)
app.secret_key = "secretcode1234"

# Configure Session
app.config["SESSION_PERMENANT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
UPLOAD_FOLDER = 'static/food'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Session(app)

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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

# Recipe Related Routes

@app.route("/viewRecipes", methods=["GET", "POST"])
def viewRecipes():
    if request.method == "POST":
        filterCategory = request.form.get('category', "Meal Type")
        filterClass = request.form.get("class", "Requirements")
        displayInfo = q.filter(filterCategory, filterClass)
    else:
        displayInfo = q.get_display_info()
        print(displayInfo)
    categories = q.get_categories()
    return render_template("viewRecipes.html", displayInfo=displayInfo, categories=categories)

@app.route("/addRecipe", methods=["GET", "POST"])
def addRecipe():
    if request.method == "GET":
        return render_template("addRecipe.html")
    elif request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        videoUrl = request.form.get("videoUrl", None)
        cookTime = request.form.get("cookTime", None)
        servings = request.form.get("servings", None)
        category = request.form.get("category", None)
        classification = request.form.get("class", None)
        instructions=""
        ingredients=""
        for i in range(1,100):
            if request.form.get(f"instructions-{i}", False):
                instructions = instructions + f"_{i}. " + request.form.get(f"instructions-{i}")
            else:
                break
        for i in range(1,100):
            if request.form.get(f"ingredientsName-{i}", False):
                ingredients = f"{ingredients},{request.form.get('ingredientsNum-' + str(i))}_{request.form.get('ingredientsMeasure-' + str(i))}_{request.form.get('ingredientsName-' + str(i))}"
            else:
                break
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            picName = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(picName)

            if q.addRecipe(name, description, picName, instructions, ingredients, videoUrl, cookTime, servings, category, classification):
                flash(f"Successfully added {name} to the database", "success")
                return redirect("/")


@app.route("/viewRecipe/<name>")
def viewRecipe(name):
    recipe = q.get_recipe_by_name(name)
    current_recipe = session.get('currentRecipe')
    for i in range(0, len(recipe["ingredients"])):
        recipe["ingredients"][i].append(q.get_ingredient_image(recipe["ingredients"][i][-1]))
        recipe["ingredients"][i].insert(0, recipe["ingredients"][i][-2].replace(" ", "_"))
    # return recipe
    return render_template("viewRecipe.html", recipe=recipe, current_recipe=current_recipe)

@app.route('/toggle_favorite', methods=['POST'])
def toggle_favorite():
    data = request.json
    recipe_name = data.get('recipe_name')
    if session.get('currentRecipe') == recipe_name:
        session['currentRecipe'] = None
    else:
        session['currentRecipe'] = recipe_name
    return jsonify(status='success')

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
