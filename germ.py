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
        self.body = self.canvas.create_polygon(*poly_oval(0, 0, 10, 10, 30), fill=color, tags=self.tag)
        self.canvas.move(self.body, *xy)
        self.color = color # Saving this mostly just for debugging purposes.
        
        # Create the pivots.
        self.pivots = (self.canvas.create_polygon(*poly_oval(0, 0, 4, 4, 30), fill=color, tag=self.tag), self.canvas.create_polygon(*poly_oval(0, 0, 4, 4, 30), fill=color, tag=self.tag))
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
        return cls(canvas, xy, color)

    def move(self, direction: int, moving: int):
        """
            Moves the germ based on its velocity. Bounces off walls.

            direction - A signed integer. If negative, pivot left. If positive, pivot right.
            moving - Also a signed integer. If negative, don't move. If positive, move.
        """
        def rotate(canvas, tag, rotate_xy, angle):
            angle = -angle if direction > 0 else angle # Flip angle to achieve clockwise rotation on the right pivot.
            angle = angle * math.atan(1) * 4 / 180
            for item in canvas.find_withtag(tag):
                xy = []
                for x, y in grouped(canvas.coords(item), 2):
                    # Shift to the rotating origin first.
                    x -= rotate_xy[0]
                    y -= rotate_xy[1]

                    # Rotate it.
                    new_x = x * math.cos(angle) + y * math.sin(angle)
                    new_y = -x * math.sin(angle) + y * math.cos(angle)

                    # Shift point back to original place.
                    new_x += rotate_xy[0]
                    new_y += rotate_xy[1]

                    xy += [int(new_x), int(new_y)]
                canvas.coords(item, xy)

        def oval_center(bounding_box):
            x = (bounding_box[0] + bounding_box[2]) / 2
            y = (bounding_box[1] + bounding_box[3]) / 2
            return (x, y)

        pivot = oval_center(self.canvas.bbox(self.pivots[0]) if direction < 0 else self.canvas.bbox(self.pivots[1]))
        speed = Germ.speed if moving > 0 else 0
        rotate(self.canvas, self.tag, pivot, speed)

    def __repr__(self):
        """
            A useful representation for all major components of a germ.
        """
        return "<A {0} at {1}, {2}, with speed of {5}, {6}>".format(self.color, *self.canvas.bbox(self.body), *self.velocity)


def poly_oval(x0: int, y0: int, x1: int, y1: int, edges: int = None):
    """
        Convenience function for Germ to use. It converts ovals to polygons, to allow rotation in tkinter canvas.
    """
    center_x = x0 + x1 / 2
    center_y = y0 + y1 / 2
    radius_x = center_x - x0
    radius_y = center_y - y0

    if not edges: edges = round((radius_x + radius_y) * .5)

    step = math.atan(1) * 8 / edges
    result = []
    top = math.atan(1) * 6

    for _ in range(edges):
        result.append([center_x + radius_x * math.cos(top), center_y + radius_y * math.sin(top)])
        top += step
    return result

def grouped(iterable, n: int):
    """
        Turns an iterable into chunks of n.

        iterable - the long sequence of values.
        n - the amount of items in each group.
    """
    return zip(*[iter(iterable)] * n)
