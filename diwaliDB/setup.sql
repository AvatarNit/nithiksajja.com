-- run this file by typing sqlite3 -cmd ".read setup.sql" from your terminal

.open project.db
.mode box


-- drop the tables
DROP TABLE IF EXISTS tables;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS history;
-- create your tables
CREATE TABLE IF NOT EXISTS tables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tableNum INTEGER NOT NULL,
    totalSeats INTEGER DEFAULT 10,
    people TEXT DEFAULT "",
    arrived TEXT DEFAULT ""
);
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    passwords TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aName TEXT NOT NULL,
    action TEXT NOT NULL,
    tableNum INTEGER NOT NULL
);
-- add some starter data to your tables using INPUT statemtns
INSERT INTO tables (tableNum, people, arrived) VALUES (1, "aang,katara,sokka,toph beifong,zuko,suki,appa,momo,iroh,ursa", "appa,momo");
INSERT INTO admins (username, passwords) VALUES ("NITHIK", "704090");
INSERT INTO history (aName, action, tableNum) VALUES ("NITHIK", "Create",1);
-- show all the starter data
SELECT * FROM tables;
SELECT * FROM admins;
SELECT * FROM history;
