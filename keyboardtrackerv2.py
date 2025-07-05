import os
from time import sleep

from pynput.keyboard import Key, Listener

  
def show(key):
    
    if key == Key.tab:
        print("good")
        os.system('python jjd.py')


# Collect all event until released
while True:
    Listener(on_press = show)
                