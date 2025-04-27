import toml
import os
from .file_paths import current_user_dir

def get_user_config():
    config_file_path = os.path.join(current_user_dir(), "config.toml")

    with open(config_file_path, "r") as f:
        config_data = toml.loads(f.read())
        return config_data
