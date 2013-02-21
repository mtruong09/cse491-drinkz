import db

class Recipe():
    
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients    

    def need_ingredients(self):
        "Returns a list of missing ingredients to make the recipe"
        missing = []

        # For each ingredient, check to see if its in the inventory
        for typ, amount in self.ingredients:
            # convert the amount to ml
            amountNeeded = db.convert_to_ml(amount)

            # check if its in the inventory and return the amount
            amountInInventory = db.check_inventory_for_type(typ)

            # check if the amount in inventory is less than the amount needed
            if amountInInventory <= amountNeeded:

                amountMissing = amountNeeded - amountInInventory
                missingTup = (typ, amountMissing)
                missing.append(missingTup)

        return missing
            
