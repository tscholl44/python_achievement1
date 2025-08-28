# Import packages and methods
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker

# Create engine object to connect to database
engine = create_engine("mysql+pymysql://cf-python:password@localhost/task_database")

# Store declarative base
Base = declarative_base()

# Create session object to make changes to database
Session = sessionmaker(bind=engine)
session = Session()

# Part 2: Create Your Model and Table
class Recipe(Base):
    __tablename__ = 'final_recipes'
    
    # Define columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    ingredients = Column(String(255), nullable=False)
    cooking_time = Column(Integer, nullable=False)
    difficulty = Column(String(20), nullable=False)
    

    def __repr__(self):
        return f"<Recipe(id={self.id}, name='{self.name}', difficulty='{self.difficulty}')>"
    
    # formatted string method
    def __str__(self):
        return f"""
{'='*60}
Recipe ID: {self.id}
Recipe Name: {self.name}
{'='*60}
Ingredients: {self.ingredients}
Cooking Time: {self.cooking_time} minutes
Difficulty: {self.difficulty}
{'='*60}
        """.strip()
    
    # Calculate difficulty based on cooking time and ingredients
    def calculate_difficulty(self):
        ingredients_list = self.return_ingredients_as_list()
        num_ingredients = len(ingredients_list)
        
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_ingredients >= 4:
            self.difficulty = "Hard"
    
    # Return ingredients as list
    def return_ingredients_as_list(self):
        if not self.ingredients or self.ingredients.strip() == "":
            return []
        return [ingredient.strip() for ingredient in self.ingredients.split(", ")]

# Create the table
Base.metadata.create_all(engine)

# Part 3: Define Main Operations as Functions

# Function to create a new recipe

def create_recipe():
    print("\n" + "="*50)
    print("           CREATE NEW RECIPE")
    print("="*50)
    
    # Collect recipe name
    while True:
        name = input("Enter recipe name: ").strip()
        if not name:
            print("Recipe name cannot be empty!")
            continue
        if len(name) > 50:
            print("Recipe name cannot exceed 50 characters!")
            continue
        if not name.replace(" ", "").isalnum():
            print("Recipe name should contain only alphanumeric characters and spaces!")
            continue
        break
    
    # Collect cooking time
    while True:
        cooking_time_input = input("Enter cooking time (minutes): ").strip()
        if not cooking_time_input.isnumeric():
            print("Cooking time must be a number!")
            continue
        cooking_time = int(cooking_time_input)
        if cooking_time <= 0:
            print("Cooking time must be positive!")
            continue
        break
    
    # Collect ingredients
    while True:
        num_ingredients_input = input("How many ingredients would you like to enter? ").strip()
        if not num_ingredients_input.isnumeric():
            print("Please enter a valid number!")
            continue
        num_ingredients = int(num_ingredients_input)
        if num_ingredients <= 0:
            print("You must enter at least one ingredient!")
            continue
        break
    
    ingredients = []
    for i in range(num_ingredients):
        while True:
            ingredient = input(f"Enter ingredient {i+1}: ").strip()
            if not ingredient:
                print("Ingredient cannot be empty!")
                continue
            if not ingredient.replace(" ", "").isalpha():
                print("Ingredient should contain only alphabetical characters!")
                continue
            break
        ingredients.append(ingredient)
    
    # Convert ingredients list to string
    ingredients_str = ", ".join(ingredients)
    
    # Create recipe entry
    recipe_entry = Recipe(
        name=name,
        ingredients=ingredients_str,
        cooking_time=cooking_time
    )
    
    # Calculate difficulty
    recipe_entry.calculate_difficulty()
    
    # Add to database
    session.add(recipe_entry)
    session.commit()
    
    print(f"\n✓ Recipe '{name}' added successfully with difficulty: {recipe_entry.difficulty}")

# Function to view all recipes

