# germ.py

import itertools, random, math

class Germ:

    germ_colors = ["green", "magenta", "purple", "yellow", "cyan", "lavenderblush", "salmon"]
    speed = 15 # This is an angle, mind you. 

    def __init__(self, state, canvas: "tkinter.canvas", xy: (int, int), bearing: float, color):
        """
            Creates a germ given the canvas on which to create it, the coordinates, color, and initial velocity.

            canvas - the tkinter canvas that the germ is being created on
            xy - coordinates; location of the germ. To prevent sticking, must be between 0 and bounding area, _exclusively_.
            color - a tkinter-viable color (can be hex)
        """
        # 'Adopts' the canvas, and then creates itself on the canvas with the color given.
        # Then moves itself to the given xy coordinate.
        self.state = state
        self.canvas = canvas
        self.bearing = bearing
        self.body = self.canvas.create_oval(0, 0, 11, 11, fill=color, tags="germ")
        self.canvas.move(self.body, *xy)

        self.dead = False
        self.color = color # Saving this mostly just for debugging purposes.
        
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
        return cls(state, canvas, xy, bearing, color)

    @staticmethod
    def oval_center(bounding_box):
        x = math.floor((bounding_box[0] + bounding_box[2]) / 2)
        y = math.floor((bounding_box[1] + bounding_box[3]) / 2)
        return (x, y)

    def move(self, direction: int, moving: int):
        """
            Moves the germ based on its velocity. Bounces off walls.

            direction - A signed integer. If negative, pivot left. If positive, pivot right.
            moving - Also a signed integer. If negative, don't move. If positive, move.
        """
        def rotate_point(xy, pivot_xy, angle):
            """
                Rotates a point xy around another point pivot_xy by angle degrees.
            """
            angle = -angle if direction > 0 else angle  # Flip the angle to get clockwise rotation when pivoting to the right.
            angle = math.radians(angle)
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

        pivots_bearing = self.bearing + direction * math.degrees(math.atan(.75))  # Multiply by direction to get whether to subtract or add to self.bearing.
        body = Germ.oval_center(self.canvas.bbox(self.body))
        pivot = (10 * math.cos(math.radians(pivots_bearing)) + body[0], 
                 10 * math.sin(math.radians(pivots_bearing)) + body[1])
        speed = Germ.speed if moving > 0 else 0

        body_center = rotate_point(Germ.oval_center(self.canvas.bbox(self.body)), pivot, speed)
        self.bearing = (self.bearing + speed * direction) % 360

        self.canvas.coords(self.body, (body_center[0] - 5, body_center[1] - 5, body_center[0] + 5, body_center[1] + 5))

        self.collision()    # Check for collisions with planks or germs.

    def collision(self):
        """
            Checks for collisions with other objects, and reacts accordingly.
        """
        intruders = list(self.canvas.find_overlapping(*self.canvas.bbox(self.body)))
        intruders.remove(self.body)    # Remove itself from the list.
        for intruder in intruders:
            if "plank" in self.canvas.gettags(intruder):
                # Kill both parties if colliding with a plank.
                for citizen in self.state():
                    if citizen.body == intruder: citizen.die()
                self.die()

            elif "germ" in self.canvas.gettags(intruder):
                # If two germs bounce into each other, they'll bounce away from each other
                self_xy = Germ.oval_center(self.canvas.bbox(self.body))
                other_xy = Germ.oval_center(self.canvas.bbox(intruder))
                offset_y = other_xy[1] - self_xy[1]
                offset_x = other_xy[0] - self_xy[0]
                self_new = (self_xy[0] - .5 * offset_x, self_xy[1] - .5 * offset_y)
                other_new = (other_xy[0] + .5 * offset_x, other_xy[1] + .5 * offset_y)

                # Apply the new repercussion-ed coordinates
                self.canvas.coords(self.body, (self_new[0] - 5, self_new[1] - 5, self_new[0] + 5, self_new[1] + 5))
                self.canvas.coords(intruder, (other_new[0] - 5, other_new[1] - 5, other_new[0] + 5, other_new[1] + 5))

    def die(self):
        self.canvas.delete(self.body)
        self.dead = True
