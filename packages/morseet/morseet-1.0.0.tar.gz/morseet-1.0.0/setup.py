import gzip
import os
import platform
import shutil

from setuptools import find_packages, setup


def install_man_page():
    source_path = os.path.join("docs", "man", "morseet.1")
    dest_path = os.path.join("/usr/local/", "share", "man", "man1", "morseet.1.gz")

    # Compress the man page
    with open(source_path, "rb") as src, gzip.open(dest_path, "wb") as dst:
        shutil.copyfileobj(src, dst)


description = """
# morseet
morseet(slang for morse-it) is a command line tool to convert text to morse-code and vice versa. It has various features and customization options making it the only tool
you would go to. 

# Features

- Text to Morse code converter
- Morse Code to text converter
- Easily unserstand minor bugged morse codes
- SOS signal
- See delayed morse code formation real time
- Amazing color scheme customizability

# Installation
To install morseet, please fulfill the dependicies and run the following command:
```bash
pip install morseet
```
To run the command, run the following command:
```bash
morseet
```
And you are good to go!

## Dependencies
- toml
- Other python libraries which will be installed automatically

Visit the Github Repository for more details: https://github.com/AnirudhG07/morseet

# Version
1.0.0

# Note:
1) The tool is developed using Python.
2) This tools is crossplatform for MacOS, Linux, Windows, etc.

"""

setup(
    name="morseet",
    version="1.0.0",
    description="morseet, is a command-line tool to convert morse code to text and vice versa.",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/AnirudhG07/morseet",
    author="Anirudh Gupta",
    package_data={
        'morseet': ['config.toml'],
    },
    packages=find_packages(),
    install_requires=["toml"],
    keywords=["terminal", "Morse Code converted", "Encryption", "CLI"],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "morseet=morseet.main:main",
        ],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
    ],
)

