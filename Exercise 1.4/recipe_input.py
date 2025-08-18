# Import the pickle module
import pickle

# Define calc_difficulty
def calc_difficulty(cooking_time, ingredients):
    
    num_ingredients = len(ingredients)
    
    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and num_ingredients >= 4:
        difficulty = "Hard"
    
    return difficulty


# Define take_recipe
def take_recipe():

    recipe_name = input("Enter recipe name: ")
    cooking_time = int(input("Enter cooking time (in minutes): "))
    
    ingredients = []
    ingredient_count = int(input("How many ingredients does this recipe have? "))
    
    for i in range(ingredient_count):
        ingredient = input(f"Enter ingredient {i+1}: ")
        ingredients.append(ingredient)
    
    difficulty = calc_difficulty(cooking_time, ingredients)
    
    recipe = {
        'recipe_name': recipe_name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
        'difficulty': difficulty
    }
    
    return recipe

# User can enter a filename
filename = input("Enter the filename where you want to save recipes: ")

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found. Creating new data structure.")
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
except:
    print("An error occurred. Creating new data structure.")
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
else:
    file.close()
finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']


# Ask user how many recipes they want to enter
n = int(input("How many recipes would you like to enter? "))

# Loop to calls take_recipe function 
for i in range(n):
    print(f"\nEntering recipe {i+1}:")
    recipe = take_recipe()
    recipes_list.append(recipe)

    # Inner loop that scans through recipe ingredients and adds them to all_ingredients
    for ingredient in recipe['ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

# Update data dictionary
data = {
    'recipes_list': recipes_list,
    'all_ingredients': all_ingredients
}

# Save data to file
with open(filename, 'wb') as file:
    pickle.dump(data, file)

print(f"Recipe data saved to {filename}")


