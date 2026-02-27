import json
from tabulate import tabulate
from datetime import datetime
import os
import random
from colorama import Fore, Style, init
import csv

valid_category = ["side dish", "main course", "dessert", "beverage"]
valid_difficulty = ["hard", "medium", "easy"]

#-----------------------------------------------------------------------
#   opening recipes json file
#-----------------------------------------------------------------------
# encoding="utf-8" is needed for emoji stored in json
try:
    with open('recipes.json', 'r', encoding="utf-8") as file:
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
#   opening recipe goals json file
#-----------------------------------------------------------------------

try:
    with open('recipe_goals.json', 'r') as file:
        recipe_goals = json.load(file)
except FileNotFoundError:
    print("Goals file not found. Goal set to default zero.")
    recipe_goals = {"year_goal": 0}
except json.JSONDecodeError:
    print("Issue loading Goals file. File empty or invalid JSON file. Goal set to default zero.")
    recipe_goals = {"year_goal": 0}
except ValueError:
    print("Invalid Goals item. Goal set to default zero.")
    recipe_goals = {"year_goal": 0}
except PermissionError:
    print("Need permission to access Goals file. Goal set to default zero.")
    recipe_goals = {"year_goal": 0}

#-----------------------------------------------------------------------
#   timestamp
#-----------------------------------------------------------------------

def datetime_now_stamp():    
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_string


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
    print("[12] Recipe Goals")
    print("[13] Export Recipes to CSV")
    print("[14] Get Recipe Recommendation") 
    

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

    while True:
        choice = input("Would you like to mark recipe as favorite (yes or no): ").lower()
        if choice == "yes":
            favorite = "★"
        elif choice == "no":
            break
        else:
            print("Invalid entry. Please enter yes or no.")
#---------------- name
    while True:
        name = input("Enter recipe name: ")
        if name == "":
            print("Blank space is not a valid entry. Please try again.")
        else:
            break

#---------------- description
    while True:
        description = input("Enter recipe description: ")
        if description == "":
            print("Blank space is not a valid entry. Please try again.")
        else:
            break
    

#---------------- ingredients
# multiple ingredients and amounts so need a list of dictionaries
    ingredients = []
    print('Enter ingredients or enter "done" to stop.')

    while True:
        ingredient = input("Enter ingredient name: ").lower()
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
    print('Enter instruction or enter "done" to stop.')

    while True:
        instruction = input("Enter instruction step: ").lower()
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
    print('Enter tag or enter "done" to stop.')

    while True:
        tag = input("Enter tag: ").lower()
        if tag == "done":
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
        "date_added": date_string,
        "finished_date": "N/A"
    }

    recipes.append(recipe)
    
#-----------------------------------------------------------------------
#   option [2] show all Recipes
#-----------------------------------------------------------------------
# dont need to show ingredients until recipe is started. make shorter list to display
def view_recipes():
    print('Displaying All Summary Recipes. Completed Recipes shown in Green.')
    # validate recipes exist. return and ends function if recipes is empty.
    if not recipes:
        print('No recipes available.')
        return
    
    # make different list to display

    diplay_all_recipes = []

    for recipe in recipes:        
        name = recipe["name"]
        # turn completed recipe name green
        if recipe["finished_date"] != "N/A":
            name = Fore.GREEN + name + Style.RESET_ALL
        
        # append into a new list
        display_dict = {
            "number": recipe['number'],
            "favorite": recipe['favorite'],
            "name": name,
            "cook_time": recipe['cook_time'],
            "difficulty": recipe['difficulty'],
            "category": recipe['category'],            
            "rating": recipe['rating']            
        }
        diplay_all_recipes.append(display_dict)

    return diplay_all_recipes
    #print(tabulate(diplay_all_recipes,headers="keys", tablefmt="grid"))

#-----------------------------------------------------------------------
#   option [3] filter by Category
#-----------------------------------------------------------------------
def filter_categories():

    diplay_all_recipes = view_recipes()
    
    while True:
        cat_filter = input("Enter category filter (Side Dish/ Main Course/ Dessert/ Beverage): ").lower()
        if cat_filter in valid_category:
            break
        else:
            print("Invalid category. Please try again.")

    filtered_categories = [recipe for recipe in diplay_all_recipes if cat_filter in recipe["category"].lower()]

        # validate recipes in category exist
    if filtered_categories:
        print('Displaying Filtered Summary Recipes. Completed Recipes shown in Green.')
        print(tabulate(filtered_categories,headers="keys", tablefmt="grid"))
    else:
        print("No recipes in that category.")
        return

