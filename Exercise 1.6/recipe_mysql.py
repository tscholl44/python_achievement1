import pymysql

# Part 1: Create & Connect Database
def create_connection():
    """Create connection to MySQL database with fallback options"""
    print("Attempting to connect to MySQL...")
    
    # Try different connection configurations
    configs = [
        {'host': 'localhost', 'user': 'root', 'password': 'ScammyScammer_'},
        {'host': '127.0.0.1', 'user': 'root', 'password': 'ScammyScammer_'},
        {'host': 'localhost', 'user': 'cf-python', 'password': 'password'},
        {'host': '127.0.0.1', 'user': 'cf-python', 'password': 'password'},
    ]
    
    conn = None
    cursor = None
    
    for config in configs:
        try:
            print(f"Trying to connect with user: {config['user']}")
            conn = pymysql.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                charset='utf8mb4'
            )
            print(f"✓ Connected successfully as {config['user']}")
            break
        except pymysql.Error as e:
            print(f"✗ Failed to connect as {config['user']}: {e}")
            continue
        except Exception as e:
            print(f"✗ Unexpected error with {config['user']}: {e}")
            continue
    
    if not conn:
        print("All connection attempts failed!")
        return None, None
    
    try:
        
        # Initialize cursor
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
        print("Database 'task_database' created successfully!")
        
        # Use the database
        cursor.execute("USE task_database")
        
        # Create Recipes table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Recipes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            ingredients VARCHAR(255) NOT NULL,
            cooking_time INT NOT NULL,
            difficulty VARCHAR(20) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        print("Table 'Recipes' created successfully!")
        
        return conn, cursor
        
    except pymysql.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None, None

# Calculate difficulty function
def calculate_difficulty(cooking_time, ingredients):
    """Calculate recipe difficulty based on cooking time and number of ingredients"""
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

