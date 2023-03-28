# NeighbourHoot Prototype Functionality 

The project makes an attempt at gamifying the concept of community exchange, which aims to lessen environmental clutter while engaging community with passive ways of sustainable behaviour. 

The code presented in these files describes the functional aspects of the prototype for the project.


## Deployment

To deploy this project run (on two different terminal panels)

```bash
python3 Doorcode.py
python3 NeighbourHoot.py
```

## Dependencies

```python
from gpiozero import Button 
from signal import pause 
import pygame, pygame.mixer
import os
import time
import fcntl
import serial
```


## Files

#### doorcode.py

This file contains code that handles door opening and closing notification.

Whenever a signal of 1 is read from the appropriate pin, an audio file is played, until the signal transmission is back to 0.

#### NeighbourHoot.py

This file contains code that handles input and transmission to the microbit.

The program reads from the serial port continuously, once it receives an input, it transmits it to the serial port as a readable line. However, if the input is a number from 0-3, an audio piece is played.

#### microbit-hello(13).hex

This file contains the javascript code from the microbit.

This code utilizes serial communication from the raspberry pi to the microbit to output the value sent on an lcd screen. The microbit takes input from three different buttons, one to confirm a game to be played, on to play the game and one to reset every variable. If the cancel button is pressed, a number between 0-3 is transmitted to the serial port.

#### Audio Files (.mp3)

There are four audio files.

- owlintro1.mp3 (Intro when executing Neighbourhoot.py)
- Goodbye.mp3 (Outro when a number between 0-3 is read through the serial port in Neighbourhoot.py)
- Scanned item.mp3 (Audio file played when an item is scanned, aka when a number is read from the serial port, other than 0-3)
- opendoor.mp3 (Audio that plays to alert when a door has been opened in doorcode.py)
