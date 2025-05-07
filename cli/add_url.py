import json
import os

import markdown
import requests
import validators
from bs4 import BeautifulSoup
from click import ClickException
from jinja2 import Environment, FileSystemLoader

from .build import build_book, get_path_info, push_file
from .helpers.get_recipes import get_user_recipes
from .helpers.load_config import get_user_config

# ---
# title: "recipe4"
# tags: ["quick", "weekend"]
# image: "pic.jpg"
# ---
#
# ## Ingredients
#
# - 2 apples
# - 5 garlic cloes
# - rice
# - rhubarb
#
# ## Instructions
#
# 1. Step 1
# 2. Step 2
# 3. Step 3
# 4. Step 4


def create_content(recipe, tags):
    ingredients_str = "## Ingredients\n"
    instructions_str = "## Instructions\n"

    rec_tags = tags.split(",") if tags else []
    title = recipe["name"]

    markdown = f"---\ntitle: {title}\ntags: {
        rec_tags}\nimage: 'https://placehold.co/600x400'\n---\n"

    for instruction in recipe["recipeInstructions"]:
        instructions_str = instructions_str + f"- {instruction["text"]}\n"

    for ingredient in recipe["recipeIngredient"]:
        ingredients_str = ingredients_str + f"- {ingredient}\n"

    return markdown + ingredients_str + instructions_str


def add_url(url, filename, category, tags):
    print("hitting")
    new_recipe_dict = {}
    cat = category if category is not None else "nocategory"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    is_url = validators.url(url)
    html = ""
    if not is_url:
        raise ClickException("You didn't provide a proper url")

    try:
        document = requests.get(url, headers=headers)
        html = document.text

    except Exception as e:
        raise ClickException(f"Error requesting the url: {e}")

    soup = BeautifulSoup(html, "html.parser")
    schema_script = soup.select(".yoast-schema-graph")[0]
    schema_json_str = schema_script.get_text()
    schema_json = json.loads(schema_json_str)
    schema_json_graph = schema_json["@graph"]

    template_env = get_path_info()[2]
    outpath = get_path_info()[3]
    out_cat_path = os.path.join(outpath, cat)
    named_file = f"{filename}.md"
    content = ""

    for item in schema_json_graph:
        if item["@type"] == "Recipe":
            content = create_content(item, tags)

            # new_recipe_dict = {
            #     "title": item["name"],
            #     "category": cat,
            #     "image": item["image"][0],
            #     "tags": tags,
            #     "content": content,
            # }

    push_file(content, named_file, out_cat_path)

    # Build new recipe and directory if needed
    # template_env = get_path_info()[2]
    # outpath = get_path_info()[3]
    # out_cat_path = os.path.join(outpath, cat)
    # print(out_cat_path)
    #
    # try:
    #     os.makedirs(out_cat_path, exist_ok=True)
    # except Exception as e:
    #     print(f"error {e}")
    #
    # all_recipes = get_user_recipes()
    # config = get_user_config()
    # settings = config["settings"]
    # named_file = f"{filename}.md"
    #
    # print()

    # recipe_output = recipe_template.render(
    #     title=new_recipe_dict["title"],
    #     tags=new_recipe_dict["tags"],
    #     image=new_recipe_dict["image"],
    #     content=recipe_html,
    #     recipes=all_recipes,
    #     configuration=settings,
    # )
    #
    # push_file(recipe_output, named_file, directory=out_cat_path)
