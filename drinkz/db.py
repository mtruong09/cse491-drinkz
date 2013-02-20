"""
Database functionality for drinkz information.
"""

# private singleton variables at module level

_bottle_types_db = set([])
_inventory_db = {}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db = set([])
    _inventory_db = {}

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
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
    "Converts from oz to ml"
    if("ml") in amount:
        amount = amount.strip(' ml')
        result = float(amount)
    elif("oz") in amount:
        amount = amount.strip(' oz')
        result = float(amount) * 29.5735

    return result
