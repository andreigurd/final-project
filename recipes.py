import json
from tabulate import tabulate
from datetime import datetime,date,timedelta
import os
import random
from colorama import Fore, Style, init

valid_category = ["Side Dish", "Main Course", "Dessert", "Beverage"]
valid_difficulty = ["Hard", "Medium,", "Easy"]

#-----------------------------------------------------------------------
#   opening recipes json file
#-----------------------------------------------------------------------
try:
    with open('recipes.json', 'r') as file:
        recipes = json.load(file)
except FileNotFoundError:
    print("Recipes file not found. Blank list created.")
    recipes = [] # makes an empty list
except json.JSONDecodeError:
    print("Issue loading Recipes file. File empty or invalid JSON file. Blank Recipes list created.")
    recipes = []
except ValueError:
    print("Invalid Recipes item. Blank list created.")
    recipes = []
except PermissionError:
    print("Need permission to access Recipes file. Blank Recipes list created.")
    recipes = []

#-----------------------------------------------------------------------
#   timestamp
#-----------------------------------------------------------------------

from datetime import datetime
def datetime_now_stamp():    
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_string

# importing time delta to allow time change functions
from datetime import datetime,timedelta

#-----------------------------------------------------------------------
#   showing menu
#-----------------------------------------------------------------------

def show_menu():
    print("")
    print("Welcome to Recipe Manager")
    print("[0] Exit")
    print("[1] Add Recipe")
    print("[2] View All")
    print("[3] View by Tag")
    print("[4] View by Difficulty")    
    print("[5] View by Cook Time")
    print("[6] Sort by Rating")
    print("[7] Sort by Cook Time")
    print("[8] Search Recipes")
    print("[9] Start a Recipe")
    print("[10] Recipe Statistics")
    print("[11] Delete Recipe")
    print("[12] Edit Recipe")
    print("[13] Export Recipes to CSV")
    print("[14] Feeling Lucky! Recommendation")  

#-----------------------------------------------------------------------
#   option [1] Add Recipe
#-----------------------------------------------------------------------
def add_recipe():
#---------------- number
# check if this works after a recipe is deleted. might need to loop through and renumber everything.

    number = len(recipes) + 1

#---------------- favorite
# either blank with "" or star
    favorite = ""
#---------------- name
    name = input("Enter recipe name: ")

#---------------- description
    description = input("Enter recipe description: ")

#---------------- ingredients
# multiple ingredients and amounts so need a list of dictionaries
    ingredients = []
    print('Enter ingredients or enter "done" to stop.').lower()

    while True:
        ingredient = input("Enter ingredient name: ")
        if ingredient == "done":
            break
        amount = input('Enter ingredient amount: ')
        ingredient_dict = {
            "ingredient": ingredient,
            "amount": amount
        }
        ingredients.append(ingredient_dict)

#---------------- instructions

    instructions = []
    print('Enter instruction or enter "done" to stop.').lower()

    while True:
        instruction = input("Enter instruction step: ")
        if instruction == "done":
            break
        
        instruction_dict = {
            "instruction": instruction,            
        }
        instructions.append(instruction_dict)

#---------------- cook time

    while True:
            try:
                cook_time = int(input("Enter cook time (minutes): "))
                if cook_time > 0:
                    break
            except ValueError:
                print("Invalid entry. Please try again.")

#---------------- difficulty

    while True:
        difficulty = input("Enter difficulty (Easy/ Medium/ Hard): ").lower()
        if difficulty in valid_difficulty:
            break
        else:
            print("Invalid difficulty. Please try again.")

#---------------- category

    while True:
        category = input("Enter category (Side Dish/ Main Course/ Dessert/ Beverage): ").lower()
        if category in valid_category:
            break
        else:
            print("Invalid category. Please try again.")
    
#---------------- hashtag/ tag

    tags = []
    print('Enter tag or enter "done" to stop.').lower()

    while True:
        tag = input("Enter tag: ")
        if instruction == "done":
            break
        
        tag_dict = {
            "tag": tag,            
        }
        tags.append(tag_dict)

#---------------- rating (allow decimal ratings)
# ask once completed
    rating = "N/A"

#---------------- date added

    date_string = datetime_now_stamp()
    print(f'Recipe added date entered as {date_string}') 

#---------------- status (completed or not completed)

    completed_flag = "not_completed"

    recipe = {
        "number": number,
        "favorite": favorite,
        "name": name,
        "description": description,
        "ingredients": ingredients,
        "instructions": instructions,
        "cook_time": cook_time,
        "difficulty": difficulty,
        "category": category,
        "tags": tags,
        "rating": rating,
        "date": date_string
    }

    recipes.append(recipe)
    return completed_flag

#-----------------------------------------------------------------------
#   option [2] show all Recipes
#-----------------------------------------------------------------------
# dont need to show ingredients until recipe is started. make shorter list to display
def view_recipes():
    print('Displaying All Recipes. Completed Recipes shown in Green.')
    # validate recipes exist. return and ends function if recipes is empty.
    if not recipes:
        print('No recipes available.')
        return
    
    # make different list to display

    diplay_all_recipes = []

    for recipe in recipes:        
        name = recipe["name"]
        # turn completed recipe name green
        if recipe["name"] == "completed":
            name = Fore.GREEN + name + Style.RESET_ALL
        
        # append into a new list
        display_dict = {
            "number": recipe['number'],
            "favorite": recipe['favorite'],
            "name": name,
            "cook_time": recipe['cook_time'],
            "difficulty": recipe['difficulty'],
            "category": recipe['category'],
            "tags": recipe['tags'],
            "rating": recipe['rating']            
        }
        diplay_all_recipes.append(display_dict)

    
#-----------------------------------------------------------------------
#   function to write to recipes json
#-----------------------------------------------------------------------
def write_recipe_json():
    with open('recipes.json', 'w') as file:
        json.dump(recipes, file, indent=4)

#-----------------------------------------------------------------------
#   # while loop to get user input
#-----------------------------------------------------------------------

while True:
    show_menu()
    option = input("\nSelect Option: ")    
    if option == '0':        
        write_recipe_json()            
        print("Goodbye.")
        break
    elif option == '1':
        add_recipe()
        write_recipe_json()       
    elif option == '2':        
        diplay_all_recipes = view_recipes()
        print(tabulate(diplay_all_recipes,headers="keys", tablefmt="grid"))
    elif option == '3':
        pass         
    elif option == '4':        
        pass
    elif option == '5':
        pass 
    elif option == '6':
        pass 
    elif option == '7':
        pass                
    elif option == '8':
        pass
    elif option == '9':        
        pass
    elif option == '10':
        pass
    elif option == '11':
        pass
    elif option == '12':
        pass
    elif option == '13':
        pass      
    else:
        print("Invalid action. Please try again.")