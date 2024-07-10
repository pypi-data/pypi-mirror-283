import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import argparse
import subprocess
from entry import *

def main():
    ## Handle input flags
    parser = argparse.ArgumentParser(
        description="Morseet Morseet Morseeeeeeet!!! Convert Morse Code to Text and Text to Morse Code!",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    # Add the flags
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="Morseet - version 1.0.0",
        help="Show the version of the program and exit.",
    )
    parser.add_argument(
        "-c",
        "--config",
        action="store_true",
        help="Open the Configuration file in $EDITOR.",
    )
    parser.add_argument(
            "-r",
            "--read",
            metavar="FILE",
            type=str,
            help="Read the specified input file and convert.",
        )

    args = parser.parse_args()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to config.toml in the same directory
    config_path = os.path.join(script_dir, "config.toml")
    # Check if the config flag was used
    if args.config:
        # Get the default editor from the environment variable
        editor = os.getenv("EDITOR", "nano")  # Default to nano if EDITOR is not set
        # Open the config.toml file in the editor
        subprocess.run([editor, config_path])

    elif args.read:
        # Read the content of the specified input file
        input_file_path = args.read
        try:
            with open(input_file_path, 'r') as file:
                file_content = file.read()
            # Pass the file content to the entry function
            exit_code = file_entry(file_content)
        except FileNotFoundError:
            print(f"Error: The file '{input_file_path}' does not exist.")
            exit_code = 1
    else:
        # Call the entry function if the -c flag is not used
        exit_code = entry()
if __name__ == "__main__":
    main()