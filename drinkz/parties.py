import db

class Party():
    
    def __init__(self, name, recipes):
        self.name = name
        self.recipes = recipes    

    def get_rating(self):
        "Returns the average drink rating"
        rating = 0
        length = 0
        for recipe in self.recipes:
            rating += recipe.rating
            length += 1
            
        rating /= length

        return rating
