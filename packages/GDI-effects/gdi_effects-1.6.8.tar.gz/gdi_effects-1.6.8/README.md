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
glitchscreen()
# Creates a glitch effect on the screen.
```

## Available Functions
```python

BWscreen() # Creates a black and white effect on the screen.

errorscreen() # Displays error icons at various positions on the screen.

warningscreen() # Displays a warning icon randomly on the screen.

questionscreen() # Displays a question icon randomly on the screen.

asteriskscreen() # Displays an asterisk icon randomly on the screen.

invertscreen() # Inverts the colors on the screen.

panscreen() # Pans the screen in random directions.

Rainbowhell() # Creates random rainbow effects on the screen.

screenwavy() # Creates a wavy effect on the screen.

voidscreen() # Creates a void effect on the screen.

glitchscreen() # Creates a glitch effect on the screen.

```

## Contributing
If you would like to contribute to this project, please fork the repository, create a new branch for your changes, and submit a pull request.