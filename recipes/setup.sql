
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS ingredients;

CREATE TABLE IF NOT EXISTS recipes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    picName TEXT NOT NULL,
    videoUrl TEXT,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    cookTime INTEGER,
    servings INTEGER,
    category TEXT,
    class TEXT,
    description TEXT NOT NULL
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
    recipeNum INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    picLocation TEXT NOT NULL
);

INSERT INTO recipes (name,picName,videoUrl,ingredients,instructions,cookTime,servings,category,class, description) VALUES ("Lemon Rice", "/static/food/lemon rice/lemon.heic", "https://youtu.be/DVoTi4mve2U?si=ORpf8WDUCEfjxoXC", "1_Cup:Peanuts,5:Chilies,8:Curry Leaves,1_tsp:Jeera,1_tsp:Chana Dal,1_tsp:Mustard Seeds,1_tsp:Urad Dal,1_tsp:Turmeric,Lemon Extract,Salt,2_Cup:Cooked Rice", "1. Break up the rice.,2. Heat oil in a pan.,3. Fry peanuts until golden.,4. Add Chana Dal, Jeera, Mustard Seeds, and Urad Dal. Mix.,5. Add Curry Leaves and Chilies. Mix.,6. Add turmeric. Mix.,7. Add rice. Mix well.,8. Add lemon juice and salt to taste.,9. Enjoy!",15,2,"Breakfast","Veg", "Lemon Rice is a South Indian rice dish with lemon and spices");
INSERT INTO admins (username, passwords) VALUES ("NITHIK", "704090");
INSERT INTO history (aName, action, recipeNum) VALUES ("NITHIK", "Create",1);
INSERT INTO ingredients (name,picLocation) VALUES ("Chana Dal", "/static/ingredients/chana dal.png");
INSERT INTO ingredients (name,picLocation) VALUES ("Chilies", "/static/ingredients/chilies.png");
INSERT INTO ingredients (name,picLocation) VALUES ("Cooked Rice", "/static/ingredients/cooked rice.png");
INSERT INTO ingredients (name,picLocation) VALUES ("Curry Leaves", "/static/ingredients/curry leaves.png");
INSERT INTO ingredients (name,picLocation) VALUES ("Jeera", "/static/ingredients/jeera.png");
INSERT INTO ingredients (name,picLocation) VALUES ("Lemon Extract", "/static/ingredients/lemon extract.png");
INSERT INTO ingredients (name,picLocation) VALUES ("Mustard Seeds", "/static/ingredients/mustard seeds.png");
INSERT INTO ingredients (name,picLocation) VALUES ("Peanuts", "/static/ingredients/peanuts.png");
INSERT INTO ingredients (name,picLocation) VALUES ("Salt", "/static/ingredients/salt.png");
INSERT INTO ingredients (name,picLocation) VALUES ("Turmeric", "/static/ingredients/turmeric.png");
INSERT INTO ingredients (name,picLocation) VALUES ("Urad Dal", "/static/ingredients/urad dal.png");