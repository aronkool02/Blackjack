# Overview

Blackjack optimal strategy practice. The blackjack games aren't played to completion. You'll only need to get the first action right according to basic blackjack strategy.

Running gui.py will run the game with a GUI. This is also the file that should be used when compiling the game into an app using for example py2app or pyinstaller.

Run blackjack.py to get a command line version of the game.

Python 3.12 used. See requirements.txt for libraries.

# Compiling

## Windows compile guide
Use pyinstaller version 6.7. Navigate to project directory and run:
```bash
pyinstaller --onefile --windowed --add-data "cards;cards" gui.py
```

## MacOS compile guide
Generate setup.py using py2applet. You need to modify setup.py to recursively include every .png for the cards (figure it out LOL). Then run:
```bash
python setup.py py2app
```

## Installation

To install the required packages, run the following command:
```sh
pip install -r requirements.txt
