import toml
from morse_dict import morse_dict, reverse_morse_dict
import os

def space_char():
    """
    Opens up config.toml file and reads the space character number
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, "config.toml")

    with open(config_path, "r") as f:
        config = toml.load(f)
    # Access the settings
    space = ""
    space_num = config["settings"]["space_char"]
    if space_num != 1:
        space = "......."
    else:
        space = "/"
    return f" {space} "


def text_to_morse(sent: str):
    """
    This function changes any sent to its morse_code
    """
    morsed_sent = ""
    space = space_char()
    err = 0
    invalid_input = set()
    for char in sent:
        if char.lower() in morse_dict or char in [" ", "\n", "\t", "\r"]:
            if char not in [" ", "\n", "\t", "\r"]:
                morsed_sent += morse_dict[char.lower()] + " "
            else:
                morsed_sent += space
        else:
            invalid_input.add(char)
            err = 1
            morsed_sent += " ? "

    return morsed_sent, err, invalid_input


def morse_to_text(morse: str):
    """
    This function converts any morse 1 sent to english text
    """
    text = ""
    err = 0
    invalid_input = set()
    for part in morse.split():
        if part in reverse_morse_dict or part in ["/", ".......", "\n", "\t", "\r"]:
            if part in ["/", "......."]:
                text += " "
            elif part in ["\n", "\t", "\r"]:
                text += part
            else:
                text += reverse_morse_dict[part]
        else:
            text += " ? "
            err = 1
            invalid_input.add(part)

    return text, err, invalid_input
