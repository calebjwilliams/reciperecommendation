# Recipe Recommendation

## Project Update 2
For project update, we made the following developments:
  1. Scraped more data from the **allrecipes** website. Instead of navigating to a final recipe page and scrape all data from that one page, we scraped data from mulitple pages and passed through using `meta`.
  2. Data cleaning: we removed rows which weren't actually recipes, split up the nutrition column from a dictionary format to separate columns, and included NAs for some of the recipes which did not have rating etc.
  3. Created an outline the interface for the webapp with options for specific ingredient list, allergies, cook time etc.


## Project Description
The Recipe Recommendation Web App is designed to help users easily find recipes based on the ingredients they have at home and their specific nutritional goals. The app addresses two major challenges in meal planning: ingredient-based recipe discovery and nutrition tracking. The first feature allows users to input the ingredients they currently have in their kitchen or specify a type of meal (e.g., “chicken and rice”), and the app generates a list of recipes that can be made with those ingredients. This helps users minimize food waste by utilizing available ingredients. The second feature is focused on users’ nutritional goals. Users can set specific dietary parameters, such as maximum calorie count or minimum protein intake, and the app will suggest recipes that meet those criteria, ensuring users stay on track with their health goals. 

The app’s user interface is designed to be intuitive and interactive, enabling users to easily input ingredients, dietary restrictions, and meal preferences. The app connects to a recipe database, which contains detailed information on each recipe, including nutritional data. Users can browse through a list of recipe recommendations that are ranked based on user ratings and relevance to their inputs. They can then select a recipe based on factors like taste preferences, nutritional fit, or ingredient availability. Once a recipe is chosen, users can click on a link to view the full recipe page, which includes step-by-step instructions, ingredient quantities, and nutritional breakdown.
