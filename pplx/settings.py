import os
import json


SETTINGS = {
    "FOLDER_PATH": '',
    "DELIMITER": '-/'
}


def set_settings(key: str, value: str):
    global FOLDER_PATH
    global DELIMITER
    if key in SETTINGS:
        SETTINGS[key] = value
    else:
        raise Exception(f'Invalid key: {key}')
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'), 'w') as file:
        json.dump(SETTINGS, file, indent=4)


with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'), 'r') as file:
    SETTINGS = json.load(file)
