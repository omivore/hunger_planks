# plank.py

import math, random
from germ import lines_intersect

class Plank():

    width = 6
    colors = ["red", "black", "orange", "green", "lightgreen"]

    def __init__(self, get_state, set_state, canvas: "tkinter.canvas", start_xy: (int, int), bearing: float, length: int, color, speed: int = 2):
        self.canvas = canvas
        self.get_state = get_state
        self.set_state = set_state

        end_xy = (start_xy[0] + length * math.cos(math.radians(bearing)), 
                  start_xy[1] + length * math.sin(math.radians(bearing)))

        self.body = self.canvas.create_line(*start_xy, *end_xy, width=Plank.width, fill=color, tags="plank")
        self.direction = bearing + random.choice([-1, 1]) * 90  # Set the direction as perpindicular to the bearing, randomly picking a side. This might change later on.
        self.speed = speed

    @classmethod
    def from_random(cls, get_state, set_state, canvas):
        start_xy = (random.randint(10, canvas.winfo_width() - 10), random.randint(10, canvas.winfo_height() - 10))
        bearing = random.randrange(360)
        length = random.randrange(5, max(canvas.winfo_width(), canvas.winfo_height()) - 100, 8)
        color = random.choice(Plank.colors)
        speed = random.randrange(1, 4)
        return cls(get_state, set_state, canvas, start_xy, bearing, length, color, speed)

    def move(self):
        self.canvas.move(self.body,
                         self.speed * math.cos(math.radians(self.direction)),
                         self.speed * math.sin(math.radians(self.direction)))
        if self.body not in self.canvas.find_overlapping(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height()):
            self.die()

    def seen(self, raycast_tag):
        bone = self.canvas.coords(self.body)
        raycast = self.canvas.coords(self.canvas.find_withtag(raycast_tag)[0])

        return lines_intersect(bone, raycast)

    def die(self):
        self.canvas.delete(self.body)
        current = self.get_state()
        current[1].remove(self)
        self.set_state(*current)


class Border(Plank):

    def __init__(self, get_state, set_state, canvas: "tkinter.canvas", start_xy: (int, int), bearing: float, length: int, color):
        super().__init__(get_state, set_state, canvas, start_xy, bearing, length, color, 0)

    def move(self):
        # Why would a border move? That would be death to all germs.
        pass

    def die(self):
        # BORDERS NEVER DIE
        pass
