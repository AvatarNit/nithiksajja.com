import json
# this function returns a list of dictionaries with all the table information
def get_tables():
    with open("table.json", "r") as table_file:
        tables = json.load(table_file)
    if not tables:
        tables = []
    return tables

def load_tables(table):
    with open("table.json", "w") as my_file:
        json.dump(table, my_file, indent=2)


# this function wil filter by name and return a dictionary with the table info
def get_table_info_by_name(name):
    tables = get_tables()
    found=False
    tableId = None
    for table in tables:
        if name.lower() in table["notChecked"]:
            tables[table["id"]-1]["checked"].append(name.lower())
            tables[table["id"]-1]["notChecked"].remove(name.lower())
            found = True
            tableId = table
            break
    if found == True:
        load_tables(tables)
        return table
    elif found == False:
        return None


# this function wil filter by name and return a dictionary with the table info
def get_table_info_by_id(id):
    tables = get_tables()
    return tables[id-1]
