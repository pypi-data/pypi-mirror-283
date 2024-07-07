# GDI_effects
GDI_effects is a Python library that allows you to create GDI screen effects on Windows.

## Installation
First, you need to install the pywin32 library using pip:
```shell
pip install pywin32
```

After installing pywin32, you can install GDI_effects via pip:
```shell
pip install GDI_effects
```

## Usage
Below is an example of how to use the library to create various screen effects:
```python
from GDI_effects import *
GDI.glitchscreen()
# Creates a glitch effect on the screen.
```

## Available Functions
```python

GDI.BWscreen() # Creates a black and white effect on the screen.

GDI.copyscreen() # continuously copies the entire screen area and displays it without any offset.

GDI.errorscreen() # Displays error icons at various positions on the screen.

GDI.warningscreen() # Displays a warning icon randomly on the screen.

GDI.questionscreen() # Displays a question icon randomly on the screen.

GDI.asteriskscreen() # Displays an asterisk icon randomly on the screen.

GDI.supericonscreen() # displays various system icons randomly on the screen. 

GDI.invertscreen() # Inverts the colors on the screen.

GDI.panscreen() # Pans the screen in random directions.

GDI.Rainbowhell() # Creates random rainbow effects on the screen.

GDI.screenwavy() # Creates a wavy effect on the screen.

GDI.voidscreen() # Creates a void effect on the screen.

GDI.glitchscreen() # Creates a glitch effect on the screen.

GDI.tunnelscreen() # creates a tunnel effect by continuously stretching and copying the screen content inwards from the edges.

Meme.easter_eggs() # secret

```

## Contributing
If you would like to contribute to this project, please fork the repository, create a new branch for your changes, and submit a pull request.