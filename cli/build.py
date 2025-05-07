"""Builds static files and pushes to /book"""

import os

import click
import markdown
from jinja2 import Environment, FileSystemLoader

from .helpers.check_recipe_validity import are_recipes_duped, is_recipe_valid
from .helpers.copy_images import copy_user_images
from .helpers.file_paths import cli_dir
from .helpers.get_readme import get_user_readme
from .helpers.get_recipes import (get_user_readmes, get_user_recipes,
                                  get_user_tags)
from .helpers.get_static_files import get_user_static_files
from .helpers.load_config import get_user_config

config = get_user_config()

# Isolated function to prevent failure when module is imported and config
# cannot be found - need to fix


def get_path_info():
    """Returns the path info for later use"""

    here = cli_dir(2)
    template_path = os.path.join(here, "templates")
    env = Environment(loader=FileSystemLoader(template_path))

    recipe_directory = os.path.join(config["book"]["directory"], "content")
    recipe_out_directory = os.path.join(config["book"]["directory"], "book")
    content_directory = os.path.join(config["book"]["directory"], "content")

    return (recipe_directory, recipe_out_directory, env, content_directory)


def push_file(file_content, file_name, directory=""):
    """Pushes the files to /book"""
    out_dir = get_path_info()[1]
    full_out_path = os.path.join(out_dir, directory, file_name)
    with open(full_out_path, "w", encoding="utf-8") as f:
        f.write(file_content)


# def build_category_page(category):


def build_book():
    """Compiles the book"""

    template_env = get_path_info()[2]
    outpath = get_path_info()[1]

    # Recipes are returned as an array of categories, with subarrays of recipes
    recipes = get_user_recipes()
    readmes = get_user_readmes()
    tags = get_user_tags(recipes)
    settings = config["settings"]

    for cat, cat_recipes in recipes.items():
        # # Build cat pages
        # build_category_page(cat)

        os.makedirs(os.path.join(outpath, cat), exist_ok=True)
        # no_recipe_dupes = are_recipes_duped(cat_recipes)

        for recipe in cat_recipes:
            is_valid = is_recipe_valid(recipe)

            if is_valid is False:
                raise click.ClickException(
                    "Recipes are expected to have at least '## Ingredients' and '## Instructions'\nThe book was not built"
                )

            recipe_html = markdown.markdown(recipe["content"])
            recipe_template = template_env.get_template("recipe.html")
            recipe_output = recipe_template.render(
                title=recipe["title"],
                tags=recipe["tags"],
                image=recipe["image"],
                content=recipe_html,
                recipes=recipes,
                configuration=settings,
            )
            push_file(recipe_output, recipe["filename"], cat)

    for cat, cat_readme in readmes.items():

        os.makedirs(os.path.join(outpath, cat), exist_ok=True)

        for readme in cat_readme:

            if is_valid is False:
                raise click.ClickException(
                    "Recipes are expected to have at least '## Ingredients' and '## Instructions'\nThe book was not built"
                )

            readme_template = template_env.get_template("catindex.html")
            category_recipes = [f for r, f in recipes.items() if r == cat][0]
            readme_output = readme_template.render(
                icon=readme["icon"],
                image=readme["image"],
                description=readme["description"],
                title=cat,
                recipes=recipes,
                configuration=settings,
                recipes_in_cat=category_recipes,
            )
            push_file(readme_output, readme["filename"], cat)

    # Build tags
    os.makedirs(os.path.join(outpath, "tags"), exist_ok=True)

    for tag, tag_data in tags.items():
        tag_template = template_env.get_template("tagindex.html")
        tag_output = tag_template.render(
            title=tag, tag_recipes=tag_data, recipes=recipes, configuration=settings
        )

        push_file(tag_output, f"{tag}.html", os.path.join(outpath, "tags"))

    # Build readme
    readme = get_user_readme()
    readme_html = markdown.markdown(readme)

    # Build index.html
    homepage_template = template_env.get_template("homepage.html")
    homepage_output = homepage_template.render(
        title="Homepage",
        recipes=recipes,
        intro_content=readme_html,
        configuration=settings,
    )
    push_file(homepage_output, "index.html")

    # Build style.css
    stylesheet_content = get_user_static_files("stylesheet")
    push_file(stylesheet_content, "style.css")

    # Build index.js
    script_content = get_user_static_files("javascript")
    push_file(script_content, "script.js")

    # Build index.js
    script_content = get_user_static_files("lunr")
    push_file(script_content, "lunr.js")

    # Copies images over to /book/images
    copy_user_images()

    # Finished building book
    click.echo("finished building book")
