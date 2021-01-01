import os
from PIL import Image
from flask import current_app


def add_profile_pic(pic_upload, username) -> str:
    """
    Handler function for dealing with picture upload.

    :param pic_upload: The uploaded picture.
    :param username: The username of the user.
    :return: The filepath of the picture.
    """
    filename = pic_upload.filename
    # "mypicture" . "jpg"
    extension_type = filename.split(".")[-1]
    storage_filename = str(username) + "." + extension_type
    filepath = os.path.join(current_app.root_path, "static", "profile_pics",
                            storage_filename)
    output_size = (200, 200)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename
