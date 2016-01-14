# germ.py

import itertools, random, math

class Germ:

    germ_colors = ["green", "magenta", "purple", "yellow", "cyan", "lavenderblush", "salmon"]
    speed = 15 # This is an angle, mind you. 

    def __init__(self, canvas: "tkinter.canvas", xy: (int, int), color):
        """
            Creates a germ given the canvas on which to create it, the coordinates, color, and initial velocity.

            canvas - the tkinter canvas that the germ is being created on
            xy - coordinates; location of the germ. To prevent sticking, must be between 0 and bounding area, _exclusively_.
            color - a tkinter-viable color (can be hex)
        """
        # The tag in tkinter representing all parts of this germ. Appended "str" to the front b/c tags don't work if they don't contain letters for some reason.
        self.tag = "str" + str(id(self))

        # 'Adopts' the canvas, and then creates itself on the canvas with the color given.
        # Then moves itself to the given xy coordinate.
        self.canvas = canvas
        self.body = self.canvas.create_oval(0, 0, 11, 11, fill=color, tags=self.tag)
        self.canvas.move(self.body, *xy)
        self.color = color # Saving this mostly just for debugging purposes.
        
        # Create the pivots.
        self.pivots = (self.canvas.create_oval(0, 0, 5, 5, fill=color, tag=self.tag), self.canvas.create_oval(0, 0, 5, 5, fill=color, tag=self.tag))
        self.canvas.move(self.pivots[0], xy[0] - 5, xy[1] - 11)
        self.canvas.move(self.pivots[1], xy[0] + 11, xy[1] - 11)

    @classmethod
    def from_random(cls, canvas: "tkintercanvas"):
        """
            Creates a germ with a random position, color, and velocity. Needs some input, though.

            cls - the current class. Needed to make this a classmethod
            canvas - the tkinter canvas that the germ is being created on
        """
        xy = (random.randint(1, canvas.winfo_width()), random.randint(1, canvas.winfo_height()))
        color = random.choice(cls.germ_colors)
        return cls(canvas, xy, color)

    def move(self, direction: int, moving: int):
        """
            Moves the germ based on its velocity. Bounces off walls.

            direction - A signed integer. If negative, pivot left. If positive, pivot right.
            moving - Also a signed integer. If negative, don't move. If positive, move.
        """
        def oval_center(bounding_box):
            x = math.floor((bounding_box[0] + bounding_box[2]) / 2)
            y = math.floor((bounding_box[1] + bounding_box[3]) / 2)
            return (x, y)

        def rotate_point(xy, pivot_xy, angle):
            angle = -angle if direction > 0 else angle  # Flip the angle to get clockwise rotation when pivoting to the right.
            angle = angle * math.atan(1) * 4 / 180
            xy = list(xy)   # Make xy mutable; it's a tossaway variable anyway.

            # Move to the origin.
            xy[0] -= pivot_xy[0]
            xy[1] -= pivot_xy[1]

            # Rotate the point.
            new_x = xy[0] * math.cos(angle) + xy[1] * math.sin(angle)
            new_y = -xy[0] * math.sin(angle) + xy[1] * math.cos(angle)

            # Move back.
            new_x += pivot_xy[0]
            new_y += pivot_xy[1]

            return (new_x, new_y)

        pivot = oval_center(self.canvas.bbox(self.pivots[0] if direction < 0 else self.pivots[1]))
        speed = Germ.speed if moving > 0 else 0

        body_center = oval_center(self.canvas.bbox(self.body))
        other_pivot = self.pivots[0] if direction > 0 else self.pivots[1]
        other_center = oval_center(self.canvas.bbox(other_pivot))

        body_center_new = rotate_point(body_center, pivot, speed)
        other_center_new = rotate_point(other_center, pivot, speed)

        self.canvas.coords(self.body, (body_center_new[0] - 5, body_center_new[1] - 5, body_center_new[0] + 5, body_center_new[1] + 5))
        self.canvas.coords(other_pivot, (other_center_new[0] - 2, other_center_new[1] - 2, other_center_new[0] + 2, other_center_new[1] + 2))

    def __repr__(self):
        """
            A useful representation for all major components of a germ.
        """
        return "<A {0} at {1}, {2}, with speed of {5}, {6}>".format(self.color, *self.canvas.bbox(self.body), *self.velocity)


def grouped(iterable, n: int):
    """
        Turns an iterable into chunks of n.

        iterable - the long sequence of values.
        n - the amount of items in each group.
    """
    return zip(*[iter(iterable)] * n)
