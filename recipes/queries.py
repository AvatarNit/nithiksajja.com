from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash

db = SQL("sqlite:///recipes.db")

# General Functions

def split_list(lst, chunk_size):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

# Recipes Database

def get_display_info():
    sql = """SELECT name,description,picName FROM recipes"""
    result = db.execute(sql)
    # for i in range(0,10):
    #     result.append(i)
    return split_list(result,4)


# Admin Database

def get_admin_info():
    sql = """SELECT * FROM admins"""
    return db.execute(sql)

def login(name, password):
    adminInfo = get_admin_info()
    for i in range(len(adminInfo)):
        if adminInfo[i]["username"] == name and adminInfo[i]["passwords"] == password:
            return True
    return False

def addAccount(name,password):
    sql="""INSERT INTO admins (username, passwords) VALUES (?,?)"""
    return db.execute(sql,name,password)

def get_admin_info_by_id(id):
    sql="""SELECT * FROM admins WHERE id=?"""
    return db.execute(sql,id)[0]

def editAccount(name,password,id):
    sql="""UPDATE admins SET username=?, passwords=? WHERE id=?"""
    return db.execute(sql,name,password,id)

def delete_acc_by_id(id):
    sql="""DELETE FROM admins WHERE id=?"""
    return db.execute(sql,id)

# History Database

def get_history():
    sql="""SELECT * FROM history"""
    return db.execute(sql)

def get_history_by_name(name):
    sql="""SELECT * FROM history WHERE aName=?"""
    return db.execute(sql,name)


def add_history(name,action, msg):
    sql="""INSERT INTO history (aName,action,msg) VALUES (?,?,?)"""
    return db.execute(sql,name,action,msg)
