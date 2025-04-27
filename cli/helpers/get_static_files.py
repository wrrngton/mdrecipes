""" Returns static file content """

import os

from .file_paths import cli_dir


# Returns content of requested file
def get_user_static_files(requested_file) -> str:
    """ Returns user's static files """

    user_dir = cli_dir(2)
    file_name = ""

    if requested_file == "stylesheet":
        file_name = "style.css"
    elif requested_file == "javascript":
        file_name = "script.js"
    elif requested_file == "lunr":
        file_name = "lunr.js"

    with open(os.path.join(user_dir, "static", file_name), "r", encoding="utf-8") as f:
        return f.read()