def view_all_recipes():

    print("\n" + "="*50)
    print("            ALL RECIPES")
    print("="*50)
    
    # Retrieve all recipes
    recipes = session.query(Recipe).all()
    
    if not recipes:
        print("No recipes found in the database!")
        return None
    
    # Display each recipe
    for recipe in recipes:
        print(recipe)
        print()

# Function to search recipes by ingredients

def search_by_ingredients():
 
    print("\n" + "="*50)
    print("       SEARCH BY INGREDIENTS")
    print("="*50)
    
    # Check if any recipes exist
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("No recipes found in the database!")
        return None
    
    # Get all ingredients from database
    results = session.query(Recipe.ingredients).all()
    
    # Extract unique ingredients
    all_ingredients = []
    for result in results:
        ingredients_list = result[0].split(", ")
        for ingredient in ingredients_list:
            ingredient = ingredient.strip()
            if ingredient and ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
    
    # Display ingredients with numbers
    print("\nAvailable ingredients:")
    for i, ingredient in enumerate(all_ingredients, 1):
        print(f"{i}. {ingredient}")
    
    # Get user selection
    while True:
        selection = input(f"\nEnter ingredient numbers (1-{len(all_ingredients)}) separated by spaces: ").strip()
        if not selection:
            print("Please enter at least one ingredient number!")
            continue
        
        try:
            selected_numbers = [int(x) for x in selection.split()]
            if not all(1 <= num <= len(all_ingredients) for num in selected_numbers):
                print(f"Please enter numbers between 1 and {len(all_ingredients)}!")
                continue
            break
        except ValueError:
            print("Please enter valid numbers separated by spaces!")
            continue
    
    # Create search ingredients list
    search_ingredients = [all_ingredients[num-1] for num in selected_numbers]
    
    # Create search conditions
    conditions = []
    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))
    
    # Search recipes
    recipes = session.query(Recipe).filter(or_(*conditions)).all()
    
    if not recipes:
        print("No recipes found with the selected ingredients!")
        return None
    
    print(f"\nRecipes containing {', '.join(search_ingredients)}:")
    print("-" * 80)
    for recipe in recipes:
        print(recipe)
        print()

# Function to edit a recipe

def edit_recipe():

    print("\n" + "="*50)
    print("            EDIT RECIPE")
    print("="*50)
    
    # Check if any recipes exist
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("No recipes found in the database!")
        return None
    
    # Display available recipes
    results = session.query(Recipe.id, Recipe.name).all()
    print("Available recipes:")
    print("-" * 40)
    for recipe_id, recipe_name in results:
        print(f"ID: {recipe_id} | Name: {recipe_name}")
    print("-" * 40)
    
    # Get recipe selection
    while True:
        recipe_id_input = input("Enter recipe ID to edit: ").strip()
        if not recipe_id_input.isnumeric():
            print("Please enter a valid recipe ID!")
            continue
        
        recipe_id = int(recipe_id_input)
        recipe_to_edit = session.query(Recipe).filter(Recipe.id == recipe_id).first()
        
        if not recipe_to_edit:
            print("Recipe not found!")
            return None
        break
    
    # Display current recipe details
    print(f"\nSelected Recipe:")
    print(f"Name: {recipe_to_edit.name}")
    print(f"Ingredients: {recipe_to_edit.ingredients}")
    print(f"Cooking Time: {recipe_to_edit.cooking_time} minutes")
    
    # Show editable attributes
    print("\nWhich attribute would you like to edit?")
    print("1. Name")
    print("2. Ingredients")
    print("3. Cooking Time")
    
    while True:
        choice_input = input("Enter your choice (1-3): ").strip()
        if choice_input not in ['1', '2', '3']:
            print("Please enter 1, 2, or 3!")
            continue
        choice = int(choice_input)
        break
    
    # Edit based on choice
    if choice == 1:
        # Edit name
        while True:
            new_name = input("Enter new recipe name: ").strip()
            if not new_name:
                print("Recipe name cannot be empty!")
                continue
            if len(new_name) > 50:
                print("Recipe name cannot exceed 50 characters!")
                continue
            break
        recipe_to_edit.name = new_name
        
    elif choice == 2:
        # Edit ingredients
        while True:
            num_ingredients_input = input("How many ingredients would you like to enter? ").strip()
            if not num_ingredients_input.isnumeric():
                print("Please enter a valid number!")
                continue
            num_ingredients = int(num_ingredients_input)
            if num_ingredients <= 0:
                print("You must enter at least one ingredient!")
                continue
            break
        
        ingredients = []
        for i in range(num_ingredients):
            while True:
                ingredient = input(f"Enter ingredient {i+1}: ").strip()
                if not ingredient:
                    print("Ingredient cannot be empty!")
                    continue
                break
            ingredients.append(ingredient)
        
        recipe_to_edit.ingredients = ", ".join(ingredients)
        
    elif choice == 3:
        # Edit cooking time
        while True:
            cooking_time_input = input("Enter new cooking time (minutes): ").strip()
            if not cooking_time_input.isnumeric():
                print("Cooking time must be a number!")
                continue
            cooking_time = int(cooking_time_input)
            if cooking_time <= 0:
                print("Cooking time must be positive!")
                continue
            break
        recipe_to_edit.cooking_time = cooking_time
    
    # Recalculate difficulty
    recipe_to_edit.calculate_difficulty()
    
    # Commit changes
    session.commit()
    
    print(f"\n✓ Recipe updated successfully!")
    print(f"New difficulty: {recipe_to_edit.difficulty}")

