import os
import pathlib

import click
import frontmatter

from .load_config import get_user_config

# from .check_recipe_validity import is_readme_valid

VALID_README_KEYS = ["icon", "image", "description"]
user_path = get_user_config()["book"]["directory"]
recipes_path = os.path.join(user_path, "content")


def loop_files(path) -> list:
    files = os.listdir(path)

    # Error is folder does not contain README (categories must contain one)
    if "README.md" not in files:
        raise click.ClickException("Category folders must contain a README.md")

    recipe_files = []
    readme_files = []

    for file in files:
        # README is handled elsewhere
        if file != "README.md" and pathlib.Path(file).suffix == ".md":
            recipe_files.append(os.path.join(path, file))
        elif file == "README.md":
            readme_files.append(os.path.join(path, file))

    return (
        readme_files,
        recipe_files,
    )


def traverse_directories():
    """Checks content/ dir for sub folder"""

    # init obj of classified recipes and category indexes
    recipes_in_folders = {}
    readmes_in_folders = {}
    tags_with_recipes = []

    # Get list of subdirectories and top level recipes
    subfolders = [f.path for f in os.scandir(recipes_path) if f.is_dir()]
    top_level_recipes = [
        f
        for f in os.listdir(recipes_path)
        if pathlib.Path(os.path.join(recipes_path, f)).suffix == ".md"
        and f != "README.md"
    ]

    # If there are top level recipes not in a folder, add them to dict
    if top_level_recipes:
        recipes_in_folders["nocategory"] = []

        # Loop top level recipes that aren't in folders
        for recipe in top_level_recipes:
            single_recipe_path = os.path.join(recipes_path, recipe)
            recipes_in_folders["nocategory"].append(single_recipe_path)

    # Loop recipes in subdirectories
    for folder in subfolders:
        folder_name = os.path.basename(folder)
        if folder_name == "images":
            continue

        # If subfolders exist, throw an error, we only allow 1 level of subfolders
        sub_subfolders = [
            f.path for f in os.scandir(os.path.join(recipes_path, folder)) if f.is_dir()
        ]

        if sub_subfolders:
            raise click.ClickException("Recipe folders cannot have subfolders")

        readme_list, recipes_list = loop_files(folder)
        readmes_in_folders[folder_name] = readme_list
        recipes_in_folders[folder_name] = recipes_list

    return (readmes_in_folders, recipes_in_folders)


def extract_recipe_data(recipe, cat):
    """Extracts recipe data"""
    with open(recipe, "r", encoding="utf-8") as f:
        post = frontmatter.loads(f.read())

        # Extract just the file name, we don't need the full path
        file_name = os.path.basename(recipe)

        # Create recipe object
        recipe_dict = {
            "title": post["title"],
            "tags": post["tags"],
            "content": post.content,
            "filename": file_name.replace(".md", ".html"),
            "image": post["image"],
            "category": cat
        }

        return recipe_dict


def extract_readme_data(readme):
    """Extracts readme data"""
    with open(readme, "r", encoding="utf-8") as f:
        metadata, _ = frontmatter.parse(f.read())

        for key, _ in metadata.items():
            if key not in VALID_README_KEYS:
                raise click.ClickException(
                    "readme frontmatter can only contain specific keys, mdrecipes --help"
                )

        # Create readme object
        readme_dict = {
            "icon": metadata["icon"],
            "image": metadata["image"],
            "description": metadata["description"],
            "filename": "index.html",
        }
        return readme_dict


def get_user_recipes():
    """Gets a list of user recipes"""

    _, categorised_recipes = traverse_directories()

    for cat, recipes in categorised_recipes.items():
        new_arr = [extract_recipe_data(f, cat) for f in recipes]
        categorised_recipes[cat] = new_arr

    return categorised_recipes


def get_user_readmes():
    """Gets a list of user category readmes"""
    categorised_readmes, _ = traverse_directories()

    for cat, readmes in categorised_readmes.items():
        new_arr = [extract_readme_data(f) for f in readmes]
        categorised_readmes[cat] = new_arr

    return categorised_readmes


def get_user_tags(recipes) -> dict:
    recipes_dict = {}

    def loop_tags(tags, recipe):
        for tag in tags:
            if tag not in recipes_dict:
                recipes_dict[tag] = []
            if tag in recipes_dict:
                recipes_dict[tag].append(recipe)

    for key in recipes:
        for recipe in recipes[key]:
            loop_tags(recipe["tags"], recipe)

    return recipes_dict
