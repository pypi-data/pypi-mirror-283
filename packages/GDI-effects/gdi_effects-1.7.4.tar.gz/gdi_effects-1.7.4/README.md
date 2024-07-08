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
GDI.glitch_screen()
# Creates a glitch effect on the screen.
```

## Available Functions
```python

GDI.BW_screen() # Creates a black and white effect on the screen.

GDI.copy_screen() # Continuously copies the entire screen area and displays it without any offset.

GDI.error_screen() # Displays error icons at various positions on the screen.

GDI.warning_screen() # Displays a warning icon randomly on the screen.

GDI.question_screen() # Displays a question icon randomly on the screen.

GDI.asterisk_screen() # Displays an asterisk icon randomly on the screen.

GDI.super_icon_screen() # displays various system icons randomly on the screen. 

GDI.invert_screen() # Inverts the colors on the screen.

GDI.pan_screen() # Pans the screen in random directions.

GDI.Rainbow_blink() # Creates random rainbow effects on the screen.

GDI.screen_wavy() # Creates a wavy effect on the screen.

GDI.void_screen() # Creates a void effect on the screen.

GDI.glitch_screen() # Creates a glitch effect on the screen.

GDI.tunnel_screen() # Creates a tunnel effect by continuously stretching and copying the screen content inwards from the edges.

twisted_screen() # Apply a twisted screen effect by performing bitwise operations on the screen content.

Meme.easter_eggs() # Secret

```

## Contributing
If you would like to contribute to this project, please fork the repository, create a new branch for your changes, and submit a pull request.