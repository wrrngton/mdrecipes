"""Copies files from content dir to /book/images"""

import os
import shutil

from .load_config import get_user_config


def copy_user_images() -> bool:
    user_dir = get_user_config()["book"]["directory"]
    images_dir = os.path.join(user_dir, "content", "images")
    out_dir = os.path.join(user_dir, "book", "images")

    outdir_exists = os.path.isdir(out_dir)

    if images_dir is None:
        return

    if outdir_exists is False:
        os.mkdir(out_dir)

    images = os.listdir(images_dir)

    for image in images:
        full_image_path = os.path.join(images_dir, image)
        out_path = os.path.join(out_dir, image)
        shutil.copy(full_image_path, out_path)
