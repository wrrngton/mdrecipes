"""Module for initialising the book"""

import os
import shutil

import click
import toml

from .helpers.file_paths import cli_dir, current_user_dir

# [TODO] DRY all the os.path.joins below!

def init_book():
    """Inits the user book"""
    book_name = click.prompt("What is your book called?")
    author = click.prompt("What is the author's name")
    toml_data = toml.dumps(
        {
            "book": {
                "title": book_name,
                "author": author,
                "directory": os.path.join(current_user_dir(), book_name),
            }
        }
    )

    outpath = os.path.join(current_user_dir(), book_name)
    image = os.path.join(cli_dir(2), "static", "images", "placeholder.webp")

    try:
        os.makedirs(os.path.join(outpath, "content"))
        os.makedirs(os.path.join(outpath, "content", "images"))

        shutil.copyfile(
            os.path.join(cli_dir(2), "static", "images", "placeholder.webp"),
            os.path.
            join(outpath, "content", "images", "placeholder.webp"),
        )

        os.makedirs(os.path.join(outpath, "book"))

        with open(
            os.path.join(outpath, "config.toml"), "w", encoding="utf-8"
        ) as toml_file:
            toml_file.write(toml_data)

    except OSError as e:
        raise click.ClickException(f"error when creating directory: {e}")

    click.echo(
        f"Book successfully created, now run `cd {
            book_name}/content` and start publishing"
    )
