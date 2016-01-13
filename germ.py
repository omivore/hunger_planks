# germ.py

import itertools, random

class Germ:

    germ_colors = ["green", "magenta", "purple", "yellow", "cyan", "snow", "lavenderblush", "salmon"]
    speed_limit = 3
    germ_speeds = list(itertools.chain(range(-speed_limit - 1, 0), range(1, speed_limit + 1)))

    def __init__(self, canvas: "tkinter.canvas", xy: (int, int), color, velocity: (int, int)):
        """
            Creates a germ given the canvas on which to create it, the coordinates, color, and initial velocity.

            canvas - the tkinter canvas that the germ is being created on
            xy - coordinates; location of the germ
            color - a tkinter-viable color (can be hex)
            velocity - the initial speeds and directions of the germ
        """
        # 'Adopts' the canvas, and then creates itself on the canvas with the color given.
        # Then moves itself to the given xy coordinate.
        self.canvas = canvas
        self.id = self.canvas.create_oval(0, 0, 10, 10, fill=color)
        self.canvas.move(self.id, *xy)
        
        # Determines the starting speed and direction. velocity contains two 'speeds', and the signs
        # is the direction, left or right, or down or up, corresponding to negative or positive.
        self.velocity = list(velocity)

    def move(self):
        """
            Moves the germ based on its velocity. Bounces off walls. (supposedly :P)
            TODO: Make this canvas size independent.
        """
        xy = self.canvas.coords(self.id)
        if xy[1] <= 0 or xy[3] >= 499: self.velocity[1] *= -1
        if xy[2] >= 499 or xy[0] <= 0: self.velocity[0] *= -1
        self.canvas.move(self.id, *self.velocity)

    @classmethod
    def from_random(cls, canvas: "tkintercanvas", bounds: (int, int)):
        """
            Creates a germ with a random position, color, and velocity. Needs some input, though.

            cls - the current class. Needed to make this a classmethod
            canvas - the tkinter canvas that the germ is being created on
            bounds - the maximum boundaries the germ can be in; assumed to start at (0, 0)
        """
        xy = (random.randint(0, bounds[0]), random.randint(0, bounds[1]))
        color = random.choice(cls.germ_colors)
        velocity = (random.choice(cls.germ_speeds), random.choice(cls.germ_speeds))
        return cls(canvas, xy, color, velocity)
