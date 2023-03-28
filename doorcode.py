from gpiozero import Button 
from signal import pause 
import pygame, pygame.mixer
import os

pygame.mixer.init()

def say_hello(): 
    pygame.mixer.music.stop()
    print("hi")
def say_goodbye():
    print("bye") 
    pygame.mixer.music.load(os.path.join("/home/pi/Doorcode/opendoor.mp3"))
    pygame.mixer.music.play()
    

button1 = Button(3) 
button1.when_pressed = say_hello 
button1.when_released = say_goodbye 

button2 = Button(4) 
button2.when_pressed = say_hello 
button2.when_released = say_goodbye 

button3 = Button(17) 
button3.when_pressed = say_hello 
button3.when_released = say_goodbye 

button4 = Button(27) 
button4.when_pressed = say_hello 
button4.when_released = say_goodbye 
pause()