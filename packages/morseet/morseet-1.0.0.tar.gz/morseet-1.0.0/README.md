# morseet

Morseet is the new and only command line text MORSEEEEEETTT-er! Which means to `morse-it` in my slang, which also sounds like name of a pretty lady. This converts Morse to text, text to morse, Text to text and Morse to Morse. Just kidding!
But you get the point.

## Table of Contents

- [morseet](#morseet)
  - [Previews/Screenshots](#previewsscreenshots)
  - [Installation](#installation)
    - [Homebrew](#homebrew)
    - [Pip Installation](#pip-installation)
    - [Manual installation](#manual-installation)
  - [Configurations](#configurations)
  - [What makes MORSEET different?](#what-makes-morseet-different)
  - [Dependencies](#dependencies)
- [Poem for Morseet](#poem-for-morseet)
  - [Thank you](#thank-you)

## Previews/Screenshots

TBD

## Features

- Text to Morse code converter
- Morse Code to text converter
- Easily unserstand minor bugged morse codes
- SOS signal
- See delayed morse code formation real time
- Input text files and perform conversions
- Amazing color scheme customizability

## Installation

Here are the instructions to download and install your own morseet.

### Homebrew

You can install this command line tool on MacOS using Homebrew by running the command -

```bash
brew install anirudhg07/anirudhg07/morseet
```

If you are facing issues, try -

```bash
brew tap anirudhg07/anirudhg07
brew install morseet
```

### Pip Installation

You can install this command through Pypi by running the command -

```bash
pip install morseet
```

### Manual installation

You can manually install the tool by building from source using the following commands -

```bash
git clone https://github.com/AnirudhG07/morseet
cd morseet
pip install .
```

This should install the command in your machine. If you are facing any issues feel free to raise any issue.

## Configurations

You can have color_schemes as you like for this `MORSEET` command-line tool. Run the below command to open the `config.toml` file in your editor and edit the color_schemes as you wish.

```bash
morseet -c # or --config
```

## What makes MORSEET different?

Unlike other command line tools for converting morse codes, this tool let's you -

- Deal with errors, it will convert the text which makes sense and raise a '?' for the invalid inputs.
- You can have instant SOS signal.
- You can have a custom color scheme for the tool.
- And of course, you can MORSEEEEEEEET!

## Dependencies

- toml

That's it honestly. You can install it using the command -

```bash
pip install toml
```

This will though automatically downloaded with the installation of the tool.

# Poem for Morseet

```
Morseet, Morseet, Morseet
 - .... . / -.-. --- -- -- .- -. -.. / .-.. .. -. . / - --- --- .-..
 .-- .... .. -.-. .... / -.-. --- -. ...- . .-. - ... / -- --- .-. ... . / - --- / - . -..- -
 .- -. -.. / - . -..- - / - --- / -- --- .-. ... .

 .. - .----. ... / - .... . / --- -. .-.. -.-- / - --- --- .-.. / -.-- --- ..- / -. . . -..
 - --- / ... --- ... / .. -. / - .... . / -.. .- .-. -.-
 --- .-. / - --- / -.-. --- -. ...- . .-. - / -.-- --- ..- .-. / -. .- -- .
 - --- / .- / ... . .-. .. . ... / --- ..-. / -.. --- - ...

 --- .... / -- --- .-. ... . . -
 .-- .... . -. / .. / ..- ... . / .-. ..- -. / -.-- --- ..-
 .. / ..-. . . .-.. / .-.. .. -.- . / .- / ... .... .. .--. / -.-. .- .--. - .- .. -.
 ... . -. -.. .. -. --. / ... .. --. -. .- .-.. ... / - --- / - .... . / .-- --- .-. .-.. -..

 -- --- .-. ... . . - --..-- / -- --- .-. ... . . - --..-- / -- --- .-. ... . . -
 - .... . / -.-. --- -- -- .- -. -.. / .-.. .. -. . / - --- --- .-..
 .-- .... .. -.-. .... / -.-. --- -. ...- . .-. - ... / -- --- .-. ... . / - --- / - . -..- -
 .- -. -.. / -- -.-- / .... . .- .-. - / - --- / -- --- .-. ... .
```

## Thank you
