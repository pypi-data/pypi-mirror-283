from convert import morse_to_text, text_to_morse
import toml 
import time
import os

welcome = "Welcome to Morse Code Translator. Input the below options to get started:"
option1 = "Text to Morse Code:"
option2 = "Morse Code to Text:"
option3 = "SOS Signal"
option4 = "See morse code with delay"
option5 = "Exit"
select_option = "Select an number among above options: "

error_dict = {
    0: "No err",
    1: "Invalid input character",
}

greetings = """
                                    _
 _ __ ___   ___  _ __ ___  ___  ___| |_
| '_ ` _ \\ / _ \\| '__/ __|/ _ \\/ _ \\ __|
| | | | | | (_) | |  \\__ \\  __/  __/ |_
|_| |_| |_|\\___/|_|  |___/\\___|\\___|\\__|
"""

dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, "config.toml")

def format(text:str, code) -> str:
    """
    This function formats the text to be printed
    """
    return f"\033[{code}m{text}\033[0m"

def entry():
    with open(config_path, "r") as f:
        config = toml.load(f)
    # Access the color_schemes
    greet_col = config["color_schemes"]["greeting"]
    mains = config["color_schemes"]["main_strings"]
    option_nums = config["color_schemes"]["option_nums"]
    option_text = config["color_schemes"]["option_text"]
    error_ = config["color_schemes"]["error"]
    success = config["color_schemes"]["success"]

    ####
    print(format(greetings, greet_col))
    print(format(welcome, mains))
    print(f"{format('[1]', option_nums)}", format(option1, option_text))
    print(f"{format('[2]', option_nums)}", format(option2, option_text))
    print(f"{format('[3]', option_nums)}", format(option3, option_text))
    print(f"{format('[4]', option_nums)}", format(option4, option_text))
    print(f"{format('[5]', option_nums)}", format(option5, option_text))

    option = 0
    while True:
        option = int(input(f"\n{select_option}"))
        if 1 <= option <= 5:
            break
        else:
            print(format("Invalid option. Please select an option among 1, 2 or 3.", error_))

    assert 1<= option <= 5, "Invalid option. Option must be 1 to 5"

    error, invalid, output = "No err", set() , ""
    while option != 5:
        if str(option) == "1" or str(option) == "4":
            input_sent = input("Enter English text: ")
            output, err, invalid = text_to_morse(input_sent)
            error = error_dict[err]
            break
        elif str(option) == "2": 
            input_morse = input("Enter Morse code: ")
            output, err, invalid = morse_to_text(input_morse)
            error = error_dict[err]
            break
        elif str(option) == "3":
            output, err, invalid = text_to_morse("SOS")
            error = error_dict[err]
            print(output)
            print(format("\nEmergency exiting! SOS Signal is alarmed. ", error_))
            return 0

    if option == 5:
        print(format("\nThank you for using Morseeeeet! Goodbye!", success))
        return 0
    
    if option == 4:
        delay_unit = config["settings"]["delay_unit"]
        for char in output:
            print(char, end="", flush=True)
            if char == ".":
                time.sleep(delay_unit)
            elif char == "-":
                time.sleep(3*delay_unit)
            else: ## Space
                time.sleep(7*delay_unit)
        print("\n")
    else:
        print(output)

    if error != error_dict[0]:
        print(format(f"\nError: {error} occurred", error_))
        print("Invalid inputs characters received: ", invalid)
    
    replay = input(format("\nWould you like to morseet more? (y/n) ", greet_col))
    if replay.lower() == "y" or replay.lower() == "yes":
        entry()
    elif replay.lower() == "n" or replay.lower() == "no":
        print(format("\nThank you for using Morseeeeet! Goodbye!", success))
    else:
        print(format("Invalid input. Exiting... Goodbye!", error_))

    return 0

def file_entry(file_content: str) -> int:
    with open(config_path, "r") as f:
        config = toml.load(f)
    # Access the color_schemes
    greet_col = config["color_schemes"]["greeting"]
    mains = config["color_schemes"]["main_strings"]
    option_nums = config["color_schemes"]["option_nums"]
    option_text = config["color_schemes"]["option_text"]
    error_ = config["color_schemes"]["error"]
    success = config["color_schemes"]["success"]

    print(format(greetings, greet_col))
    print(format("Welcome to Morse Code Translator. Your input file is successfully been inputted. Select an option: ", mains))

    print(f"{format('[1]', option_nums)}", format(option1, option_text))
    print(f"{format('[2]', option_nums)}", format(option2, option_text))
    print(f"{format('[3]', option_nums)}", format(option3, option_text))
    print(f"{format('[4]', option_nums)}", format("Exit", option_text))

    option = 0
    while True:
        option = int(input(f"\n{select_option}"))
        if 1 <= option <= 4:
            break
        else:
            print(format("Invalid option. Please select an option among 1 to 4.", error_))

    assert 1<= option <= 4, "Invalid option. Option must be 1 to 4"

    error, invalid, output = "No err", set() , ""
    while option != 4:
        if str(option) == "1":
            output, err, invalid = text_to_morse(file_content)
            error = error_dict[err]
            break
        elif str(option) == "2": 
            output, err, invalid = morse_to_text(file_content)
            error = error_dict[err]
            break
        elif str(option) == "3":
            output, err, invalid = text_to_morse("SOS")
            error = error_dict[err]
            print(output)
            print(format("\nEmergency exiting! SOS Signal is alarmed. ", error_))
            return 0

    if str(option) == "4":
        print(format("\nThank you for using Morseeeeet! Goodbye!", success))
        return 0

    print(output)
    if error != error_dict[0]:
        print(format(f"\nError: {error} occurred", error_))
        print("Invalid inputs characters received: ", invalid)
    
    replay = input(format("\nWould you like to morseet more? (y/n) ", greet_col))
    if replay.lower() == "y" or replay.lower() == "yes":
        entry()
    elif replay.lower() == "n" or replay.lower() == "no":
        print(format("\nThank you for using Morseeeeet! Goodbye!", success))
    else:
        print(format("Invalid input. Exiting... Goodbye!", error_))

    return 0