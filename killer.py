from tkinter import *
from germ import Germ

def Killer(Germ):
    def __init__(self, state, canvas: "tkinter.canvas", xy: (int, int), bearing: float):
        super().__init__(state, canvas, xy, bearing, "red")
        self.body = self.canvas.create_oval(0, 0, 11, 11, fill=color, tags="cereal-killer")
        self.spoon = self.canvas.create_oval(0,0,14,14,fill=color)
        self.dead = False;
    @classmethod
    def from_random(cls, get_state, set_state, canvas: "tkintercanvas"):
        """
            Creates a germ with a random position, color, and velocity. Needs some input, though.

            cls - the current class. Needed to make this a classmethod
            canvas - the tkinter canvas that the germ is being created on
        """
        xy = (random.randint(1, canvas.winfo_width()), random.randint(1, canvas.winfo_height()))
        bearing = random.randrange(360)
        return cls(get_state, set_state, canvas, xy, bearing, "red`")

    def killGerm(self):
        overlap = find_overlapping(self.knife)
        for thing in overlap:
            if thing.gettags() is germ:
                thing.die()


    def checkForGerm(self):
        self.spoon = self.canvas.create_oval(0, 0, 14, 14, fill="white")
        killGerm()
        self.canvas.delete(self.spoon)

    def die(self):
        self.dead = True;