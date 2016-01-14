# germ.py

import itertools, random

class Germ:

    germ_colors = ["green", "magenta", "purple", "yellow", "cyan", "snow", "lavenderblush", "salmon"]
    speed_limit = 3 
    germ_speeds = list(itertools.chain(range(-speed_limit, 0), range(1, speed_limit + 1)))

    def __init__(self, canvas: "tkinter.canvas", xy: (int, int), color, velocity: (int, int)):
        """
            Creates a germ given the canvas on which to create it, the coordinates, color, and initial velocity.

            canvas - the tkinter canvas that the germ is being created on
            xy - coordinates; location of the germ. To prevent sticking, must be between 0 and bounding area, _exclusively_.
            color - a tkinter-viable color (can be hex)
            velocity - the initial speeds and directions of the germ
        """
        # 'Adopts' the canvas, and then creates itself on the canvas with the color given.
        # Then moves itself to the given xy coordinate.
        self.canvas = canvas
        self.tag = "str" + str(id(self))    # The tag in tkinter representing all parts of this germ. Appended "str" to the front b/c tags don't work if they don't contain letters for some reason.
        self.body = self.canvas.create_oval(0, 0, 10, 10, fill=color, tags=self.tag)
        self.canvas.move(self.body, *xy)
        self.color = color # Saving this mostly just for debugging purposes.
        
        # Determines the starting speed and direction. velocity contains two 'speeds', and the signs
        # is the direction, left or right, or down or up, corresponding to negative or positive.
        self.velocity = list(velocity)

        # Create the pivots.
        self.pivots = (self.canvas.create_oval(0, 0, 4, 4, fill=color, tag=self.tag), self.canvas.create_oval(0, 0, 4, 4, fill=color, tag=self.tag))
        self.canvas.move(self.pivots[0], xy[0] - 5, xy[1] - 10)
        self.canvas.move(self.pivots[1], xy[0] + 11, xy[1] - 10)

    @classmethod
    def from_random(cls, canvas: "tkintercanvas"):
        """
            Creates a germ with a random position, color, and velocity. Needs some input, though.

            cls - the current class. Needed to make this a classmethod
            canvas - the tkinter canvas that the germ is being created on
        """
        xy = (random.randint(1, canvas.winfo_width()), random.randint(1, canvas.winfo_height()))
        color = random.choice(cls.germ_colors)
        velocity = (random.choice(cls.germ_speeds), random.choice(cls.germ_speeds))
        return cls(canvas, xy, color, velocity)

    def move(self):
        """
            Moves the germ based on its velocity. Bounces off walls.
        """
        xy = self.canvas.coords(self.tag)
        if xy[1] <= 0 or xy[3] >= self.canvas.winfo_height():
            self.velocity[1] *= -1

            # If germ is stuck in the stuttering gap, this will boost it out.
            if xy[1] + self.velocity[1] <= 0:
                self.canvas.move(self.tag, 0, 0 - xy[1])
            elif xy[3] + self.velocity[1] >= self.canvas.winfo_height():
                self.canvas.move(self.tag, 0, self.canvas.winfo_height() - xy[3])

        if xy[2] >= self.canvas.winfo_width() or xy[0] <= 0:
            self.velocity[0] *= -1

            # Same thing here.
            if xy[0] + self.velocity[0] <= 0:
                self.canvas.move(self.tag, 0 - xy[0], 0)
            elif xy[2] + self.velocity[1] >= self.canvas.winfo_width():
                self.canvas.move(self.tag, self.canvas.winfo_width() - xy[2], 0)


        self.canvas.move(self.tag, *self.velocity)

    def __repr__(self):
        """
            A useful representation for all major components of a germ.
        """
        return "<A {0} at {1}, {2}, with speed of {5}, {6}>".format(self.color, *self.canvas.coords(self.id), *self.velocity)
