# germ.py

import itertools, random, math
from brain import Brain

class Germ:

    germ_colors = ["green", "magenta", "purple", "yellow", "cyan", "lavenderblush", "salmon"]
    speed = 15 # This is an angle, mind you. 


    def __init__(self, state, canvas: "tkinter.canvas", xy: (int, int), bearing: float, color, synapses: ("input_synapses", "hidden_synapses")=(None, None)):
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
        self.brain = Brain.from_random() if not (synapses[0] and synapses[1]) else Brain(*synapses)
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

    def execute(self):
        """
            Does all the management for one loop of the game loop. Call this to do stuff.
        """
        perceptions = self.sight()
        decisions = self.brain.think(perceptions)
        self.move(*decisions)

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

        pivots_bearing = self.bearing + math.copysign(math.degrees(math.atan(.75)), direction)  # Take the sign of direction to get whether to subtract or add to self.bearing.
        body = Germ.oval_center(self.canvas.bbox(self.body))
        pivot = (10 * math.cos(math.radians(pivots_bearing)) + body[0], 
                 10 * math.sin(math.radians(pivots_bearing)) + body[1])
        speed = Germ.speed if moving > 0 else 0

        body_center = rotate_point(Germ.oval_center(self.canvas.bbox(self.body)), pivot, speed)
        self.bearing = (self.bearing + math.copysign(speed, direction)) % 360

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

    def seen(self, raycast_tag) -> bool:
        """
            Checks if the given tag intersects with self. Returns true or false accordingly.
        """
        center = self.oval_center(self.canvas.bbox(self.body))
        bone = (center[0] - 5, center[1], center[0] + 5, center[1])
        raycast = self.canvas.coords(self.canvas.find_withtag(raycast_tag)[0])

        return lines_intersect(bone, raycast)

    def sight(self) -> [float for _ in range(8)]:
        """
            Raycasts in eight directions and gets the object (if any) in that direction. If there is an object, this will compute the distance proportionately.
            If the object (if any) is a plank, then the float will be negative. If another germ, then it will be positive. If there isn't an object, then 0.
        """
        xy = Germ.oval_center(self.canvas.bbox(self.body))
        sight_bearings = [offset + self.bearing for offset in range(0, 360, 45)]
        sights = []     # Our results array.
        for bearing in sight_bearings:
            end = (xy[0] + 132 * math.cos(math.radians(bearing)), xy[1] + 132 * math.sin(math.radians(bearing)))
            sightline = self.canvas.create_line(*xy, *end, tags="raycast")

            seen = dict()
            for citizen in [citizen for citizen in self.state() if citizen != self]:
                intersect = citizen.seen("raycast")
                if intersect:
                    seen[citizen] = intersect
            self.canvas.delete(sightline)

            # For each object, calculate the distance away from self. The closest is the one the eye sees.
            closest = (None, 133)   # This will be the closest citizen, and then the distance.
            for citizen in seen:
                distance = math.hypot(seen[citizen][0] - xy[0], seen[citizen][1] - xy[1])
                if distance < closest[1]: closest = (citizen, distance)

            # If closest is still none, then nothing's within the range of the germ.
            if not closest[0]:
                sights.append(0)
                continue

            # Generate result based on the distance.
            scaled_distance = 1 - (closest[1] / 132)        # Normalizes the distance so it's between 0 and 1, where the smaller the number, the farther away it is.
            proportioned_distance = scaled_distance ** 2    # Squares the distance to mimic light intensity (see inverse-square law).

            # See if the object seen is a germ or a plank, and change the sign of this eye's result accordingly.
            if "germ" in self.canvas.gettags(closest[0].body):
                sights.append(math.copysign(proportioned_distance, 1))
            else:   # Then citizen must be a plank. Run!
                sights.append(math.copysign(proportioned_distance, -1))

        return sights

    def die(self):
        """
            Removes this germ from the canvas, then marks itself as dead so it can be removed from the overall state.
        """
        self.canvas.delete(self.body)
        self.dead = True


def lines_intersect(line1: (int, int, int, int), line2: (int, int, int, int)) -> bool:
    """
        Returns point of intersection if lines intersect, false if they don't. Lines comes in the format of (end_x, end_y, otherend_x, otherend_y).
    """
    if intersects(line1, line2):
        return intersection(line1, line2)
    else: return False

def intersects(line1, line2) -> bool:
    def ccw(point1, point2, point3):
        """
            Checks if triplet is counter clockwise.
        """
        return (point3[1] - point1[1]) * (point2[0] - point1[0]) > (point2[1] - point1[1]) * (point3[0] - point1[0])
    return ccw((line1[0], line1[1]), (line2[0], line2[1]), (line2[2], line2[3])) != ccw((line1[2], line1[3]), (line2[0], line2[1]), (line2[2], line2[3])) and \
           ccw((line1[0], line1[1]), (line1[2], line1[3]), (line2[0], line2[1])) != ccw((line1[0], line1[1]), (line1[2], line1[3]), (line2[2], line2[3]))

def intersection(line1, line2):
    xdiff = (line1[0] - line1[2], line2[0] - line2[2])
    ydiff = (line1[1] - line1[3], line2[1] - line2[3])

    def determinate(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = determinate(xdiff, ydiff)
    if div == 0:
        return False

    d = (determinate((line1[0], line1[1]), (line1[2], line1[3])), determinate((line2[0], line2[1]), (line2[2], line2[3])))
    x = determinate(d, xdiff) / div
    y = determinate(d, ydiff) / div
    return x, y
