# plank.py

import math, random
from germ import grouped

class Plank():

    width = 6
    speed = 2

    def __init__(self, canvas: "tkinter.canvas", start_xy: (int, int), bearing: float, length: int, color):
        self.canvas = canvas

        left_start = (start_xy[0] + (Plank.width / 2) * math.cos(math.radians(bearing - 90)), 
                      start_xy[1] + (Plank.width / 2) * math.sin(math.radians(bearing - 90)))
        right_start = (start_xy[0] + (Plank.width / 2) * math.cos(math.radians(bearing + 90)), 
                       start_xy[1] + (Plank.width / 2) * math.sin(math.radians(bearing + 90)))
        left_end = (left_start[0] + length * math.cos(math.radians(bearing)), 
                    left_start[1] + length * math.sin(math.radians(bearing)))
        right_end = (right_start[0] + length * math.cos(math.radians(bearing)), 
                     right_start[1] + length * math.sin(math.radians(bearing)))

        self.body = self.canvas.create_polygon(*left_start, *left_end, *right_end, *right_start, fill=color)
        # Set the direction as perpindicular to the bearing, randomly picking a side. This might change later on.
        self.direction = bearing + random.choice([-1, 1]) * 90

    def move(self):
        self.canvas.move(self.body,
                         Plank.speed * math.cos(math.radians(self.direction)),
                         Plank.speed * math.sin(math.radians(self.direction)))
