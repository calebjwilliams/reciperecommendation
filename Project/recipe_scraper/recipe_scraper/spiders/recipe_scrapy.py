# scrapy crawl allrecipes -o recipes.csv

import scrapy
from scrapy_selenium import SeleniumRequest

class AllRecipesSpider(scrapy.Spider):
    name = 'allrecipes'
    allowed_domains = ['allrecipes.com']
    start_urls = ['https://www.allrecipes.com/recipes-a-z-6735880']
        

    def start_requests(self):
        yield SeleniumRequest(
            url=self.start_urls[0],
            callback=self.parse_index
        )

    def parse_index(self, response):
        # Select links for each type of recipe
        initial_links = response.css('a.mntl-link-list__link::attr(href)').getall()
        categories = response.css('a.mntl-link-list__link::text').getall()
        for link, category in zip(initial_links, categories):
            yield response.follow(link, callback=self.parse_recipe_link, meta={'category': category.strip()})


    def parse_recipe_link(self, response):
        # Extract details for individual recipe pages
        category = response.meta.get('category', 'Unknown')
        recipe_links = response.css('a.comp.mntl-card-list-items::attr(href)').getall()
        for link in recipe_links:
            if 'www.allrecipes.com/article/' not in link and 'www.allrecipes.com/gallery/' not in link:
                yield response.follow(link, callback=self.parse_recipe_page, meta={'category': category})

    def parse_recipe_page(self, response):
        category = response.meta.get('category', 'Unknown')
        title = response.css('h1.article-heading.text-headline-400::text').get(default='').strip()
        total_time = response.css('div.mm-recipes-details__item:contains("Total Time") div.mm-recipes-details__value::text').get()
        prep_time = response.css('div.mm-recipes-details__item:contains("Prep Time") div.mm-recipes-details__value::text').get()
        cook_time = response.css('div.mm-recipes-details__item:contains("Cook Time") div.mm-recipes-details__value::text').get()

        ingredients = []
        for ingredient in response.css('li.mm-recipes-structured-ingredients__list-item'):
            quantity = ingredient.css('span[data-ingredient-quantity="true"]::text').get(default='').strip()
            unit = ingredient.css('span[data-ingredient-unit="true"]::text').get(default='').strip()
            name = ingredient.css('span[data-ingredient-name="true"]::text').get(default='').strip()
            full_ingredient = f"{quantity} {unit} {name}".strip()
            ingredients.append(full_ingredient)
        ingredients = ', '.join(ingredients) if ingredients else "No ingredients listed"

        nutrition_facts = {}
        nutrition_rows = response.css('tbody.mm-recipes-nutrition-facts-summary__table-body tr.mm-recipes-nutrition-facts-summary__table-row')

        for row in nutrition_rows:
            nutrient_value = row.css('td.mm-recipes-nutrition-facts-summary__table-cell.text-body-100-prominent::text').get(default='').strip()
            nutrient_name = row.css('td.mm-recipes-nutrition-facts-summary__table-cell.text-body-100::text').get(default='').strip()
            if nutrient_value and nutrient_name:
                nutrition_facts[nutrient_name] = nutrient_value
 
        serving_info = response.css('p.mm-recipes-serving-size-adjuster__meta::text').get()
        rating = response.css('div.mm-recipes-review-bar__rating::text').get(default='No rating available').strip()
        recipe_link = response.url
        

        yield {
            'category': category,
            'title': title,
            'total_time': total_time,
            'prep_time': prep_time,
            'cook_time': cook_time,
            'ingredients': ingredients,
            'serving_info': serving_info,
            'nutrition_facts': nutrition_facts,  # Added nutrition facts to the output
            'rating': rating,
            'recipe_link': recipe_link
        }


