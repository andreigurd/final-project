import json
from tabulate import tabulate
from datetime import datetime,date,timedelta
import os
import random
from colorama import Fore, Style, init

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
    print("[4] View by Diffuculty")    
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
        pass
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