#-----------------------------------------------------------------------
#   option [4] filter by Difficulty
#-----------------------------------------------------------------------
def filter_difficulty():

    diplay_all_recipes = view_recipes()

    while True:
        difficulty_filter = input("Enter difficulty filter (Easy/ Medium/ Hard): ").lower()
        if difficulty_filter in valid_difficulty:
            break
        else:
            print("Invalid difficulty. Please try again.")

    filtered_difficulty = [recipe for recipe in diplay_all_recipes if difficulty_filter in recipe["difficulty"].lower()]

    # validate recipes in difficulty exist
    if filtered_difficulty:
        print('Displaying Filtered Summary Recipes. Completed Recipes shown in Green.')
        print(tabulate(filtered_difficulty,headers="keys", tablefmt="grid"))
    else:
        print("No recipes in that difficulty.")
        return  
        
#-----------------------------------------------------------------------
#   option [5] filter by Cook Time
#-----------------------------------------------------------------------
def filter_time():

    diplay_all_recipes = view_recipes()

    # user selects time slot filter
    while True:
        time_filter = input("Enter cook time filter ([1] under 30 min/ [2] under 2 hours/ [3] over 2 hours): ")
        if time_filter == "1":
            filtered_cook_time = [recipe for recipe in diplay_all_recipes if recipe["cook_time"] < 30]
            break
        elif time_filter == "2":
            filtered_cook_time = [recipe for recipe in diplay_all_recipes if recipe["cook_time"] < 120]
            break
        elif time_filter == "3":
            filtered_cook_time = [recipe for recipe in diplay_all_recipes if recipe["cook_time"] >= 120]
            break
        else:
            print("Invalid number entry. Select number (1-3).")
        
    # validate recipes in time slot exist
    if filtered_cook_time:
        print('Displaying Filtered Summary Recipes. Completed Recipes shown in Green.')
        print(tabulate(filtered_cook_time,headers="keys", tablefmt="grid"))
    else:
        print("No recipes in that cook time.")
        return 

#-----------------------------------------------------------------------
#   option [6] sort by rating
#-----------------------------------------------------------------------
def rating_sort():

    diplay_all_recipes = view_recipes()

    # make list of recipes with ratings (exclude N/A)
    rated_recipes = [rating for rating in diplay_all_recipes if rating["rating"] != "N/A"]
    sorted_rated = sorted(rated_recipes, key=lambda recipe: recipe["rating"], reverse=True)

    print('Displaying Sorted Summary Recipes. Completed Recipes shown in Green.')
    print(tabulate(sorted_rated,headers="keys", tablefmt="grid"))

#-----------------------------------------------------------------------
#   option [7] sort by cook time
#-----------------------------------------------------------------------
def cook_time_sort():

    diplay_all_recipes = view_recipes()
        
    sorted_time = sorted(diplay_all_recipes, key=lambda recipe: recipe["cook_time"], reverse=True)

    print('Displaying Sorted Summary Recipes. Completed Recipes shown in Green.')
    print(tabulate(sorted_time,headers="keys", tablefmt="grid"))

#-----------------------------------------------------------------------
#   option [8] Search by any term
#-----------------------------------------------------------------------
def search():

    
    while True:
        search_term = input("Enter search term: ").lower()
        if search_term == "":
            print("Blank is invalid entry. Please try again.")
        else:
            break
    
    search_results = []

    # search in name, description, ingredients, and tags
    # need unique variables for each. cant have multiple recipe variables in one function.

    for recipe in recipes:
        if search_term in recipe['name'].lower():
            # add validation to prevent duplicate recipes
            if recipe not in search_results:
                search_results.append(recipe)

    #for b in recipes:
        if search_term in recipe['description'].lower():
            if recipe not in search_results:
                search_results.append(recipe)

# ingredients is a list so need to look inside list.
    #for c in recipes:
        for cc in recipe['ingredients']:
            # note dictionary ingredients has ingredient and amount. want to refrence ingredient here, no S.
            if search_term in cc['ingredient'].lower():
                if recipe not in search_results:
                    search_results.append(recipe)

    #for d in recipes:
        for dd in recipe['tags']:
            if search_term in dd['tag'].lower():
                if recipe not in search_results:
                    search_results.append(recipe)

        if search_term in recipe['difficulty'].lower():
            if recipe not in search_results:
                search_results.append(recipe)

    if not search_results:
        print("No matching recipes found.")
        return
        #print(tabulate(search_results,headers="keys", tablefmt="grid"))
    # else:
    #     print("No matching recipes found.")
    #     return

    search_summary = []

    for summary in search_results:        
        name = summary["name"]
        # turn completed recipe name green
        if summary["finished_date"] != "N/A":
            name = Fore.GREEN + name + Style.RESET_ALL
        
        # append into a new list
        display_dict = {
            "number": summary['number'],
            "favorite": summary['favorite'],
            "name": name,
            "cook_time": summary['cook_time'],
            "difficulty": summary['difficulty'],
            "category": summary['category'],            
            "rating": summary['rating']            
        }
        search_summary.append(display_dict)

    print(tabulate(search_summary,headers="keys", tablefmt="grid"))

#-----------------------------------------------------------------------
#   option [9] Recipe Statistics
#-----------------------------------------------------------------------
def view_statistics():

    # validate recipes exist
    if len(recipes) == 0:
        print("No recipes created yet.")
        return
    
#---------------- total recipes

    total_recipes = len(recipes)

#---------------- total completed recipes

    completed_recipes = [completed for completed in recipes if completed["finished_date"] != "N/A"]
    total_completed = len(completed_recipes)

#---------------- recipes completed this month

    now = datetime.now()    
    month_fin_recipes = []
    for finished in completed_recipes:
        
        date_string = now.strftime("%Y-%m-%d %H:%M:%S")       

        recipe_date = finished['finished_date'][:7]
        month_now = date_string[:7]

        if recipe_date == month_now:
            month_fin_recipes.append(finished)
    total_month_finished = len(month_fin_recipes)

#---------------- Highest rated recipe


    rated_recipes = [item for item in recipes if item["rating"] != "N/A"]

    # validate rated exist

    if len(rated_recipes) == 0:
        print("No recipes created yet.")
        return
    
    sorted_rated = sorted(rated_recipes, key=lambda rated_item: rated_item["rating"], reverse=True)
    max_rated = sorted_rated[0]
    max_recipe_name = max_rated['name']

    stats_table = [
        ["Total Recipes", total_recipes],
        ["Total Completed Recipes", total_completed],
        ["Recipes Completed This Month", total_month_finished],
        ["Highest Rated Recipe", max_recipe_name]
    ]

    print("--- Recipe Statistics ---")
    print(tabulate(stats_table, tablefmt="grid"))


#-----------------------------------------------------------------------
#   option [10] mark recipe complete
#-----------------------------------------------------------------------
def mark_complete():
    # show all recipes to select from
    view_recipes()
    
    
    while True:
        try:
            choice = int(input("Select recipe number to delete: "))
            if 1 <= choice and choice <= len(recipes):
                break
            else:
                print("Number out of range. Please try again.")

        except ValueError:
            print("Invalid entry. Please try again.")

    selected_recipe = recipes[choice-1]
    date_string = datetime_now_stamp()
    selected_recipe['finished_date'] = date_string

    print(f'Recipe "{selected_recipe["name"]}" marked complete.')

    # provide rating for finished recipe
    while True:
        try:
            rating = float(input("Select recipe rating (1 to 5 including decimals): "))
            if 0 <= rating and rating <= 5:
                selected_recipe['rating'] = rating
                break
            else:
                print("Number out of range. Please try again.")

        except ValueError:
            print("Invalid entry. Please try again.")



#-----------------------------------------------------------------------
#   option [11] delete recipe
#-----------------------------------------------------------------------
def delete_recipe():
    # show all recipes to select from
    view_recipes()
        
    while True:
        try:
            choice = int(input("Select recipe number to delete: "))
            if 1 <= choice and choice <= len(recipes):
                break
            else:
                print("Number out of range. Please try again.")

        except ValueError:
            print("Invalid entry. Please try again.")

    removed_recipe = recipes.pop(choice-1)
    print(f'Recipe "{removed_recipe["name"]}" deleted.')

    # need to renumber recipes
    # number = len(recipes)+1 wont work here because that was appending into a list. this is looping through a list.

    for index, recipe in enumerate(recipes, start=1):
        recipe["number"] = index

#-----------------------------------------------------------------------
#   option [12] recipe goals
#-----------------------------------------------------------------------
def run_recipe_goal():

#---------------- total completed recipes

    completed_recipes = [completed for completed in recipes if completed["finished_date"] != "N/A"]

