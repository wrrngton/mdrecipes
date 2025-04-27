import os
from .load_config import get_user_config

def get_user_readme():
    config = get_user_config()
    readme_file = os.path.join(config["book"]["directory"], "content", "README.md")
    with open(readme_file, "r") as f:
        readme_content = f.read()

    return readme_content



