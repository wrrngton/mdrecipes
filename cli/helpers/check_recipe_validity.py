def is_recipe_valid(recipe_dict: dict) -> bool:
    """ Checks recipe validity """
    recipe_content = recipe_dict["content"].lower()

    if "## ingredients" not in recipe_content or "## ingredients" not in recipe_content:
        return False

    return True


# def is_readme_valid(readme: dict) -> bool:
#     """ Checks readme validity """
#
#     for key, _ in readme:
#
#
#     return True
#     pass


def are_recipes_duped(recipes: dict) -> bool:
    duplicates = []
    seen = set()

    for recipe in recipes:
        if recipe["title"] in seen:
            duplicates.append(recipe["title"])
        else:
            seen.add(recipe["title"])
