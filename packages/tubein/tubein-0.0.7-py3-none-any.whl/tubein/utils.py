import os
import re


EMPTY_ANNOTATION_FILE = (
    '<?xml version="1.0" encoding="UTF-8" ?>'
    "<document><annotations></annotations></document>"
)


def sanitize_identifier(identifier, replacement="-"):
    return re.sub(r"[^\w-]", replacement, identifier)


def get_itemname(infodict, new_item_id=None):
    # Remove illegal characters in identifier
    # use update_id to replace the id with a new id, if present
    return sanitize_identifier(
        "%s" % (update_id(infodict.get("display_id"), new_item_id),)
    )


def check_is_file_empty(filepath):
    """
    Check whether file is empty or not.

    :param filepath:  Path of a file that will be checked.
    :return:          True if the file empty.
    """
    if os.path.exists(filepath):
        return os.stat(filepath).st_size == 0
    else:
        raise FileNotFoundError("Path '%s' doesn't exist" % filepath)


def update_extractor(extractor, new_item_id):
    # change extractor to 'youtube' for standard IA naming
    # if yt-dlp youtube extractor used OR --new-item-id option used
    # example: 'youtube+oath2' OR 'bitchute' becomes 'youtube'
    if extractor.startswith("youtube+") or new_item_id is not None:
        return "youtube"
    else:
        return extractor


def update_id(id, new_item_id):
    # change id to new_item_id if not None
    if new_item_id is not None:
        return new_item_id
    else:
        return id


def get_content_type(file, content_type=None):
    imageExtensionsToCheck = ["jpg", "webp"]
    videoExtensionsToCheck = ["webm", "mp4", "ogv", "mkv"]
    file_name, file_extension = os.path.splitext(file)
    if file_extension[1:] in imageExtensionsToCheck:
        content_type = "image/" + file_extension[1:]
    elif file_extension[1:] in videoExtensionsToCheck:
        content_type = "video/" + file_extension[1:]
    elif file_extension[1:] == "json":
        content_type = "application/json"
    return content_type


def ac_object_exist(client, s3_bucket, itemname: str) -> bool:
    objects = client.list_objects(s3_bucket, prefix=itemname)
    if any(True for _ in objects):
        return True
