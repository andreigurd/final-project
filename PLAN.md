markdown

# Recipe List Project Plan

## Data Structure
Each recipe will be a dictionary with:
- Recipe number (to avoid needing to enumerate lists later)
- mark favorite with a star
- name/title
- description
- ingredients (list)
- instructions (multiple items so make a list)
- cook time
- diffuculty
- category
- hashtag/ tag
- rating (allow decimal ratings)
- status (Not Completed/Completed)(maybe status is indicated by green or red color recipe name)
- date added

## Features
look into displaying tables with each word capitalized even if stored lower case. also center all words.
0. Exit
1. Add recipe
2. View all recipes
3. View by tag
4. view by diffuculty
5. view by cook time ( then have under 30 min, under 1 hour, 2 hour +)
6. Sort by rating
7. Sort by cook time
8. Search
9. Start Recipe (with Auto mark complete)
10. View Recipe statistics ( Total recipes, Highest rated recipe, recipes completed this month, total completed)
11. Delete recipe
12. Export to CSV file.
13. Get Recipe Recommendation (from not completed list)
14. Save/load from JSON

## Files
- recipes.py (main program)
- recipe.json (data storage)
- README.md (documentation)