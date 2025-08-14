# Python Addition Script

A simple Python script that prompts the user to enter two numbers and displays their sum.

## Files

- `add.py` - Main script that adds two user-entered numbers
- `hello.py` - Additional Python script
- `requirements.txt` - List of Python dependencies

## How to Run

1. Make sure you have Python installed
2. Run the script: `python add.py`
3. Enter two numbers when prompted
4. The sum will be displayed

## Installation

To install the required packages:
```bash
pip install -r requirements.txt
```

## Data Structure

I have chosen to structure my recipe objects as dictionary data types, because each attribute is represented by key value pairs. This makes updating and adding to the recipes easy. I also wrapped these recipe dictionaries into a larger dictionary called all_recipes so that for example 'recipe_1' becomes the key value paired with its respective list of names, cooking times and ingredients.