"""Module for initialising the book"""

import os

import click
import toml

from .helpers.file_paths import current_user_dir


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

    try:
        os.makedirs(os.path.join(outpath, "content"))
        os.makedirs(os.path.join(outpath, "book"))
        with open(os.path.join(outpath, "config.toml"), "w", encoding="utf-8") as toml_file:
            toml_file.write(toml_data)

    except Exception as e:
        print(e, "error when creating directory")

    click.echo(
        f"Book successfully created, now run `cd {
            book_name}/content` and start publishing"
    )
