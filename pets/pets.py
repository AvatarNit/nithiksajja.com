# Handel all the data stuff for our pets app
import json

# this function will load all the pets from the json file


def load_pets():
    with open("registered.json", "r") as my_file:
        pets = json.load(my_file)

    if not pets:
        pets = []
    return pets

# This function will add a new
def add_pet(pet_dict):
    # load pets from json
    pets = load_pets()
    # add to the list
    pets.append(pet_dict)
    # now update the json file
    with open("registered.json" , "w") as my_file:
        json.dump(pets, my_file, indent=2)


def grooming_pets():
    grooming_pets = []
    pets = load_pets()
    for pet in pets:
        if "grooming" in pet["services"]:
            grooming_pets.append(pet)
    return grooming_pets

# This function wil update the json wityh new info for a specific pet
# new_info is the updated pet dict
def update_pet(ind, new_info):
    all_pets = load_pets() # gets the full list
    all_pets[ind].update(new_info) # updates a specific dict
    # now resave the full list
    with open("registered.json", "w") as my_file:
        json.dump(all_pets, my_file, indent=2)
    return all_pets[ind]

def delete_pet(ind):
    all_pets = load_pets()
    pet = ""
    try:
        pet = all_pets[int(ind)]
    except IndexError:
        pet = -1

    if pet != -1:
        all_pets.pop(int(ind))
    with open("registered.json", "w") as my_file:
        json.dump(all_pets, my_file, indent=2)

