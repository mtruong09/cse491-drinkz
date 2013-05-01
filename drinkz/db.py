"""
Database functionality for drinkz information.

I chose to implent using a set because using a dictionary would cause a lot of
unnecessary set up that you don't really need. It's just as simple to pull up the ingredients using recipe.ingredients as it is to get them using a key.
"""

from recipes import Recipe
from parties import Party
from cPickle import dump, load
import sqlite3

# private singleton variables at module level

_bottle_types_db = set([])
_inventory_db = {}
_recipes_db = set()
_parties_db = set()

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes_db, _parties_db
    _bottle_types_db = set([])
    _inventory_db = {}
    _recipes_db = set()
    _parties_db = set()
    
def save_db(filename):

    conn = sqlite3.connect(filename)

    c = conn.cursor()
 
    c.execute('''CREATE TABLE bottle_types
                 (mfg text,liquor text,typ text)''')
    c.execute('''CREATE TABLE inventory
                 (mfg text,liquor text,amount text)''')
    c.execute('''CREATE TABLE recipes
                 (recipe text)''')
    c.execute('''CREATE TABLE parties
                 (party text)''')

    for val in _bottle_types_db:
        c.execute("INSERT INTO bottle_types (mfg,liquor,typ) VALUES (?,?,?)",val)
        
    for val in _inventory_db:
        (val1,val2) = val
        val3 = _inventory_db[val]
        c.execute("INSERT INTO inventory (mfg,liquor,amount) VALUES (?,?,?)",(val1,val2,val3))

        
    for val in _recipes_db:
        serialized = dumps(val)
        
    c.execute("INSERT INTO recipes (recipe) VALUES (?)",[sqlite3.Binary(serialized)])

    c.execute('SELECT * FROM bottle_types')
    conn.commit()
    conn.close()

def load_db(filename):
                      
    db = sqlite3.connect(filename)
    c = db.cursor()
    print "got here"
    c.execute('SELECT * FROM bottle_types')
    results = c.fetchall()
    print results
    for (mfg,liquor,typ)in results:
        add_bottle_type(mfg,liquor,typ)
        
    c.execute('SELECT * FROM inventory')
    results = c.fetchall()
    for (mfg,liquor,amount) in results:
        print amount
        add_to_inventory(mfg, liquor, amount+' ml')
        
    for row in c.execute("select * from recipes"):
        add_recipe(cPickle.loads(str(row[0])))
        
    c.close()
        
                  
# exceptions in Python inherit from Exception and generally don't need to
# override any methods.

class LiquorMissing(Exception):
    pass

class DuplicateRecipeName(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False
	
def get_liquor_types():
	"Get the liquor types."
	for (m, l, t) in _bottle_types_db:
		yield m, l, t
	

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)
    else:
        newamount = convert_to_ml(amount)
        if(mfg, liquor) in _inventory_db:
            _inventory_db[(mfg, liquor)] += newamount
        else:
            _inventory_db[(mfg, liquor)] = newamount
        
        
def check_inventory(mfg, liquor):
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    #amounts = []
    #for (m, l, amount) in _inventory_db:
    #    if mfg == m and liquor == l:
    #        amounts.append(amount)
    amounts = _inventory_db[(mfg, liquor)]
    
    return amounts

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db:
		yield m, l

def convert_to_ml(amount):
    "Converts from some unit to ml"
    if("ml") in amount:
        amount = amount.strip(' ml')
        result = float(amount)
    elif("oz") in amount:
        amount = amount.strip(' oz')
        result = float(amount) * 29.5735
    elif("gallon") in amount:
        amount = amount.strip(' gallon')
        result = float(amount) * 3785.41
    elif("liter") in amount:
        amount = amount.strip(' liter')
        result = float(amount) * 1000
    else:
        result = 0
    return result

def check_inventory_for_type(typ):
    "Checks the inventory to see if the type exists and \
    returns the max amount of it"
    amount = 0
    for(mfg, liquor, t) in _bottle_types_db:
        if (t == typ):
            if(amount < get_liquor_amount(mfg, liquor)):
                   amount = get_liquor_amount(mfg, liquor)
    return amount

            
def add_recipe(r):
    "Adds a recipe to the database"
#    for recipe in _recipes_db:
#        if r.name == recipe.name:
#            raise DuplicateRecipeName()
    print "adding"
    _recipes_db.add(r)    

def get_recipe(name):
    "Gets a recipe from the database"
    for recipe in _recipes_db:
        if name == recipe.name:
            return recipe
    return None
        
def get_all_recipes():
    "Gets all recipes"
    return list(_recipes_db)
    

def get_recipes_from_inventory():
    "Given an inventory and a list of recipes, find out which recipes we can make"
    available_recipes = []

    for recipe in _recipes_db:
        print recipe.name
        missing = recipe.need_ingredients()
        if recipe.need_ingredients() == []:
            available_recipes.append(recipe)

    return available_recipes

def add_party(p):
    "Adds a party to the database"
    _parties_db.add(p)

def get_party(name):
    "Gets a party from the database"
    for party in _parties_db:
        if name == party.name:
            return party

    return None

def get_all_parties():
    "Gets all parties"
    return list(_parties_db)

