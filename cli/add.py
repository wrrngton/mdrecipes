import requests
import json
import validators
from bs4 import BeautifulSoup
from click import ClickException

def create_content(recipe):
    ingredients_str = "## Ingredients\n"
    instructions_str = "## Instructions\n"
    
    for instruction in recipe["recipeInstructions"]:
        instructions_str = instructions_str + f"- {instruction["text"]}\n"

    for ingredient in recipe["recipeIngredient"]:
        ingredients_str = ingredients_str + f"- {ingredient}\n"

    return ingredients_str + instructions_str


def add_recipes(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    is_url = validators.url(url)
    html = ""
    if not is_url:
        raise ClickException("You didn't provide a proper url")

    try:
        document = requests.get(url, headers=headers)
        html = document.text

    except Exception as e:
        raise ClickException("Error requesting the url")
    
    soup = BeautifulSoup(html, 'html.parser')
    schema_script = soup.select(".yoast-schema-graph")[0]
    schema_json_str = schema_script.get_text()
    schema_json = json.loads(schema_json_str)
    schema_json_graph = schema_json["@graph"] 
    
    for item in schema_json_graph:
        if item["@type"] == "Recipe":
            content = create_content(item)
            print( { 
                "title": item["name"],
                "tags": [],
                "content": content

            })

    recipe_dict = {
        
    }
    # print(schema_jsonx)
        # recipe_dict = {
        #     "title": post["title"],
        #     "tags": post["tags"],
        #     "content": post.content,
        #     "filename": file_name.replace(".md", ".html"),
        #     "image": post["image"],
        #     "category": cat
        # }


    # html = document.text
    #
    # soup

    # print("not reaching")
