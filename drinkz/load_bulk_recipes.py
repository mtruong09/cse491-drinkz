"""
Module to load in bulk recipes from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv
import string

from . import db, recipes                        # import from local package

def data_reader(fp):
    reader = csv.reader(fp)

    for line in reader:
        if not line:
            continue
        if line[0].startswith('#'):
            continue
        if not line[0].strip():
            continue
        yield line

def load_recipes(fp):
    """
    Loads in data of the form name,ingredient,ingredient amt, from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of recipes loaded
    """
    reader = data_reader(fp)
    
    x = []
    n = 0
    for line in reader:
        try:
            name = line[0]

            i = 1
            ingredients = []
            while i < len(line)-1:
                typ = line[i]
                amount = line[i+1]
                ingredients.append((typ, amount))
                i+=2
                
#            splitline = line[1].split('/')

#            i = 0
#            while i < len(splitline)-1:
#                ingredients = splitline[i].split(';')
#                i+=1

        except:
            print "Error loading line - incorrect formatting"

        try:
            r = recipes.Recipe(name, ingredients)
            db.add_recipe(r)
        except:
            print "Error adding recipe"

        n+=1
        
    return n

