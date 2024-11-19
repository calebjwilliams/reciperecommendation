# Recipe Recommendation

## Project Update 2
For project update, we made the following developments:
  1. Scraped more data from the **allrecipes** website. Instead of navigating to a final recipe page and scrape all data from that one page, we scraped data from mulitple pages and passed through using `meta`
  2. Data cleaning: we removed rows which weren't actually recipes, split up the nutrition column from a dictionary format to separate columns, and included NAs for some of the recipes which did not have rating etc.
  3. Created an outline the interface for the webapp with options for specific ingredient list, allergies, cook time etc.
