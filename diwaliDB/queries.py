from cs50 import SQL

db = SQL("sqlite:///project.db")

# Tables Database

def get_table_info():
    sql = """SELECT * FROM tables ORDER BY tableNum"""
    return db.execute(sql)

def createTable(tableNum, seatsNum, people):
    sql = """INSERT INTO tables (tableNum, totalSeats, people) VALUES (?, ?, ?)"""
    return db.execute(sql, tableNum, seatsNum, people)

def get_table_by_id(id):
    sql = """SELECT * FROM tables WHERE id=?"""
    return db.execute(sql,id)[0]

def delete_table_by_id(id):
    sql = """DELETE FROM tables WHERE id=?"""
    return db.execute(sql, id)

def editTable(tableNum, seatsNum, people, arrived,id):
    sql = """UPDATE tables SET tableNum=?, totalSeats=?, people=?, arrived=? WHERE id=?"""
    return db.execute(sql,tableNum, seatsNum, people, arrived,id)

def checkIn_by_id(name):
    tableInfo = get_table_info()
    for i in tableInfo:
        i["people"] = list(i["people"].split(","))
        i["arrived"] = list(i["arrived"].split(","))
    for t in tableInfo:
        if name in t["people"]:
            if name  not in t["arrived"]:
                t["arrived"].append(name)
                sql = """UPDATE tables SET people=?, arrived=? WHERE id=?"""
                db.execute(sql, ",".join(t["people"]), ",".join(t["arrived"]), t["id"])
            return t["id"]
    return False

def get_table_count():
    sql = """SELECT COUNT(DISTINCT tableNum) FROM tables"""
    return db.execute(sql)[0]["COUNT(DISTINCT tableNum)"]

# Admins Database

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


def add_history(name,action,num):
    sql="""INSERT INTO history (aName,action,tableNum) VALUES (?,?,?)"""
    return db.execute(sql,name,action,num)
