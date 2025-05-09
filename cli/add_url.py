import json
import os

import requests
import validators
import click
from bs4 import BeautifulSoup
from click import ClickException

from .build import get_path_info, push_file


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

    outpath = get_path_info()[3]
    
    # Make directory for category, if exists, do nothing
    out_cat_path = os.path.join(outpath, cat)
    
    try:
        os.makedirs(out_cat_path, exist_ok=True)
    except OSError as e:
        print(f"Failed to create directory: {e}")

    named_file = f"{filename}.md"
    content = ""

    for item in schema_json_graph:
        if item["@type"] == "Recipe":
            content = create_content(item, tags)

    push_file(content, named_file, out_cat_path)
    click.echo("Recipe successfully added, go /content to further edit")