# Function to delete a recipe

def delete_recipe():

    print("\n" + "="*50)
    print("           DELETE RECIPE")
    print("="*50)
    
    # Check if any recipes exist
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("No recipes found in the database!")
        return None
    
    # Display available recipes
    results = session.query(Recipe.id, Recipe.name).all()
    print("Available recipes:")
    print("-" * 40)
    for recipe_id, recipe_name in results:
        print(f"ID: {recipe_id} | Name: {recipe_name}")
    print("-" * 40)
    
    # Get recipe selection
    while True:
        recipe_id_input = input("Enter recipe ID to delete: ").strip()
        if not recipe_id_input.isnumeric():
            print("Please enter a valid recipe ID!")
            continue
        
        recipe_id = int(recipe_id_input)
        recipe_to_delete = session.query(Recipe).filter(Recipe.id == recipe_id).first()
        
        if not recipe_to_delete:
            print("Recipe not found!")
            return None
        break
    
    # Confirm deletion
    print(f"\nSelected recipe: {recipe_to_delete.name}")
    while True:
        confirm = input("Are you sure you want to delete this recipe? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            session.delete(recipe_to_delete)
            session.commit()
            print(f"✓ Recipe '{recipe_to_delete.name}' deleted successfully!")
            break
        elif confirm in ['no', 'n']:
            print("Deletion cancelled.")
            return None
        else:
            print("Please enter 'yes' or 'no'!")
            continue

# Part 4: Design Your Main Menu
def main_menu():
    print("\n" + "="*60)
    print("           RECIPE DATABASE APPLICATION")
    print("="*60)
    print("Welcome to the Recipe Database Manager!")
    
    while True:
        print("\n" + "-"*50)
        print("           MAIN MENU")
        print("-"*50)
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("\nType 'quit' to quit the application")
        print("-"*50)
        
        choice = input("Enter your choice: ").strip().lower()
        
        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice == 'quit':
            print("\n" + "="*50)
            print("Thank you for using Recipe Database Manager!")
            print("Goodbye!")
            print("="*50)
            break
        else:
            print("\n❌ Invalid input! Please enter 1-5 or 'quit'")
            continue

# Main execution
if __name__ == "__main__":
    try:
        main_menu()
    finally:
        # Close session and engine
        session.close()
        engine.dispose()
        print("Database connection closed.")