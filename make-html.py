#! /user/bin/env python

import os
from drinkz import db
from drinkz import recipes

#fill the database
db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

r = recipes.Recipe('scotch on the rocks', [('blended scotch', '4 oz')])
db.add_recipe(r)

r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),('vermouth', '1.5 oz')])
db.add_recipe(r)

r = recipes.Recipe('vomit inducing martini', [('orange juice','6 oz'),('vermouth','1.5 oz')])
db.add_recipe(r)


###

try:
	os.mkdir('html')
except:
	pass

#strings to other pages
index_html = """<p><a href="index.html">Index</a>"""
liquor_types_html = """<p><a href="liquor-types.html">Liquor Types</a>"""
inventory_html = """<p><a href="inventory.html">Inventory</a>"""
recipes_html = """<p><a href="recipes.html">Recipes</a>"""

##
#Index.html
##
fp = open('html/index.html', 'w')
links = "CSE491 Draankz\n" + liquor_types_html + inventory_html + recipes_html
print >> fp, links
fp.close()


##
#liquor-types.html
##
fp = open('html/liquor-types.html', 'w')
liquors = "Liquor Types\n<ol>"
for mfg, liquor in db.get_liquor_inventory():
	liquors += "<li>" + mfg + ", " + liquor + "</li>"

liquors += "</ol>"

links = index_html + inventory_html + recipes_html
liquors += links
print >> fp, liquors

fp.close()


##
#inventory.html
##
fp = open('html/inventory.html', 'w')
inventory = "Inventory\n<ol>"
for liquor in db.get_liquor_inventory():
	mfg = liquor[0]
	l = liquor[1]
	amount = db.get_liquor_amount(mfg, l)
	inventory += "<li>" + mfg + ", " + l + ": " + str(amount) + " ml</li>\n"

inventory += "</ol>"
links = index_html + liquor_types_html + recipes_html
inventory += links
print >> fp, inventory

fp.close()


##
#Recipes.html
##
fp = open('html/recipes.html', 'w')
all_recipes = db.get_all_recipes()
recipe_str = "Recipez\n<ol>"
for r in all_recipes:
	if(r.need_ingredients() == []):
		have_all = "Yeahhhhhhh"
	else:
		have_all = "Oh noooooo"
	recipe_str += "<li>" + r.name + ": " + have_all + "</li>\n"

recipe_str += "</ol>"
links = index_html + liquor_types_html + inventory_html
recipe_str += links
print >> fp, recipe_str

fp.close()
