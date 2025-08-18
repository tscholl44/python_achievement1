import pickle

# define a function to display a recipe
def display_recipe(recipe):

    print(f"Recipe: {recipe['recipe_name']}")
    print(f"Cooking Time: {recipe['cooking_time']} minutes")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty: {recipe['difficulty']}")

# define a function to search for recipes by ingredient
def search_ingredient(data):

    all_ingredients = data['all_ingredients']
    
    print("Available ingredients:")
    for index, ingredient in enumerate(all_ingredients):
        print(f"{index}: {ingredient}")
    
    try:
        user_choice = int(input("\nEnter the number corresponding to the ingredient: "))
        ingredient_searched = all_ingredients[user_choice]
    except (ValueError, IndexError):
        print("Incorrect input. Please enter a valid number from the list.")
    else:
        print(f"\nRecipes containing '{ingredient_searched}':")
        
        recipes_list = data['recipes_list']
        found_recipes = False
        
        for recipe in recipes_list:
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)
                found_recipes = True
        
        if not found_recipes:
            print(f"No recipes found containing '{ingredient_searched}'")

# Ask the user for the name of the file that contains the recipe data
filename = input("Enter the filename that contains your recipe data: ")

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found. Please make sure the filename is correct and the file exists.")
else:
    search_ingredient(data)