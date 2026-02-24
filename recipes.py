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
    print("[3] Filter by Category")
    print("[4] Filter by Difficulty")    
    print("[5] Filter by Cook Time")
    print("[6] Sort by Rating")
    print("[7] Sort by Cook Time")
    print("[8] Search Recipes")
    print("[9] Recipe Statistics")
    print("[10] Mark Recipe Complete")
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
#   option [3] filter by Category
#-----------------------------------------------------------------------
def filter_categories():
    
    while True:
        cat_filter = input("Enter category filter (Side Dish/ Main Course/ Dessert/ Beverage): ").lower()
        if cat_filter in valid_category:
            break
        else:
            print("Invalid category. Please try again.")

        filtered_categories = [recipe for recipe in recipes if cat_filter in recipe["category"].lower()]

        # validate recipes in category exist
        if filtered_categories:
            print(tabulate(filtered_categories,headers="keys", tablefmt="grid"))
        else:
            print("No recipes in that category.")
            return

#-----------------------------------------------------------------------
#   option [4] filter by Difficulty
#-----------------------------------------------------------------------
def filter_difficulty():
    while True:
        difficulty_filter = input("Enter difficulty filter (Easy/ Medium/ Hard): ").lower()
        if difficulty_filter in valid_difficulty:
            break
        else:
            print("Invalid difficulty. Please try again.")

        filtered_difficulty = [recipe for recipe in recipes if difficulty_filter in recipe["difficulty"].lower()]

        # validate recipes in difficulty exist
        if filtered_difficulty:
            print(tabulate(filtered_difficulty,headers="keys", tablefmt="grid"))
        else:
            print("No recipes in that difficulty.")
            return  
        
#-----------------------------------------------------------------------
#   option [5] filter by Cook Time
#-----------------------------------------------------------------------
def filter_time():
    # user selects time slot filter
    while True:
        time_filter = input("Enter cook time filter ([1] under 30 min/ [2] under 2 hours/ [3] over 2 hours): ")
        if time_filter == "1":
            filtered_cook_time = [recipe for recipe in recipes if recipe["cook_time"] < 30]
            break
        elif time_filter == "2":
            filtered_cook_time = [recipe for recipe in recipes if recipe["cook_time"] < 120]
            break
        elif time_filter == "3":
            filtered_cook_time = [recipe for recipe in recipes if recipe["cook_time"] >= 120]
            break
        else:
            print("Invalid number entry. Select number (1-3).")
        
        # validate recipes in time slot exist
        if filtered_cook_time:
            print(tabulate(filtered_cook_time,headers="keys", tablefmt="grid"))
        else:
            print("No recipes in that cook time.")
            return 

#-----------------------------------------------------------------------
#   option [6] sort by rating
#-----------------------------------------------------------------------
def rating_sort():
    # make list of recipes with ratings (exclude N/A)
    rated_recipes = [rating for rating in recipes if rating["rating"] != "N/A"]
    sorted_rated = sorted(rated_recipes, key=lambda recipe: recipe["rating"], reverse=True)

    print(tabulate(sorted_rated,headers="keys", tablefmt="grid"))


#-----------------------------------------------------------------------
#   option [8] Search by any term
#-----------------------------------------------------------------------
def search():

    search_term = input("Enter search term: ").lower()
    while True:
        if search_term == "":
            print("Blank is invalid entry. Please try again.")
        else:
            break
    
    search_results = []

    # search in name, description, ingredients, and tags

    for recipe in recipes:
        if search_term in recipe['name'].lower():
            search_results.append(recipe)

    for recipe in recipes:
        if search_term in recipe['description'].lower():
            search_results.append(recipe)

    for recipe in recipes:
        if search_term in recipe['ingredients'].lower():
            search_results.append(recipe)

    for recipe in recipes:
        if search_term in recipe['tags'].lower():
            search_results.append(recipe)

    if search_results:
        print(tabulate(search_results,headers="keys", tablefmt="grid"))
    else:
        print("No matching recipes found.")
        return


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
        filter_categories()         
    elif option == '4':        
        filter_difficulty()
    elif option == '5':
        filter_time() 
    elif option == '6':
        rating_sort() 
    elif option == '7':
        pass                
    elif option == '8':
        search()
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