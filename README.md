Blackjack optimal strategy practice. The blackjack games aren't played to completion. You'll only need to get the first action right according to basic blackjack strategy.

Running gui.py will run the game with a GUI. This is also the file that should be used when compiling the game into an app using for example py2app.

Run blackjack.py to get a command line version of the game.

Python 3.12 used. See requirements.txt for libraries.

**Windows compile guide**
Use pyinstaller version 6.7. Navigate to project directory and run "pyinstaller --onefile --windowed --add-data "cards;cards" gui.py".

**Macos compile guide**
Generate a setup.py file using py2applet. You need to recursively include every image file for the cards (figure it out LOL). Then run "python setup.py py2app".
