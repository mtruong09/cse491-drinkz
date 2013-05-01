"""
Tests HW5 features
"""

import unittest, StringIO, simplejson
from . import db, recipes, load_bulk_recipes, app

def initialize_db():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

    db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
    db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
        
    db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
    db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

    db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
    db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')


    r = recipes.Recipe('scotch on the rocks', [('blended scotch',
                                                '4 oz')])
    db.add_recipe(r)
    
    r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),
                                         ('vermouth', '1.5 oz')])
    db.add_recipe(r)
    
    r = recipes.Recipe('vomit inducing martini', [('orange juice',
                                                   '6 oz'),
                                                  ('vermouth',
                                                   '1.5 oz')])
    db.add_recipe(r)

def test_get_recipes_from_inventory():
    initialize_db()
    available = db.get_recipes_from_inventory()
    assert len(available) == 2

    assert available[1].name == 'scotch on the rocks'
    assert available[0].name == 'vodka martini'

# Test if it will not add an empty line
def test_bulk_load_recipes_empty_line():
    db._reset_db()

    data = ""
    fp = StringIO.StringIO(data)
    n = load_bulk_recipes.load_recipes(fp)

    assert n == 0, n

def test_bulk_load_inventory_1():
    db._reset_db()

    data = "vomit inducing martini,orange juice;6oz/vermouth;6oz"
    fp = StringIO.StringIO(data)                 # make this look like a file handle
    n = load_bulk_recipes.load_recipes(fp)
                            
    assert db.get_recipe("vomit inducing martini")
    assert n == 1, n

# Test if it will not add a line starting with #
def test_bulk_load_inventory_pound():
    db._reset_db()

    data = "#vomit inducing martin,orange juice;6oz/vermouth;6oz"
    fp = StringIO.StringIO(data)
    n = load_bulk_recipes.load_recipes(fp)
    
    #nothing in database
    assert n == 0, n

def test_rpc_add_to_inventory():

    initialize_db()
    myApp = app.SimpleApp()
        

    environ = {}
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'
    

    d = dict(method='add_to_inventory', params=['Gray Goose','vodka', '10 oz'] ,id=1)
    encoded = simplejson.dumps(d)
    environ['wsgi.input'] = StringIO.StringIO(encoded)
    environ['CONTENT_LENGTH'] = 1000
    
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
        
    results = myApp.__call__(environ,my_start_response)
    text = "".join(results)

    print text
    assert db.check_inventory('Gray Goose', 'vodka') == True
    amt = db.get_liquor_amount('Gray Goose', 'vodka')
    print amt
    assert amt == "1295.735"
    
def test_rpc_add_recipe():

    initialize_db()
    myApp = app.SimpleApp()
    
    
    environ = {}
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'
    

    d = dict(method='add_recipe', params=["Screw Driver","Orange Juice,8 oz,Vodka,1 oz"] ,id=1)
    encoded = simplejson.dumps(d)
    environ['wsgi.input'] = StringIO.StringIO(encoded)
    environ['CONTENT_LENGTH'] = 1000
    
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
        
    results = myApp.__call__(environ,my_start_response)
    text = "".join(results)
    
    assert text.find("Screw Driver") != -1, text
    

                                                                
                    
    
    
