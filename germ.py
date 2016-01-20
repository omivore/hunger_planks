# germ.py

import itertools, random, math

class Germ:

    germ_colors = ["green", "magenta", "purple", "yellow", "cyan", "lavenderblush", "salmon"]
    speed = 15 # This is an angle, mind you. 

<<<<<<< HEAD
    def __init__(self, canvas: "tkinter.canvas", xy: (int, int), color):
=======
    def __init__(self, state, canvas: "tkinter.canvas", xy: (int, int), bearing: float, color):
>>>>>>> origin/master
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
        self.state = state
        self.canvas = canvas
<<<<<<< HEAD
        self.body = self.canvas.create_oval(0, 0, 11, 11, fill=color, tags=self.tag)
        self.canvas.move(self.body, *xy)
        self.color = color # Saving this mostly just for debugging purposes.
        
        # Create the pivots.
        self.pivots = (self.canvas.create_oval(0, 0, 5, 5, fill=color, tag=self.tag), self.canvas.create_oval(0, 0, 5, 5, fill=color, tag=self.tag))
        self.canvas.move(self.pivots[0], xy[0] - 5, xy[1] - 11)
        self.canvas.move(self.pivots[1], xy[0] + 11, xy[1] - 11)

=======
        self.bearing = bearing
        self.body = self.canvas.create_oval(0, 0, 11, 11, fill=color, tags="germ")
        self.canvas.move(self.body, *xy)

        self.dead = False
        self.color = color # Saving this mostly just for debugging purposes.
        
>>>>>>> origin/master
    @classmethod
    def from_random(cls, state, canvas: "tkintercanvas"):
        """
            Creates a germ with a random position, color, and velocity. Needs some input, though.

            cls - the current class. Needed to make this a classmethod
            canvas - the tkinter canvas that the germ is being created on
        """
        xy = (random.randint(1, canvas.winfo_width()), random.randint(1, canvas.winfo_height()))
        bearing = random.randrange(360)
        color = random.choice(cls.germ_colors)
<<<<<<< HEAD
        return cls(canvas, xy, color)
=======
        return cls(state, canvas, xy, bearing, color)
>>>>>>> origin/master

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
<<<<<<< HEAD
=======
            """
                Rotates a point xy around another point pivot_xy by angle degrees.
            """
>>>>>>> origin/master
            angle = -angle if direction > 0 else angle  # Flip the angle to get clockwise rotation when pivoting to the right.
            angle = math.radians(angle)
            xy = list(xy)   # Make xy mutable; it's a tossaway variable anyway.

            # Move to the origin.
            xy[0] -= pivot_xy[0]
            xy[1] -= pivot_xy[1]
<<<<<<< HEAD

            # Rotate the point.
            new_x = xy[0] * math.cos(angle) + xy[1] * math.sin(angle)
            new_y = -xy[0] * math.sin(angle) + xy[1] * math.cos(angle)

            # Move back.
            new_x += pivot_xy[0]
            new_y += pivot_xy[1]

            return (new_x, new_y)

        pivot = oval_center(self.canvas.bbox(self.pivots[0] if direction < 0 else self.pivots[1]))
        speed = Germ.speed if moving > 0 else 0

        # Calculate the other pivot coordinate.
        other_pivot = self.pivots[0] if direction > 0 else self.pivots[1]
        other_center = rotate_point(oval_center(self.canvas.bbox(other_pivot)), pivot, speed)

        # Calculate the body coordinate.
        body_center = rotate_point(oval_center(self.canvas.bbox(self.body)), pivot, speed)

        self.canvas.coords(self.body, (body_center[0] - 5, body_center[1] - 5, body_center[0] + 5, body_center[1] + 5))
        self.canvas.coords(other_pivot, (other_center[0] - 2, other_center[1] - 2, other_center[0] + 2, other_center[1] + 2))
=======

            # Rotate the point.
            new_x = xy[0] * math.cos(angle) + xy[1] * math.sin(angle)
            new_y = -xy[0] * math.sin(angle) + xy[1] * math.cos(angle)

            # Move back.
            new_x += pivot_xy[0]
            new_y += pivot_xy[1]

            return (new_x, new_y)

        pivots_bearing = self.bearing + direction * math.degrees(math.atan(.75))  # Multiply by direction to get whether to subtract or add to self.bearing.
        body = oval_center(self.canvas.bbox(self.body))
        pivot = (10 * math.cos(math.radians(pivots_bearing)) + body[0], 
                 10 * math.sin(math.radians(pivots_bearing)) + body[1])
        speed = Germ.speed if moving > 0 else 0

        body_center = rotate_point(oval_center(self.canvas.bbox(self.body)), pivot, speed)
        self.bearing = (self.bearing + speed * direction) % 360
>>>>>>> origin/master

        self.canvas.coords(self.body, (body_center[0] - 5, body_center[1] - 5, body_center[0] + 5, body_center[1] + 5))

        self.collision()    # Check for collisions with planks or germs.

    def collision(self):
        """
            Checks for collisions with other objects, and reacts accordingly.
        """
<<<<<<< HEAD
        return "<A {0} at {1}, {2}, with speed of {5}, {6}>".format(self.color, *self.canvas.bbox(self.body), *self.velocity)


def grouped(iterable, n: int):
    """
        Turns an iterable into chunks of n.

        iterable - the long sequence of values.
        n - the amount of items in each group.
    """
    return zip(*[iter(iterable)] * n)
=======
        intruders = list(self.canvas.find_overlapping(*self.canvas.bbox(self.body)))
        intruders.remove(self.body)    # Remove itself from the list.
        for intruder in intruders:
            if "plank" in self.canvas.gettags(intruder):
                # Kill both parties if colliding with a plank.
                for citizen in self.state():
                    if citizen.body == intruder: citizen.die()
                self.die()

            elif "germ" in self.canvas.gettags(intruder):
                print("Oh hi friend!")

    def die(self):
        self.canvas.delete(self.body)
        self.dead = True
>>>>>>> origin/master
