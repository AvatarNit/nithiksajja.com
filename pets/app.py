from flask import Flask, render_template, request
import pets as fps

app = Flask(__name__)

TYPES = ["dog", "cat", "reptile", "rabbit", "mouse"]
SERVICES = ["grooming", "boarding", "training", "agility","check-ups"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("registration.html", pet_types=TYPES, services=SERVICES)


@app.route("/success", methods=["POST"])
def success():
    # first grab the data that the user entered
    owner = request.form.get("owner")
    if not owner:
        msg = "No Owner Name Entered"
        return render_template("error.html", msg=msg, href="/registration")

    pet = request.form.get("pet")
    if not pet:
        msg = "Please tell us your pet's name"
        return render_template("error.html", msg=msg, href="/registration")

    pet_type = request.form.get("pet-type")
    if pet_type not in TYPES:
        msg = f"Sorry we do not work with {pet_type}s at this time."
        return render_template("error.html", msg=msg, href="/registration")
    services = request.form.getlist("service")

    # create dict to hold pet info
    pet_dict = {
        "owner":owner.title(),
        "pet": pet.title(),
        "type": pet_type.title(),
        "services" : services
    }
    ind = request.form.get("ind")
    if ind: # this came from /edit route
        updated_info = fps.update_pet(int(ind),pet_dict)
        return render_template("success.html", owner_name=updated_info["owner"], pet_name=updated_info["pet"], pet_type=updated_info["type"])

    # now add this dict to the json file
    fps.add_pet(pet_dict)

    # Now show success message page passing in the owner and pet names
    return render_template("success.html", owner_name=owner, pet_name=pet, pet_type=pet_type)

@app.route("/show")
def show():
    all_pets = fps.load_pets()
    return render_template("show.html", all_pets=all_pets)



@app.route("/grooming")
def grooming():
    return render_template("grooming.html", grooming_pets=fps.grooming_pets())

# Ind is a variable in the route
@app.route("/edit/<int:ind>")
def edit(ind):
    all_pets= fps.load_pets()

    return render_template("edit.html", pet_info=all_pets[ind], pet_types=TYPES, services=SERVICES, index=ind)

# Ind is a variable in the route
@app.route("/confirm-delete/<int:ind>")
def confirmdelete(ind):

    return render_template("confirm-delete.html", index=ind)

# Ind is a variable in the route
@app.route("/delete", methods=["POST"])
def delete():
    all_pets= fps.load_pets()

    index = request.form.get("ind")
    current_pet=all_pets[int(index)]

    owner = request.form.get("owner")
    if not owner:
        msg = "No Owner Name Entered"
        return render_template("error.html", msg=msg, href="/registration")

    pet = request.form.get("pet")
    if not pet:
        msg = "Please tell us your pet's name"
        return render_template("error.html", msg=msg, href="/registration")

    if current_pet["owner"] == owner and current_pet["pet"] == pet:
        fps.delete_pet(index)
        return render_template("delete.html", pet_name=pet)
    else:
        msg = "Wrong information provided"
        return render_template("error.html", msg=msg, href="/show")