#-------- recipes finished this year

    now = datetime.now()    
    year_fin_recipes = []
    for finished in completed_recipes:
        
        date_string = now.strftime("%Y-%m-%d %H:%M:%S")       

        recipe_date = finished['finished_date'][:4]
        year_now = date_string[:4]

        if recipe_date == year_now:
            year_fin_recipes.append(finished)
    total_year_finished = len(year_fin_recipes)   
    
    #-------- determine goal status
    
    current_goal = recipe_goals["year_goal"] 
    if 0 < current_goal:
        if current_goal <= total_year_finished:
            print(f'Recipe goal met! {total_year_finished} recipes finished this year.')
        else:               
            print(f'Recipe goal not met yet. Only {total_year_finished} recipes finished this year.')
    
    #-------- override or user existing goal
    if current_goal > 0:
        print(f"Current yearly recipe completion goal is {current_goal}.")
        while True:            
            answer = input("Override or Continue with goal?: ").lower()

            if answer == "override":
                recipe_goals.clear()                
                break
            elif answer == "continue":
                return
            else:
                print("Invalid option. Please try again.")

    #-------- input recipe goal amount 
    while True:        
        try:
            recipe_goals["year_goal"] = int(input("Enter yearly recipe completion goal: "))
            print(f"Goal of {recipe_goals['year_goal']} recipes entered.")
            break         
        except ValueError:
            print("Invalid number. Please try again.")

#-----------------------------------------------------------------------
#   option [13] CSV export recipes
#-----------------------------------------------------------------------  
def csv_export():
    # validate recipes exist. return and ends function if recipes is empty.
    if not recipes:
        print('No recipes available to export.')
        return

    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")     
    date_now = date_string[:10]

    # encoding="utf-8" is needed for emoji stored in json. utf-8-sig is even better.
    # note that file.write() is not good with commas, quote marks, and spaces. csv.writer() may be better
    with open(f'{date_now} recipes.csv', 'w', newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        writer.writerow([
            "number",
            "favorite",
            "name","description",
            "ingredients",
            "instructions",
            "cook time",
            "difficulty",
            "category",
            "tags",
            "rating",
            "date added",
            "finished date"
            ])
        #file.write("number,favorite,name,description,ingredients,instructions,cook_time,difficulty,category,tags,rating,date added,finished date\n")
        #for recipe in recipes:
            #file.write(f"{recipe['number']},{recipe['favorite']},{recipe['name']},{recipe['description']},{recipe['ingredients']},{recipe['instructions']},{recipe['cook_time']},{recipe['difficulty']},{recipe['category']},{recipe['tags']},{recipe['rating']},{recipe['date_added']},{recipe['finished_date']}\n")
        for recipe in recipes:
            # flatten lists to readable string
            
            ingredients_text = " ; ".join(f"{ingred['ingredient']} ({ingred['amount']})" for ingred in recipe["ingredients"])
                # ";" divides the texts. can use any character
            
            instructions_text = " ; ".join(instr['instruction'] for instr in recipe["instructions"])

            tags_text = " ; ".join(tag['tag'] for tag in recipe["tags"])

            writer.writerow([
                recipe['number'],
                recipe['favorite'],
                recipe['name'],
                recipe['description'],
                ingredients_text,
                instructions_text,
                recipe['cook_time'],
                recipe['difficulty'],
                recipe['category'],
                tags_text,
                recipe['rating'],
                recipe['date_added'],
                recipe['finished_date']
                ])
                
    file_path = os.path.abspath(f'{date_now} recipes.csv')
    print(f"CSV file exported to:\n{file_path}")

#-----------------------------------------------------------------------
#   option [14] Get recipe Recommendation from not finished list
#-----------------------------------------------------------------------
def recipe_recommendation():

    # validate recipes exist. return and ends function if recipes is empty.
    if not recipes:
        print('No recipes available.')
        return
    
    # make list of not finished recipes
    unfinished_recipes = [item for item in recipes if item["finished_date"] == "N/A"]
        
    # make list of unfinished recipes

    
    if unfinished_recipes:
        recommended_recipe = random.choice(unfinished_recipes)
        print(f'Recommending to try the "{recommended_recipe["name"]}" recipe.')
    else:
        recommended_recipe = random.choice(recipes)
        print(f'All recipes are finished. Recommending to try the "{recommended_recipe["name"]}" recipe again')

#-----------------------------------------------------------------------
#   function to write to recipes json
#-----------------------------------------------------------------------
def write_recipe_json():
    with open('recipes.json', 'w') as file:
        json.dump(recipes, file, indent=4)

#-----------------------------------------------------------------------
#   function to write to recipe goals json
#-----------------------------------------------------------------------
def write_recipe_goals_json():
    with open('recipe_goals.json', 'w') as file:
        json.dump(recipe_goals, file, indent=4)

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
        cook_time_sort()                
    elif option == '8':
        search()
    elif option == '9':        
        view_statistics()
    elif option == '10':
        mark_complete()
        write_recipe_json()
    elif option == '11':
        delete_recipe()
        write_recipe_json()
    elif option == '12':
        run_recipe_goal()
        write_recipe_goals_json()
    elif option == '13':
        csv_export()      
    elif option == '14':
        recipe_recommendation() 
    else:
        print("Invalid action. Please try again.")