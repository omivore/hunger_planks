# plank.py

import math, random

class Plank():

    width = 6
    colors = ["red", "black", "orange", "green", "lightgreen"]

    def __init__(self, canvas: "tkinter.canvas", start_xy: (int, int), bearing: float, length: int, color, speed: int = 2):
        self.canvas = canvas

        left_start = (start_xy[0] + (Plank.width / 2) * math.cos(math.radians(bearing - 90)), 
                      start_xy[1] + (Plank.width / 2) * math.sin(math.radians(bearing - 90)))
        right_start = (start_xy[0] + (Plank.width / 2) * math.cos(math.radians(bearing + 90)), 
                       start_xy[1] + (Plank.width / 2) * math.sin(math.radians(bearing + 90)))
        left_end = (left_start[0] + length * math.cos(math.radians(bearing)), 
                    left_start[1] + length * math.sin(math.radians(bearing)))
        right_end = (right_start[0] + length * math.cos(math.radians(bearing)), 
                     right_start[1] + length * math.sin(math.radians(bearing)))

        self.body = self.canvas.create_polygon(*left_start, *left_end, *right_end, *right_start, fill=color, tags="plank")
        self.direction = bearing + random.choice([-1, 1]) * 90  # Set the direction as perpindicular to the bearing, randomly picking a side. This might change later on.
        self.speed = speed
        self.dead = False

    @classmethod
    def from_random(cls, canvas):
        start_xy = (random.randint(10, canvas.winfo_width() - 10), random.randint(10, canvas.winfo_height() - 10))
        bearing = random.randrange(360)
        length = random.randrange(5, max(canvas.winfo_width(), canvas.winfo_height()) - 100, 8)
        color = random.choice(Plank.colors)
        speed = random.randrange(1, 4)
        return cls(canvas, start_xy, bearing, length, color, speed)

    def move(self):
        self.canvas.move(self.body,
                         self.speed * math.cos(math.radians(self.direction)),
                         self.speed * math.sin(math.radians(self.direction)))
        if self.body not in self.canvas.find_overlapping(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height()):
            self.die()

    def die(self):
        self.canvas.delete(self.body)
        self.dead = True


class Border(Plank):

    def __init__(self, canvas: "tkinter.canvas", start_xy: (int, int), bearing: float, length: int, color):
        super().__init__(canvas, start_xy, bearing, length, color, 0)

    def move(self):
        # Why would a border move? That would be death to all germs.
        pass

    def die(self):
        # BORDERS NEVER DIE
        pass
