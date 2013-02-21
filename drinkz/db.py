"""
Database functionality for drinkz information.

I chose to implent using a set because using a dictionary would cause a lot of
unnecessary set up that you don't really need. It's just as simple to pull up the ingredients using recipe.ingredients as it is to get them using a key.
"""


from recipes import Recipe

# private singleton variables at module level

_bottle_types_db = set([])
_inventory_db = {}
_recipes_db = set()

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes_db
    _bottle_types_db = set([])
    _inventory_db = {}
    _recipes_db = set()
    
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
    for recipe in _recipes_db:
        if r.name == recipe.name:
            raise DuplicateRecipeName()
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
    
