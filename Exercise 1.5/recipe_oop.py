class Recipe:
    all_ingredients = set()

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = None
    
    # Getter and setter name
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    # Getter for ingredients
    def get_ingredients(self):
        return self.ingredients

    # Getter and setter methods to get and set cooking_time
    def get_cooking_time(self):
        return self.cooking_time

    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    # Add ingredients with variable-length arguments
    def add_ingredients(self, *ingredients):
        self.ingredients.extend(ingredients)
        self.update_all_ingredients()

    # Update class variable with all ingredients
    def update_all_ingredients(self):
        Recipe.all_ingredients.update(self.ingredients)

    # Calculate difficulty
    def calculate_difficulty(self):
        num_ingredients = len(self.ingredients)
        
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_ingredients >= 4:
            self.difficulty = "Hard"

    # Getter for difficulty that calculates if needed
    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty

    # Search for an ingredient
    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    # String representation defined for all objects
    def __str__(self):
        return (f"Recipe: {self.name}\n"
                f"Ingredients: {', '.join(self.ingredients)}\n"
                f"Cooking Time: {self.cooking_time} minutes\n"
                f"Difficulty: {self.get_difficulty()}")

# Search recipes by ingredient
def recipe_search(data, search_term):
    print(f"\nRecipes containing '{search_term}':")
    print("-" * 40)
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)
            print()

# Main code..
if __name__ == "__main__":

    tea = Recipe("Tea")
    tea.add_ingredients("Tea Leaves", "Sugar", "Water")
    tea.set_cooking_time(5)
    print(tea)
    print()


    coffee = Recipe("Coffee")
    coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
    coffee.set_cooking_time(5)
    print(coffee)
    print()

    cake = Recipe("Cake")
    cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
    cake.set_cooking_time(50)
    print(cake)
    print()

    banana_smoothie = Recipe("Banana Smoothie")
    banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
    banana_smoothie.set_cooking_time(5)
    print(banana_smoothie)
    print()

    # Create recipes list
    recipes_list = [tea, coffee, cake, banana_smoothie]
    
    # Search for recipes containing specific ingredients
    search_ingredients = ["Water", "Sugar", "Bananas"]
    
    for ingredient in search_ingredients:
        recipe_search(recipes_list, ingredient)
    
    # Display all ingredients that have been used
    print(f"All ingredients used across recipes: {sorted(Recipe.all_ingredients)}")