# Part 3: Creating a Recipe
def create_recipe(conn, cursor):
    """Add a new recipe to the database"""
    try:
        print("\n--- Create New Recipe ---")
        
        # Collect recipe details
        name = input("Enter recipe name: ").strip()
        if not name:
            print("Recipe name cannot be empty!")
            return
            
        cooking_time = int(input("Enter cooking time (minutes): "))
        if cooking_time <= 0:
            print("Cooking time must be positive!")
            return
            
        # Collect ingredients
        ingredients = []
        print("Enter ingredients (press Enter without text to finish):")
        while True:
            ingredient = input("Ingredient: ").strip()
            if not ingredient:
                break
            ingredients.append(ingredient)
        
        if not ingredients:
            print("Recipe must have at least one ingredient!")
            return
        
        # Calculate difficulty
        difficulty = calculate_difficulty(cooking_time, ingredients)
        
        # Convert ingredients list to comma-separated string
        ingredients_str = ", ".join(ingredients)
        
        # Build and execute query
        query = """
        INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, ingredients_str, cooking_time, difficulty))
        conn.commit()
        
        print(f"Recipe '{name}' added successfully with difficulty: {difficulty}")
        
    except ValueError:
        print("Please enter a valid number for cooking time!")
    except pymysql.Error as e:
        print(f"Error creating recipe: {e}")

# Part 4: Searching for a Recipe
def search_recipe(conn, cursor):
    """Search for recipes by ingredient"""
    try:
        print("\n--- Search Recipe by Ingredient ---")
        
        # Get all ingredients from database
        cursor.execute("SELECT ingredients FROM Recipes")
        results = cursor.fetchall()
        
        if not results:
            print("No recipes found in database!")
            return
        
        # Extract unique ingredients
        all_ingredients = []
        for row in results:
            ingredients = row[0].split(", ")
            for ingredient in ingredients:
                ingredient = ingredient.strip()
                if ingredient and ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)
        
        if not all_ingredients:
            print("No ingredients found!")
            return
        
        # Display ingredients to user
        print("\nAvailable ingredients:")
        for i, ingredient in enumerate(all_ingredients, 1):
            print(f"{i}. {ingredient}")
        
        # Get user choice
        try:
            choice = int(input(f"\nEnter ingredient number (1-{len(all_ingredients)}): "))
            if 1 <= choice <= len(all_ingredients):
                search_ingredient = all_ingredients[choice - 1]
            else:
                print("Invalid choice!")
                return
        except ValueError:
            print("Please enter a valid number!")
            return
        
        # Search for recipes containing the ingredient
        query = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
        cursor.execute(query, (f"%{search_ingredient}%",))
        search_results = cursor.fetchall()
        
        if search_results:
            print(f"\nRecipes containing '{search_ingredient}':")
            print("-" * 80)
            for recipe in search_results:
                print(f"ID: {recipe[0]}")
                print(f"Name: {recipe[1]}")
                print(f"Ingredients: {recipe[2]}")
                print(f"Cooking Time: {recipe[3]} minutes")
                print(f"Difficulty: {recipe[4]}")
                print("-" * 80)
        else:
            print(f"No recipes found containing '{search_ingredient}'")
            
    except pymysql.Error as e:
        print(f"Error searching recipes: {e}")

# Part 5: Updating a Recipe
def update_recipe(conn, cursor):
    """Update an existing recipe"""
    try:
        print("\n--- Update Recipe ---")
        
        # Display all recipes
        cursor.execute("SELECT * FROM Recipes")
        recipes = cursor.fetchall()
        
        if not recipes:
            print("No recipes found in database!")
            return
        
        print("Available recipes:")
        print("-" * 60)
        for recipe in recipes:
            print(f"ID: {recipe[0]} | Name: {recipe[1]} | Difficulty: {recipe[4]}")
        print("-" * 60)
        
        # Get recipe ID to update
        try:
            recipe_id = int(input("Enter recipe ID to update: "))
        except ValueError:
            print("Please enter a valid number!")
            return
        
        # Check if recipe exists
        cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id,))
        recipe = cursor.fetchone()
        
        if not recipe:
            print("Recipe not found!")
            return
        
        print(f"\nSelected recipe: {recipe[1]}")
        print("Available columns to update:")
        print("1. name")
        print("2. cooking_time")
        print("3. ingredients")
        
        try:
            column_choice = int(input("Enter column number to update (1-3): "))
        except ValueError:
            print("Please enter a valid number!")
            return
        
        if column_choice == 1:
            # Update name
            new_name = input("Enter new recipe name: ").strip()
            if not new_name:
                print("Recipe name cannot be empty!")
                return
            
            cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_name, recipe_id))
            print(f"Recipe name updated to '{new_name}'")
            
        elif column_choice == 2:
            # Update cooking time
            try:
                new_cooking_time = int(input("Enter new cooking time (minutes): "))
                if new_cooking_time <= 0:
                    print("Cooking time must be positive!")
                    return
            except ValueError:
                print("Please enter a valid number!")
                return
            
            # Recalculate difficulty
            ingredients_list = recipe[2].split(", ")
            new_difficulty = calculate_difficulty(new_cooking_time, ingredients_list)
            
            cursor.execute("UPDATE Recipes SET cooking_time = %s, difficulty = %s WHERE id = %s", 
                         (new_cooking_time, new_difficulty, recipe_id))
            print(f"Cooking time updated to {new_cooking_time} minutes")
            print(f"Difficulty updated to {new_difficulty}")
            
        elif column_choice == 3:
            # Update ingredients
            new_ingredients = []
            print("Enter new ingredients (press Enter without text to finish):")
            while True:
                ingredient = input("Ingredient: ").strip()
                if not ingredient:
                    break
                new_ingredients.append(ingredient)
            
            if not new_ingredients:
                print("Recipe must have at least one ingredient!")
                return
            
            # Recalculate difficulty
            new_difficulty = calculate_difficulty(recipe[3], new_ingredients)
            new_ingredients_str = ", ".join(new_ingredients)
            
            cursor.execute("UPDATE Recipes SET ingredients = %s, difficulty = %s WHERE id = %s", 
                         (new_ingredients_str, new_difficulty, recipe_id))
            print("Ingredients updated successfully")
            print(f"Difficulty updated to {new_difficulty}")
            
        else:
            print("Invalid choice!")
            return
        
        conn.commit()
        print("Recipe updated successfully!")
        
    except pymysql.Error as e:
        print(f"Error updating recipe: {e}")

# Part 6: Deleting a Recipe
def delete_recipe(conn, cursor):
    """Delete a recipe from the database"""
    try:
        print("\n--- Delete Recipe ---")
        
        # Display all recipes
        cursor.execute("SELECT * FROM Recipes")
        recipes = cursor.fetchall()
        
        if not recipes:
            print("No recipes found in database!")
            return
        
        print("Available recipes:")
        print("-" * 80)
        for recipe in recipes:
            print(f"ID: {recipe[0]}")
            print(f"Name: {recipe[1]}")
            print(f"Ingredients: {recipe[2]}")
            print(f"Cooking Time: {recipe[3]} minutes")
            print(f"Difficulty: {recipe[4]}")
            print("-" * 80)
        
        # Get recipe ID to delete
        try:
            recipe_id = int(input("Enter recipe ID to delete: "))
        except ValueError:
            print("Please enter a valid number!")
            return
        
        # Check if recipe exists
        cursor.execute("SELECT name FROM Recipes WHERE id = %s", (recipe_id,))
        recipe = cursor.fetchone()
        
        if not recipe:
            print("Recipe not found!")
            return
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete '{recipe[0]}'? (y/n): ").lower()
        if confirm == 'y' or confirm == 'yes':
            cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))
            conn.commit()
            print(f"Recipe '{recipe[0]}' deleted successfully!")
        else:
            print("Deletion cancelled.")
            
    except pymysql.Error as e:
        print(f"Error deleting recipe: {e}")

# Part 2: Main Menu
def main_menu(conn, cursor):
    """Display main menu and handle user choices"""
    while True:
        print("\n" + "="*50)
        print("         RECIPE DATABASE MANAGER")
        print("="*50)
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("5. Exit")
        print("-"*50)
        
        try:
            choice = int(input("Enter your choice (1-5): "))
            
            if choice == 1:
                create_recipe(conn, cursor)
            elif choice == 2:
                search_recipe(conn, cursor)
            elif choice == 3:
                update_recipe(conn, cursor)
            elif choice == 4:
                delete_recipe(conn, cursor)
            elif choice == 5:
                print("\nExiting program...")
                break
            else:
                print("Invalid choice! Please enter 1-5.")
                
        except ValueError:
            print("Please enter a valid number!")
        except KeyboardInterrupt:
            print("\n\nExiting program...")
            break

# Main execution
if __name__ == "__main__":
    print("Starting Recipe Database Manager...")
    
    # Create connection and initialize database
    conn, cursor = create_connection()
    
    if conn and cursor:
        try:
            # Run main menu
            main_menu(conn, cursor)
            
        finally:
            # Clean up connections
            if conn:
                conn.commit()
                cursor.close()
                conn.close()
                print("Database connection closed.")
    else:
        print("Failed to connect to database. Please check your MySQL setup.")