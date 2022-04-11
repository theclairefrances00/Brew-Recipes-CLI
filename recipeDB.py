import sqlite3

# -------------------------------- SQL --------------------------------
# Create tables
CREATE_RECIPE_TABLE = """CREATE TABLE IF NOT EXISTS recipes (recipe_id INTEGER PRIMARY KEY, name TEXT,
                         description TEXT, abv TEXT, recipe_type TEXT);"""

CREATE_INGREDIENTS_TABLE = """CREATE TABLE IF NOT EXISTS ingredients (ingredient_id INTEGER PRIMARY KEY, name TEXT);"""

CREATE_QUANTITIES_TABLE = """CREATE TABLE IF NOT EXISTS quantitites (quantity_id INTEGER PRIMARY KEY, quantity TEXT);"""

CREATE_UNITS_TABLE = """CREATE TABLE IF NOT EXISTS units (unit_id INTEGER PRIMARY KEY, unit TEXT);"""

CREATE_RECIPE_INGREDIENTS_TABLE = """CREATE TABLE IF NOT EXISTS recipe_ingredients (recipe_ingredient_id INTEGER PRIMARY KEY,
                                     recipe_id INT, ingredient_id INT, quantity_id INT, unit_id INT,
                                     FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),
                                     FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id),
                                     FOREIGN KEY(quantity_id) REFERENCES quantities(quantity_id),
                                     FOREIGN KEY(unit_id) REFERENCES untis(unit_id));"""

# Insert
INSERT_RECIPE = """INSERT INTO recipes (name, description, abv, recipe_type) VALUES (?,?,?,?);"""
INSERT_INGREDIENT = """INSERT INTO ingredients (name) VALUES (?);"""
INSERT_QUANTITY = """INSERT INTO quantitites (quantity) VALUES (?);"""
INSERT_UNIT = """INSERT INTO units (unit) VALUES (?);"""
INSERT_RECIPE_INGREDIENT = """INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity_id, unit_id)
    VALUES (?,?,?,?);"""


# Check if exists
RECIPE_EXISTS = """SELECT 1 FROM recipes WHERE name = ?;"""
INGREDIENT_EXISTS = """SELECT 1 FROM ingredients WHERE name = ?;"""
QUANTITY_EXISTS = """SELECT 1 FROM quantitites WHERE quantity = ?;"""
UNIT_EXISTS = """SELECT 1 FROM units WHERE unit = ?;"""


GET_RECIPE_NAMES = """SELECT name FROM recipes;"""
GET_INGREDIENTS_IN_RECIPE= """SELECT ingredients.name FROM recipes
INNER JOIN recipe_ingredients ON recipe_ingredients.recipe_id = recipes.recipe_id
INNER JOIN ingredients ON ingredients.ingredient_id = recipe_ingredients.ingredient_id
INNER JOIN quantitites ON quantitites.quantity_id = recipe_ingredients.quantity_id
INNER JOIN units ON units.unit_id = recipe_ingredients.unit_id
where recipes.name=?;"""

# Get ID
GET_RECIPE_ID_BY_NAME = """SELECT recipe_id FROM recipes WHERE name = ?;"""
GET_INGREDIENT_ID_BY_NAME = """SELECT ingredient_id FROM ingredients WHERE name = ?;"""
GET_QUANTITY_ID_BY_NAME = """SELECT quantity_id FROM quantitites WHERE quantity = ?;"""
GET_UNIT_ID_BY_NAME = """SELECT unit_id FROM units WHERE unit = ?;"""

DELETE_RECIPE_BY_NAME = "DELETE FROM recipes WHERE name = ?;"


# -------------------------------- Functions --------------------------------
#create a connection to a db. If db doesn't exits this creates it
def connect():
    return sqlite3.connect('data.db')

#create tables if they don't exist
def create_tables(connection):
    with connection:
        connection.execute(CREATE_RECIPE_TABLE)
        connection.execute(CREATE_RECIPE_INGREDIENTS_TABLE)
        connection.execute(CREATE_INGREDIENTS_TABLE)
        connection.execute(CREATE_QUANTITIES_TABLE)
        connection.execute(CREATE_UNITS_TABLE)

#add 
def add_recipe(connection, name, description, abv, recipe_type):
    with connection:
        connection.execute(INSERT_RECIPE, (name, description, abv, recipe_type))

def add_ingredient(connection, name):
    with connection:
        connection.execute(INSERT_INGREDIENT, (name,))

def add_quantity(connection, quantity):
    with connection:
        connection.execute(INSERT_QUANTITY, (quantity,))

def add_unit(connection, unit):
    with connection:
        connection.execute(INSERT_UNIT, (unit,))
        
def add_to_rel_table(connection, recipe_id, ingredient_id,quantity_id, unit_id):
    with connection:
        connection.execute(INSERT_RECIPE_INGREDIENT, (recipe_id, ingredient_id, quantity_id, unit_id,))
        
# Get recipes
def get_recipe_ingredients(connection,name):
    with connection:
        return connection.execute(GET_INGREDIENTS_IN_RECIPE, [name]).fetchall()
def get_recipe_names(connection):
    with connection:
        return connection.execute(GET_RECIPE_NAMES).fetchall()
# Get IDs
def get_recipe_id_by_name(connection, name):
    with connection:
        return connection.execute(GET_RECIPE_ID_BY_NAME, (name,)).fetchone()

def get_ingredient_id_by_name(connection, name):
    with connection:
        return connection.execute(GET_INGREDIENT_ID_BY_NAME, (name,)).fetchone()

def get_quantity_id_by_name(connection, quantity):
    with connection:
        return connection.execute(GET_QUANTITY_ID_BY_NAME, (quantity,)).fetchone()

def get_unit_id_by_name(connection, unit):
    with connection:
        return connection.execute(GET_UNIT_ID_BY_NAME, (unit,)).fetchone()

# Check if exists
def recipe_exists(connection, name):
    with connection:
        return connection.execute(RECIPE_EXISTS, (name,)).fetchall()

def ingredient_exists(connection, name):
    with connection:
        return connection.execute(INGREDIENT_EXISTS, (name,)).fetchall()

def quantity_exists(connection, quantity):
    with connection:
        return connection.execute(QUANTITY_EXISTS, (quantity,)).fetchall()

def unit_exists(connection, unit):
    with connection:
        return connection.execute(UNIT_EXISTS, (unit,)).fetchall()
    
# Delete
def delete_recipe_by_name(connection,name):
    with connection:
        return connection.execute(DELETE_RECIPE_BY_NAME, (name,)).fetchall()

