# Step 1: Initialize two empty lists
recipes_list = []
ingredients_list = []

# Step 2: Define take_recipe function
def take_recipe():

    # Get recipe name
    name = input("Enter the recipe name: ")
    
    # Get cooking time and convert to integer
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    
    # Get ingredients
    ingredients = []
    num_ingredients = int(input("How many ingredients does this recipe have? "))
    
    for i in range(num_ingredients):
        ingredient = input(f"Enter ingredient {i + 1}: ")
        ingredients.append(ingredient)
    
    # Create recipe dictionary
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients
    }
    
    return recipe

# Step 3: Main section - ask user how many recipes they want to enter
n = int(input("How many recipes would you like to enter? "))

# Step 4: Loop to collect recipes
for i in range(n):
    print(f"\n--- Recipe {i + 1} ---")
    
    # Get recipe from user
    recipe = take_recipe()
    
    # Add new ingredients to ingredients_list
    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    
    # Add recipe to recipes_list
    recipes_list.append(recipe)

# Step 5: Display recipes with difficulty levels
print("\n" + "="*50)
print("RECIPE SUMMARY")
print("="*50)

for recipe in recipes_list:
    cooking_time = recipe['cooking_time']
    num_ingredients = len(recipe['ingredients'])
    
    # Determine difficulty based on cooking time and number of ingredients
    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    else:  # cooking_time >= 10 and num_ingredients >= 4
        difficulty = "Hard"
    
    # Display recipe information
    print(f"\nRecipe: {recipe['name']}")
    print(f"Cooking Time: {recipe['cooking_time']} minutes")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty: {difficulty}")

print("\n" + "="*50)
print("ALL INGREDIENTS USED")
print("="*50)
ingredients_list.sort()  # Sort alphabetically 
for ingredient in ingredients_list:
    print(f"- {ingredient}")