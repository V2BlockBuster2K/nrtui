import time

import mouse
from .mouseinput import MouseInput


class Loop():
    def __init__(self):
        self.stop = False
        self.active = False

        self.ads = False
        self.offset = None
        self.delay = None
        self.mouseinput = MouseInput()

    def start(self):
        while not self.stop:
            if self.active and self.ads:
                if mouse.is_pressed(button='right'):
                    if mouse.is_pressed(button='left'):

                        # Move the mouse
                        self.mouseinput.move(int(self.offset))

                        # Delay between move
                        time.sleep(float(self.delay)/100)
            elif self.active:
                if mouse.is_pressed(button='left'):

                    # Move the mouse
                    self.mouseinput.move(int(self.offset))

                    # Delay between move
                    time.sleep(float(self.delay)/100)

            # Delay for the while loop
            time.sleep(0.001)
